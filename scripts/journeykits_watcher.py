"""
JourneyKits.ai Watcher
======================
Periodically checks JourneyKits.ai for new skills from trusted publishers,
screens them, installs SKILL.md files, and posts a Paperclip issue summary.

Schedule: Sundays 6 AM AEST via Windows Task Scheduler.
Run:       python D:/paperclip/scripts/journeykits_watcher.py
Log:       D:/paperclip/scripts/journeykits_watcher.log
State:     D:/paperclip/scripts/journeykits_state.json
"""

import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

JOURNEYKITS_BASE = "https://www.journeykits.ai/api"
TRUSTED_PUBLISHERS = {"matt-clawd", "citadel", "codex113", "ez-corp"}

SKILLS_DIR = Path(r"C:\Users\Administrator\.claude\skills")
STATE_FILE = Path(r"D:\paperclip\scripts\journeykits_state.json")
LOG_FILE = Path(r"D:\paperclip\scripts\journeykits_watcher.log")

PAPERCLIP_BASE = "http://localhost:3100"
LIFE_ADMIN_COMPANY_ID = "505ab906-66b5-4400-b131-96b8aee91c5d"
RESEARCHER_AGENT_ID = "9d589490-af2a-4717-b7a8-b61c60059765"

# Hard dependencies that disqualify a kit
BLOCKED_DEPENDENCIES = {
    "gog",
    "fish-audio",
    "openclaw-gateway",
    "telegram-bot",
    "firecrawl",
    "fxtwitter",
    "sqlcipher",
}

PAGE_SIZE = 100


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line.encode("ascii", errors="replace").decode("ascii"))
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_json(url: str) -> dict | list | None:
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"HTTP {e.code} fetching {url}")
        return None
    except Exception as e:
        log(f"Error fetching {url}: {e}")
        return None


def post_json(url: str, payload: dict) -> dict | None:
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"Error posting to {url}: {e}")
        return None


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Fetch kits from JourneyKits API (paginated)
# ---------------------------------------------------------------------------

def fetch_all_kits() -> list[dict]:
    kits = []
    offset = 0
    while True:
        url = f"{JOURNEYKITS_BASE}/kits?limit={PAGE_SIZE}&offset={offset}"
        page = fetch_json(url)
        if not page:
            break
        # API returns {"items": [...], "total": N} or plain list
        if isinstance(page, list):
            items = page
        else:
            items = page.get("items", page.get("kits", page.get("data", [])))
        if not items:
            break
        kits.extend(items)
        if len(items) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
    return kits


def fetch_kit_detail(owner: str, slug: str) -> dict | None:
    url = f"{JOURNEYKITS_BASE}/kits/{owner}/{slug}"
    return fetch_json(url)


# ---------------------------------------------------------------------------
# Screening
# ---------------------------------------------------------------------------

def get_existing_skill_slugs() -> set[str]:
    if not SKILLS_DIR.exists():
        return set()
    return {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}


def screen_kit(kit: dict, existing_slugs: set[str]) -> tuple[bool, str]:
    """
    Returns (passes, reason_if_failed).
    Checks in order — stops at first FAIL.
    """
    slug = kit.get("slug", "")
    owner = kit.get("owner", kit.get("publisher", ""))
    setup_difficulty = (kit.get("setupDifficulty") or kit.get("setup_difficulty") or "").lower()
    self_contained = kit.get("selfContained", kit.get("self_contained", True))
    complexity_score = kit.get("complexityScore", kit.get("complexity_score", 0)) or 0

    # 1. Publisher filter
    if owner not in TRUSTED_PUBLISHERS:
        return False, f"publisher '{owner}' not in trusted list"

    # 2. Setup difficulty
    if setup_difficulty == "high":
        return False, "setupDifficulty is 'high'"

    # 3. Self-contained check
    if not self_contained and complexity_score > 5:
        return False, f"not self-contained and complexityScore={complexity_score} > 5"

    # 4. Blocked dependencies
    deps_raw = kit.get("dependencies", kit.get("hardDependencies", []))
    if isinstance(deps_raw, str):
        deps_raw = [d.strip() for d in deps_raw.split(",") if d.strip()]
    deps = {str(d).lower() for d in deps_raw}
    blocked = deps & BLOCKED_DEPENDENCIES
    if blocked:
        return False, f"blocked dependency: {', '.join(blocked)}"

    # Check description/tags for blocked deps too
    description = (kit.get("description") or "").lower()
    tags = " ".join(str(t) for t in kit.get("tags", [])).lower()
    combined = description + " " + tags
    for blocked_dep in BLOCKED_DEPENDENCIES:
        if blocked_dep.replace("-", " ") in combined or blocked_dep in combined:
            return False, f"blocked dependency referenced in description: {blocked_dep}"

    # 5. Redundancy check
    if slug in existing_slugs:
        return False, f"slug '{slug}' already installed"

    return True, ""


# ---------------------------------------------------------------------------
# SKILL.md generation
# ---------------------------------------------------------------------------

def synthesise_skill_md(kit: dict) -> str:
    slug = kit.get("slug", "unknown")
    name = kit.get("name", slug)
    description = kit.get("description", "No description provided.")
    owner = kit.get("owner", kit.get("publisher", "unknown"))
    license_str = kit.get("license", "MIT")
    model = kit.get("recommendedModel", kit.get("model", "claude-sonnet-4-6"))
    tags = kit.get("tags", [])
    usage = kit.get("usage", kit.get("instructions", ""))
    triggers = kit.get("triggers", [])
    tools = kit.get("tools", [])

    # Build trigger list — use tags + name words if triggers not explicit
    if not triggers:
        triggers = [t.lower().replace("-", " ") for t in tags[:5]]
    trigger_lines = "\n".join(f"  - \"{t}\"" for t in triggers[:8]) if triggers else ""

    # Build tool list
    if not tools:
        tools = ["Read", "Glob", "Grep", "Bash", "Write"]
    tool_lines = "\n".join(f"  - {t}" for t in tools)

    # Truncate description for frontmatter (max 3 lines)
    short_desc = textwrap.fill(description, width=100)
    if len(short_desc) > 300:
        short_desc = short_desc[:297] + "..."

    # Body — use full usage/instructions if available, else description
    body = usage.strip() if usage.strip() else description.strip()

    triggers_block = f"triggers:\n{trigger_lines}\n" if trigger_lines else ""
    skill_md = f"""---
name: {slug}
description: >
  {short_desc}
{triggers_block}model: {model}
tools:
{tool_lines}
license: {license_str}
source: {owner}
---

# {name}

{body}

---

*Auto-installed by JourneyKits Watcher on {datetime.now(timezone.utc).strftime('%Y-%m-%d')}.*
*Source: {owner}/{slug} on JourneyKits.ai*
"""
    return skill_md


# ---------------------------------------------------------------------------
# Install a skill
# ---------------------------------------------------------------------------

def install_skill(kit: dict) -> bool:
    slug = kit.get("slug", "")
    if not slug:
        return False

    skill_dir = SKILLS_DIR / slug
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md = synthesise_skill_md(kit)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_md, encoding="utf-8")

    log(f"INSTALLED: {slug} → {skill_file}")
    return True


# ---------------------------------------------------------------------------
# Paperclip issue
# ---------------------------------------------------------------------------

def post_paperclip_issue(installs: list[dict], skipped: list[dict]) -> None:
    if not installs and not skipped:
        return

    install_lines = "\n".join(
        f"- **{k['slug']}** ({k.get('owner', k.get('publisher', '?'))}) — {k.get('name', k['slug'])}"
        for k in installs
    ) or "None"

    skip_sample = skipped[:10]
    skip_lines = "\n".join(
        f"- {k['slug']}: {k.get('_skip_reason', 'filtered')}"
        for k in skip_sample
    ) or "None"
    if len(skipped) > 10:
        skip_lines += f"\n- ... and {len(skipped) - 10} more"

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    body = f"""Weekly JourneyKits.ai scan completed on {date_str}.

## Installed ({len(installs)})

{install_lines}

## Skipped ({len(skipped)})

{skip_lines}

Skills directory: `C:\\Users\\Administrator\\.claude\\skills\\`
"""

    payload = {
        "companyId": LIFE_ADMIN_COMPANY_ID,
        "title": f"JourneyKits Watcher — {len(installs)} new skills ({date_str})",
        "description": body,
        "status": "todo",
        "assignedAgentId": RESEARCHER_AGENT_ID,
    }

    result = post_json(f"{PAPERCLIP_BASE}/api/companies/{LIFE_ADMIN_COMPANY_ID}/issues", payload)
    if result:
        issue_id = result.get("id", result.get("issueId", "?"))
        log(f"Paperclip issue created: {issue_id}")
    else:
        log("Warning: Could not create Paperclip issue (server may be offline)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    log("=== JourneyKits Watcher starting ===")

    state = load_state()
    existing_slugs = get_existing_skill_slugs()
    log(f"Existing skills: {len(existing_slugs)}")

    log("Fetching kits from JourneyKits.ai...")
    all_kits = fetch_all_kits()
    log(f"Fetched {len(all_kits)} kits total")

    installs = []
    skipped = []

    for kit in all_kits:
        slug = kit.get("slug", "")
        owner = kit.get("owner", kit.get("publisher", ""))
        if not slug:
            continue

        state_key = f"{owner}/{slug}"
        latest_tag = kit.get("latestReleaseTag", kit.get("version", ""))

        # Check if already processed at this version
        if state_key in state:
            if state[state_key].get("latestReleaseTag") == latest_tag:
                continue  # No new version

        # Screen
        passes, reason = screen_kit(kit, existing_slugs)
        if not passes:
            kit["_skip_reason"] = reason
            skipped.append(kit)
            log(f"SKIP: {slug} — {reason}")
            # Still record in state to avoid re-checking known skips
            state[state_key] = {
                "slug": slug,
                "owner": owner,
                "latestReleaseTag": latest_tag,
                "status": "skipped",
                "skipReason": reason,
                "checkedAt": datetime.now(timezone.utc).isoformat(),
            }
            continue

        # Fetch full detail before installing
        detail = fetch_kit_detail(owner, slug)
        if detail:
            kit.update(detail)

        # Install
        if install_skill(kit):
            installs.append(kit)
            existing_slugs.add(slug)
            state[state_key] = {
                "slug": slug,
                "owner": owner,
                "latestReleaseTag": latest_tag,
                "status": "installed",
                "installedAt": datetime.now(timezone.utc).isoformat(),
            }

    save_state(state)

    log(f"Summary: {len(installs)} installed, {len(skipped)} skipped this run")
    post_paperclip_issue(installs, skipped)
    log("=== JourneyKits Watcher complete ===")


if __name__ == "__main__":
    main()
