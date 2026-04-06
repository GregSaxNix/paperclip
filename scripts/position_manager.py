"""
position_manager.py -- Life Admin Position Manager CLI

Manages the "position as identity, model as engine" system for Paperclip agents.
One agent per position; model swaps are transparent.

Usage:
  python position_manager.py status              # Show all positions + active model
  python position_manager.py sub CEO fallback1   # Switch CEO to Fallback 1
  python position_manager.py sub all fallback1   # Switch ALL positions to Fallback 1
  python position_manager.py restore CEO         # Restore CEO to Primary
  python position_manager.py restore all         # Restore all to Primary
  python position_manager.py sync CEO            # Push SOUL.md + adapter + skills to agent
  python position_manager.py sync all            # Sync all positions to Paperclip
  python position_manager.py dashboard           # Generate + open lineup_dashboard.html
  python position_manager.py provision Finance   # Create new agent for position
  python position_manager.py check-quota         # Check Claude + Codex usage, suggest subs

API: http://127.0.0.1:3100 | X-Trusted-Local: true
"""

import json
import os
import re
import sys
import time
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ─── Config ──────────────────────────────────────────────────────────────────

BASE_URL = "http://127.0.0.1:3100"
COMPANY_ID = "505ab906-66b5-4400-b131-96b8aee91c5d"
HEADERS = {"X-Trusted-Local": "true", "Content-Type": "application/json"}

POSITIONS_DIR = Path(__file__).parent.parent / "positions"
POSITIONS_JSON = POSITIONS_DIR / "positions.json"
DASHBOARD_HTML = Path(__file__).parent / "lineup_dashboard.html"
LLM_MATRIX_DATA = Path(__file__).parent / "llm-matrix-data.json"

# ─── Skill key resolution (full keys to avoid ambiguity) ─────────────────────
# Use full keys for skills that have multiple versions (local + upstream)
SKILL_KEY_OVERRIDES = {
    "council-debate":  "paperclipai/paperclip/council-debate",
    "skill-discovery": "paperclipai/paperclip/skill-discovery",
    "paperclip":       "paperclipai/paperclip/paperclip",
    "paperclip-create-agent":  "paperclipai/paperclip/paperclip-create-agent",
    "paperclip-create-plugin": "paperclipai/paperclip/paperclip-create-plugin",
    "para-memory-files": "paperclipai/paperclip/para-memory-files",
}

def resolve_skills(skills):
    """Resolve short skill names to full keys where needed."""
    return [SKILL_KEY_OVERRIDES.get(s, s) for s in skills]


# ─── Pricing helpers (reads from llm-matrix-data.json) ───────────────────────

def load_pricing():
    r"""Return {model_id: {input_per_1m, output_per_1m}} for API-backed models.
    Reads from D:\paperclip\scripts\llm-matrix-data.json (single source of truth).
    Returns empty dict if file not found.
    """
    if not LLM_MATRIX_DATA.exists():
        return {}
    try:
        with open(LLM_MATRIX_DATA, encoding="utf-8") as f:
            data = json.load(f)
        return {
            m["id"]: {"input_per_1m": m["input_per_1m"], "output_per_1m": m["output_per_1m"]}
            for m in data.get("models", [])
            if m.get("input_per_1m", 0) > 0 or m.get("output_per_1m", 0) > 0
        }
    except Exception:
        return {}


def get_ollama_price_config(model, pricing):
    """Return inputTokenPriceUsd/outputTokenPriceUsd fields for an ollama_local model.
    Returns empty dict for local models (not in pricing map — stays $0).
    """
    if model in pricing:
        p = pricing[model]
        return {
            "inputTokenPriceUsd": p["input_per_1m"] / 1_000_000,
            "outputTokenPriceUsd": p["output_per_1m"] / 1_000_000,
        }
    return {}

# ─── Position map: key -> (dept/position, character, agent_id) ────────────────

POSITION_MAP = {
    "CEO":             ("executive/CEO",              "Clawdy",         "297d6a61-9900-4e31-9e7e-8ec3fa93c7a3"),
    "CTO":             ("executive/CTO",              "Gayan",          "56d606ab-a36c-4cd9-bf71-1ed422d49d4e"),
    "COO":             ("executive/COO",              "COO",            "b9acdc0e-671b-4956-9d14-ee9761ad9f06"),
    "SeniorEngineer":  ("technology/senior-engineer", "Senior Eng",     "20afbcb3-9fd0-4d72-a44e-16c2a4bea983"),
    "Engineer":        ("technology/engineer",        "Engineer",       "787afb8c-df1d-4632-8ee3-40da4d06f17b"),
    "QABot":           ("technology/qa-bot",          "QA Bot",         "6ba034eb-b618-4aef-9de8-afc8336853be"),
    "Designer":        ("technology/designer",        "Designer",       "5f031fe8-6bd7-4a33-a8eb-705f5f3e6c69"),
    "ContentLead":     ("business-ops/content-lead",  "Content Lead",   "d4047079-65bb-49d4-9bc6-f5a8e3fe259a"),
    "Accountant":      ("business-ops/accountant",    "Accountant",     "e51a0fc4-367f-4e2c-9ad5-702a0cba546b"),
    "Spielberg":       ("business-ops/spielberg",     "Spielberg",      "8a28534f-4dd2-4802-98ab-7e83712874ea"),
    "Finance":         ("finance/finance",             "Finance",        "f2e65bc6-31af-4053-acbd-187cd3d89d92"),
    "Doc":             ("health/doc",                 "Doc",            "40a94a4b-043e-46e7-97c3-dac60fc911d2"),
    "Freud":           ("health/freud",               "Freud",          "00544001-8e06-4739-a6ad-8b5fc18bf1de"),
    "TravelAgent":     ("travel/travel-agent",        "Travel Agent",   "66de6564-88df-4a0c-b918-299d2d6619ea"),
    "Researcher":      ("research/researcher",        "Researcher",     "9d589490-af2a-4717-b7a8-b61c60059765"),
    "Yoda":            ("council/yoda",               "Yoda",           "19c2937c-8e11-4f18-a166-9cdec6ab07e5"),
    "Contrarian":      ("council/contrarian",         "Contrarian",     "e8ce7488-0d6d-42c8-a63f-88e46d8a0a7c"),
    "CouncilLocal":    ("council/local",              "Council Local",  "579e8c85-f6f2-4ddb-af55-e970312756a3"),
    "CouncilEU":       ("council/eu",                 "Council EU",     "c02e9e21-2fc8-4cfb-998a-59cc1a1ce3b0"),
    "CouncilCH":       ("council/ch",                 "Council CH",     "bdb5860d-8bc6-46e1-b808-2307afd14b1c"),
    "CouncilTech":     ("council/tech",               "Council Tech",   "614bf0a2-5576-49c7-b993-525ffdb83698"),
}

# Local-only positions (hard privacy constraint -- never sub to cloud)
LOCAL_ONLY = {"Doc", "Freud", "CouncilLocal"}

# ─── API helpers ─────────────────────────────────────────────────────────────

def api(method, path, body=None, retries=2):
    """Make an API call to Paperclip."""
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=HEADERS, method=method)
    for attempt in range(retries + 1):
        try:
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except HTTPError as e:
            error_body = e.read().decode()
            print(f"  HTTP {e.code} from {method} {path}: {error_body[:200]}")
            return None
        except (URLError, TimeoutError) as e:
            if attempt < retries:
                print(f"  Timeout/error (attempt {attempt+1}/{retries+1}), retrying...")
                time.sleep(2)
            else:
                print(f"  Connection error after {retries+1} attempts: {e}")
                return None


def get_agent(agent_id):
    return api("GET", f"/api/agents/{agent_id}")


def patch_agent(agent_id, body):
    return api("PATCH", f"/api/agents/{agent_id}", body)


def put_instruction_file(agent_id, path, content):
    return api("PUT", f"/api/agents/{agent_id}/instructions-bundle/file",
               {"path": path, "content": content})


def sync_skills(agent_id, skills):
    return api("POST", f"/api/agents/{agent_id}/skills/sync",
               {"desiredSkills": skills})


def create_agent(name, role, adapter_type, adapter_config):
    return api("POST", f"/api/companies/{COMPANY_ID}/agents", {
        "name": name,
        "role": role,
        "adapterType": adapter_type,
        "adapterConfig": adapter_config,
    })

# ─── LINEUP.md parser ─────────────────────────────────────────────────────────

def parse_lineup(position_key):
    """Parse LINEUP.md for a position and return list of slot dicts."""
    dept_path, _, _ = POSITION_MAP[position_key]
    lineup_file = POSITIONS_DIR / dept_path / "LINEUP.md"
    if not lineup_file.exists():
        return []

    slots = []
    with open(lineup_file, encoding="utf-8") as f:
        content = f.read()

    # Parse markdown table rows
    # Format: | Slot | adapterType | model | Cost | When to use |
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|") or "---" in line or "Slot" in line:
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 4:
            continue
        slot_name = parts[0]
        if slot_name.lower() in ("slot",):
            continue
        slots.append({
            "slot": slot_name,
            "adapterType": parts[1],
            "model": parts[2],
            "cost": parts[3],
            "when": parts[4] if len(parts) > 4 else "",
        })
    return slots


def get_slot_config(position_key, slot_label):
    """Get adapter config for a named slot (e.g. 'Primary', 'Fallback 1', 'fallback1')."""
    # Normalise slot label
    label_map = {
        "primary": "Primary",
        "fallback1": "Fallback 1",
        "fallback 1": "Fallback 1",
        "fallback2": "Fallback 2",
        "fallback 2": "Fallback 2",
        "emergency": "Emergency",
    }
    normalised = label_map.get(slot_label.lower(), slot_label)

    slots = parse_lineup(position_key)
    for s in slots:
        if s["slot"].lower() == normalised.lower():
            return s
    return None

# ─── positions.json ────────────────────────────────────────────────────────────

def load_positions():
    """Load current positions.json state."""
    if POSITIONS_JSON.exists():
        with open(POSITIONS_JSON, encoding="utf-8") as f:
            return json.load(f)
    return {"last_updated": None, "positions": {}}


def save_positions(state):
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(POSITIONS_JSON, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def build_positions_from_api():
    """Build positions.json by querying the API for current agent state."""
    print("Building positions.json from API state...")
    state = {"last_updated": None, "positions": {}}

    for key, (dept_path, character, agent_id) in POSITION_MAP.items():
        if agent_id is None:
            state["positions"][key] = {
                "agent_id": None,
                "character": character,
                "dept_path": dept_path,
                "active_slot": "Primary",
                "active_adapter": "TBD",
                "active_model": "TBD",
                "local_only": key in LOCAL_ONLY,
                "last_sub": None,
            }
            continue

        agent = get_agent(agent_id)
        if not agent:
            print(f"  Warning: could not fetch agent {agent_id} ({key})")
            continue

        agent_data = agent.get("agent", agent)
        state["positions"][key] = {
            "agent_id": agent_id,
            "character": character,
            "dept_path": dept_path,
            "active_slot": "Primary",
            "active_adapter": agent_data.get("adapterType", "unknown"),
            "active_model": agent_data.get("adapterConfig", {}).get("model", "unknown"),
            "local_only": key in LOCAL_ONLY,
            "last_sub": None,
        }
        print(f"  {key}: {agent_data.get('adapterType')} / {agent_data.get('adapterConfig', {}).get('model', '?')}")

    save_positions(state)
    print(f"Saved to {POSITIONS_JSON}")
    return state

# ─── Commands ─────────────────────────────────────────────────────────────────

def cmd_status(args):
    """Show all positions and their active model."""
    state = load_positions()
    if not state["positions"]:
        print("No positions.json found. Run: python position_manager.py sync all")
        return

    print(f"\n{'LIFE ADMIN -- STARTING LINEUP':^80}")
    print(f"{'Last updated: ' + (state.get('last_updated','?')[:19] if state.get('last_updated') else 'never'):^80}")
    print("=" * 80)
    fmt = "{:<18} {:<16} {:<22} {:<12} {:<6}"
    print(fmt.format("POSITION", "CHARACTER", "ACTIVE MODEL", "SLOT", "FLAGS"))
    print("-" * 80)

    for key, pos in state["positions"].items():
        flags = ""
        if pos.get("local_only"):
            flags += "[L]"
        if pos.get("active_slot", "Primary") != "Primary":
            flags += "[!]"
        if pos.get("agent_id") is None:
            flags += "NEW"

        model = pos.get("active_model", "TBD")[:21]
        print(fmt.format(
            key[:17],
            pos.get("character", "")[:15],
            model,
            pos.get("active_slot", "Primary")[:11],
            flags,
        ))

    print("=" * 80)
    non_primary = [k for k, p in state["positions"].items() if p.get("active_slot", "Primary") != "Primary"]
    if non_primary:
        print(f"  [!] {len(non_primary)} position(s) on fallback: {', '.join(non_primary)}")
    print()


def cmd_sub(args):
    """Sub a position to a fallback slot. Usage: sub CEO fallback1"""
    if len(args) < 2:
        print("Usage: python position_manager.py sub <POSITION|all> <fallback1|fallback2|emergency>")
        return

    position_arg, slot_arg = args[0], args[1]
    targets = list(POSITION_MAP.keys()) if position_arg.lower() == "all" else [position_arg]

    state = load_positions()

    for key in targets:
        if key not in POSITION_MAP:
            print(f"Unknown position: {key}")
            continue

        if key in LOCAL_ONLY:
            print(f"  SKIP {key} -- LOCAL ONLY, cannot sub to cloud")
            continue

        _, _, agent_id = POSITION_MAP[key]
        if not agent_id:
            print(f"  SKIP {key} -- not yet provisioned")
            continue

        slot = get_slot_config(key, slot_arg)
        if not slot:
            print(f"  No slot '{slot_arg}' found for {key}")
            continue

        print(f"  Subbing {key} -> {slot['slot']} ({slot['adapterType']} / {slot['model']})...")
        dept_path = POSITION_MAP[key][0]
        soul_path = str(POSITIONS_DIR / dept_path / "SOUL.md").replace("\\", "/")
        adapter_config = {
            "model": slot["model"],
            "instructionsFilePath": soul_path,
        }
        # Add per-token pricing for API-backed ollama models
        if slot["adapterType"] == "ollama_local":
            pricing = load_pricing()
            adapter_config.update(get_ollama_price_config(slot["model"], pricing))

        result = patch_agent(agent_id, {
            "adapterType": slot["adapterType"],
            "adapterConfig": adapter_config,
            "replaceAdapterConfig": True,
        })

        if result:
            print(f"    OK -- {key} now on {slot['slot']}")
            if key in state["positions"]:
                state["positions"][key]["active_slot"] = slot["slot"]
                state["positions"][key]["active_adapter"] = slot["adapterType"]
                state["positions"][key]["active_model"] = slot["model"]
                state["positions"][key]["last_sub"] = datetime.now(timezone.utc).isoformat()
        else:
            print(f"    FAILED -- {key} sub unsuccessful")

    save_positions(state)
    generate_dashboard(state)


def cmd_restore(args):
    """Restore a position to Primary slot. Usage: restore CEO | restore all"""
    if not args:
        print("Usage: python position_manager.py restore <POSITION|all>")
        return

    position_arg = args[0]
    targets = list(POSITION_MAP.keys()) if position_arg.lower() == "all" else [position_arg]

    for key in targets:
        cmd_sub([key, "primary"])


def cmd_sync(args):
    """Sync SOUL.md + adapter + skills to agent. Usage: sync CEO | sync all"""
    if not args:
        print("Usage: python position_manager.py sync <POSITION|all>")
        return

    position_arg = args[0]
    targets = list(POSITION_MAP.keys()) if position_arg.lower() == "all" else [position_arg]

    state = load_positions()

    # Build reportsTo map
    reports_to = {
        "CTO":            "297d6a61-9900-4e31-9e7e-8ec3fa93c7a3",  # -> CEO
        "COO":            "297d6a61-9900-4e31-9e7e-8ec3fa93c7a3",  # -> CEO
        "SeniorEngineer": "56d606ab-a36c-4cd9-bf71-1ed422d49d4e",  # -> CTO
        "Engineer":       "56d606ab-a36c-4cd9-bf71-1ed422d49d4e",  # -> CTO
        "QABot":          "56d606ab-a36c-4cd9-bf71-1ed422d49d4e",  # -> CTO
        "Designer":       "56d606ab-a36c-4cd9-bf71-1ed422d49d4e",  # -> CTO
        "ContentLead":    "b9acdc0e-671b-4956-9d14-ee9761ad9f06",  # -> COO
        "Accountant":     "b9acdc0e-671b-4956-9d14-ee9761ad9f06",  # -> COO
        "Spielberg":      "b9acdc0e-671b-4956-9d14-ee9761ad9f06",  # -> COO
        "Freud":          "40a94a4b-043e-46e7-97c3-dac60fc911d2",  # -> Doc
    }

    for key in targets:
        if key not in POSITION_MAP:
            print(f"Unknown position: {key}")
            continue

        dept_path, character, agent_id = POSITION_MAP[key]
        if not agent_id:
            print(f"  SKIP {key} -- not yet provisioned (run: provision {key})")
            continue

        print(f"\nSyncing {key} ({character}, {agent_id[:8]})...")

        # 1. Read Primary slot config from LINEUP.md
        primary = get_slot_config(key, "Primary")
        if not primary:
            print(f"  WARNING: No Primary slot found in LINEUP.md for {key}")
            continue

        soul_path = str(POSITIONS_DIR / dept_path / "SOUL.md")
        soul_path_fwd = soul_path.replace("\\", "/")

        # 2. Read SOUL.md content
        if not Path(soul_path).exists():
            print(f"  WARNING: No SOUL.md found at {soul_path}")
            continue
        with open(soul_path, encoding="utf-8") as f:
            soul_content = f.read()

        # 3. Push SOUL.md to agent
        print(f"  Uploading SOUL.md...")
        result = put_instruction_file(agent_id, "SOUL.md", soul_content)
        if not result:
            print(f"  WARNING: Failed to upload SOUL.md for {key}")

        # 4. Update adapter + model + reportsTo (with pricing for ollama API-backed models)
        adapter_config = {
            "model": primary["model"],
            "instructionsFilePath": soul_path_fwd,
        }
        if primary["adapterType"] == "ollama_local":
            pricing = load_pricing()
            adapter_config.update(get_ollama_price_config(primary["model"], pricing))
        patch_body = {
            "adapterType": primary["adapterType"],
            "adapterConfig": adapter_config,
            "replaceAdapterConfig": True,
        }
        if key in reports_to:
            patch_body["reportsTo"] = reports_to[key]
        elif key == "CEO":
            patch_body["reportsTo"] = None  # CEO reports to nobody

        print(f"  Setting adapter: {primary['adapterType']} / {primary['model']}...")
        result = patch_agent(agent_id, patch_body)
        if not result:
            print(f"  WARNING: Failed to update adapter for {key}")
        else:
            print(f"  Adapter updated OK")

        # 5. Sync skills
        skills_file = POSITIONS_DIR / dept_path / "SKILLS.md"
        if skills_file.exists():
            with open(skills_file, encoding="utf-8") as f:
                skills_content = f.read()
            # Parse skill keys from "## System Skills (installed)" section only.
            # Falls back to reading all "- skill-name" lines for legacy flat-format files.
            in_system_section = False
            has_sections = any(l.strip().startswith("## System Skills") for l in skills_content.splitlines())
            skills = []
            for line in skills_content.splitlines():
                stripped = line.strip()
                if stripped.startswith("## System Skills"):
                    in_system_section = True
                    continue
                if stripped.startswith("##") and in_system_section:
                    break
                if (not has_sections or in_system_section) and stripped.startswith("- ") and not stripped.startswith("- #"):
                    skill = stripped.lstrip("- ").strip()
                    # Strip optional description after " -- " or " — " separator
                    for sep in (" \u2014 ", " -- "):
                        if sep in skill:
                            skill = skill.split(sep)[0].strip()
                            break
                    if skill:
                        skills.append(skill)
            if skills:
                resolved = resolve_skills(skills)
                print(f"  Syncing skills: {resolved}...")
                result = sync_skills(agent_id, resolved)
                if result:
                    print(f"  Skills synced OK")
                else:
                    print(f"  WARNING: Skills sync failed (may not be supported by adapter)")

        # 6. Update positions.json
        if key in state["positions"]:
            state["positions"][key]["active_slot"] = "Primary"
            state["positions"][key]["active_adapter"] = primary["adapterType"]
            state["positions"][key]["active_model"] = primary["model"]
            state["positions"][key]["last_sub"] = None

        print(f"  {key} sync complete")

    save_positions(state)
    generate_dashboard(state)
    print(f"\nSync complete. Dashboard updated.")


def cmd_dashboard(args):
    """Generate and open the lineup dashboard."""
    state = load_positions()
    generate_dashboard(state)
    print(f"Dashboard generated: {DASHBOARD_HTML}")
    webbrowser.open(f"file:///{DASHBOARD_HTML}")


def _soul_tagline(dept_path: str) -> str:
    """Extract the italicised tagline from a position's SOUL.md."""
    soul_file = POSITIONS_DIR / dept_path / "SOUL.md"
    if not soul_file.exists():
        return ""
    for line in soul_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("_") and stripped.endswith("_") and len(stripped) > 3:
            return stripped.strip("_")
    return ""


def _slot_chip(slot_dict: dict, is_active: bool) -> str:
    """Render a single lineup slot as a coloured chip (light mode)."""
    slot_name = slot_dict.get("slot", "?")
    model = slot_dict.get("model", "?")
    adapter = slot_dict.get("adapterType", "")
    cost = slot_dict.get("cost", "")

    # Light mode: clean, readable chips
    colour_map = {
        "Primary":    ("#1d4ed8", "#ffffff", "#1d4ed8"),   # bg, text, border — solid blue
        "Fallback 1": ("#ffffff", "#78350f", "#d97706"),   # white bg, amber text+border
        "Fallback 2": ("#ffffff", "#6b21a8", "#9333ea"),   # white bg, purple text+border
        "Emergency":  ("#ffffff", "#b91c1c", "#ef4444"),   # white bg, red text+border
    }
    bg, fg, border_col = colour_map.get(slot_name, ("#f1f5f9", "#334155", "#e2e8f0"))
    border = f"2px solid {border_col}" if is_active else f"1px solid {border_col}"
    opacity = "1" if is_active else "0.45"
    cost_str = f'<br><span style="font-size:0.68em;opacity:0.75">{cost}</span>' if cost else ""
    return (
        f'<span title="{slot_name}: {adapter}/{model}" style="'
        f'display:inline-block;background:{bg};color:{fg};border:{border};'
        f'border-radius:6px;padding:3px 8px;margin:2px;font-size:0.78em;opacity:{opacity};vertical-align:top">'
        f'{slot_name}<br><code style="background:none;border:none;padding:0;color:{fg};font-size:0.88em;font-weight:600">{model}</code>'
        f'{cost_str}</span>'
    )


def _usage_banner() -> str:
    """Read claude-usage.json and render a usage banner if available."""
    usage_file = Path(__file__).parent.parent / "claude-usage.json"
    if not usage_file.exists():
        return '<p style="color:#64748b;font-size:0.85em">No usage data yet &mdash; run <code>python scripts/check_claude_usage.py</code></p>'
    try:
        data = json.loads(usage_file.read_text(encoding="utf-8"))
    except Exception:
        return ""

    checked = data.get("last_checked", "")[:19].replace("T", " ")
    meters = data.get("meters", {})
    if not meters:
        err = data.get("error", "No data")
        return f'<p style="color:#f87171;font-size:0.85em">Usage check error: {err}</p>'

    bars = []
    colours = {"session": "#3b82f6", "all_models": "#10b981", "sonnet": "#8b5cf6"}
    labels = {"session": "Session (5hr window)", "all_models": "All Models (weekly)", "sonnet": "Sonnet (weekly)"}
    for key, info in meters.items():
        pct = info.get("pct", 0)
        reset = info.get("reset_text", "")
        col = colours.get(key, "#94a3b8")
        warn_col = "#f59e0b" if pct >= 70 else col
        limit_col = "#ef4444" if pct >= 90 else warn_col
        label = labels.get(key, key)
        bars.append(
            f'<div style="margin-bottom:8px">'
            f'<span style="font-size:0.8em;color:#475569">{label}</span>'
            f'<span style="float:right;font-size:0.8em;color:{limit_col};font-weight:600">{pct}% {("&mdash; " + reset) if reset else ""}</span>'
            f'<div style="clear:both;height:6px;background:#e2e8f0;border-radius:3px;margin-top:2px">'
            f'<div style="width:{pct}%;height:6px;background:{limit_col};border-radius:3px"></div>'
            f'</div></div>'
        )

    return (
        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:14px 18px;margin-bottom:18px">'
        f'<div style="font-size:0.8em;color:#64748b;margin-bottom:10px">Claude Max Plan Usage &mdash; checked {checked} &nbsp;'
        f'<a href="javascript:location.reload()" style="color:#3b82f6;font-size:0.9em">refresh</a></div>'
        + "".join(bars) +
        f'</div>'
    )


def generate_dashboard(state):
    """Generate lineup_dashboard.html — full lineup matrix with fallback chains."""
    rows = []

    # Group positions by department for visual separation
    dept_order = [
        ("Executive", ["CEO", "CTO", "COO"]),
        ("Technology", ["SeniorEngineer", "Engineer", "QABot", "Designer"]),
        ("Business Ops", ["ContentLead", "Accountant", "Spielberg"]),
        ("Finance", ["Finance"]),
        ("Travel", ["TravelAgent"]),
        ("Research", ["Researcher"]),
        ("Health", ["Doc", "Freud"]),
        ("Council", ["Yoda", "Contrarian", "CouncilLocal", "CouncilEU", "CouncilCH", "CouncilTech"]),
    ]

    for dept_name, keys in dept_order:
        rows.append(f'<tr class="dept-header"><td colspan="5">{dept_name}</td></tr>')
        for key in keys:
            pos = state["positions"].get(key)
            if not pos:
                continue

            active_slot = pos.get("active_slot", "Primary")
            dept_path = pos.get("dept_path", "")
            tagline = _soul_tagline(dept_path)
            slots = parse_lineup(key)

            # Build slot chips
            chips = ""
            if slots:
                for s in slots:
                    is_active = s["slot"].lower() == active_slot.lower()
                    chips += _slot_chip(s, is_active)
            else:
                model = pos.get("active_model", "TBD")
                chips = f'<code>{model}</code>'

            # Status badges
            badges = ""
            if pos.get("local_only"):
                badges += '<span class="badge local">LOCAL ONLY</span>'
            if active_slot != "Primary":
                badges += f'<span class="badge warn">ON {active_slot.upper()}</span>'

            last_sub = pos.get("last_sub", "")
            last_sub_str = last_sub[:16].replace("T", " ") if last_sub else "&mdash;"

            row_class = "primary"
            if active_slot != "Primary":
                row_class = "emergency" if "Emergency" in active_slot else "fallback"

            rows.append(f"""
        <tr class="{row_class}">
          <td>
            <strong style="color:#0f172a">{key}</strong>
            <span style="color:#94a3b8;font-size:0.8em;display:block">{pos.get('character','')}</span>
          </td>
          <td style="color:#64748b;font-size:0.82em;max-width:220px;font-style:italic">{tagline}</td>
          <td>{chips}</td>
          <td style="font-size:0.8em;color:#94a3b8">{last_sub_str}</td>
          <td>{badges}</td>
        </tr>""")

    last_updated = state.get("last_updated", "")
    last_updated_str = last_updated[:19].replace("T", " ") if last_updated else "never"
    usage_banner = _usage_banner()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="60">
  <title>Life Admin &mdash; Agent Matrix</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f1f5f9; color: #1e293b; margin: 0; padding: 20px; }}
    h1 {{ color: #0f172a; font-size: 1.4em; margin-bottom: 2px; }}
    .subtitle {{ color: #64748b; font-size: 0.82em; margin-bottom: 16px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }}
    th {{ background: #f8fafc; padding: 9px 12px; text-align: left; font-size: 0.75em; text-transform: uppercase; letter-spacing: 0.06em; color: #94a3b8; border-bottom: 1px solid #e2e8f0; }}
    td {{ padding: 9px 12px; border-bottom: 1px solid #f1f5f9; vertical-align: top; }}
    tr:last-child td {{ border-bottom: none; }}
    tr.dept-header td {{ background: #f8fafc; color: #94a3b8; font-size: 0.72em; text-transform: uppercase; letter-spacing: 0.1em; padding: 5px 12px; font-weight: 700; border-bottom: 1px solid #e2e8f0; }}
    tr.fallback td {{ background: #fffbeb; }}
    tr.emergency td {{ background: #fff1f2; }}
    code {{ background: #f1f5f9; border: 1px solid #e2e8f0; padding: 1px 5px; border-radius: 4px; font-size: 0.82em; color: #334155; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.72em; margin-right: 3px; font-weight: 600; }}
    .badge.local {{ background: #dbeafe; color: #1d4ed8; }}
    .badge.warn {{ background: #fef3c7; color: #92400e; }}
    a {{ color: #3b82f6; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .legend {{ margin-top: 14px; font-size: 0.78em; color: #94a3b8; line-height: 1.8; }}
  </style>
</head>
<body>
  <h1>Life Admin &mdash; Agent Matrix</h1>
  <p class="subtitle">Updated: {last_updated_str} &nbsp;&bull;&nbsp; Auto-refreshes every 60s &nbsp;&bull;&nbsp;
    <a href="javascript:location.reload()">Refresh now</a> &nbsp;&bull;&nbsp;
    <a href="ops-hub.html">Ops Hub</a>
  </p>

  {usage_banner}

  <table>
    <thead>
      <tr>
        <th style="width:130px">Position</th>
        <th style="width:220px">Role</th>
        <th>Lineup (hover for detail) &mdash; <strong style="color:#1d4ed8">bold border = active</strong></th>
        <th style="width:110px">Last Sub</th>
        <th style="width:110px">Status</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>

  <div class="legend">
    <strong style="color:#1d4ed8">LOCAL ONLY</strong> = health data never leaves this machine (Doc, Freud, Council Local) &nbsp;&bull;&nbsp;
    <strong style="color:#92400e">ON FALLBACK</strong> = primary model substituted &nbsp;&bull;&nbsp;
    Chip opacity: full = active, dimmed = available fallback<br>
    Manage: <code>python position_manager.py [status | sub CEO fallback1 | restore CEO | dashboard]</code>
  </div>
</body>
</html>"""

    with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
        f.write(html)


def cmd_provision(args):
    """Create a new agent for a position. Usage: provision Finance"""
    if not args:
        print("Usage: python position_manager.py provision <POSITION>")
        return

    key = args[0]
    if key not in POSITION_MAP:
        print(f"Unknown position: {key}")
        return

    dept_path, character, existing_id = POSITION_MAP[key]
    if existing_id:
        print(f"{key} already has agent ID {existing_id}. Nothing to provision.")
        return

    primary = get_slot_config(key, "Primary")
    if not primary:
        print(f"No Primary slot in LINEUP.md for {key}")
        return

    role_map = {
        "Finance": "general",
        "TravelAgent": "general",
    }
    role = role_map.get(key, "general")

    soul_path = str(POSITIONS_DIR / dept_path / "SOUL.md").replace("\\", "/")
    print(f"Creating agent for {key} ({character})...")

    result = create_agent(
        name=character,
        role=role,
        adapter_type=primary["adapterType"],
        adapter_config={
            "model": primary["model"],
            "instructionsFilePath": soul_path,
        }
    )

    if result:
        new_id = result.get("agent", result).get("id", "?")
        print(f"  Created: {character} -- ID: {new_id}")
        print(f"  Add this ID to POSITION_MAP['{key}'] in position_manager.py")
        print(f"  Then run: python position_manager.py sync {key}")
    else:
        print(f"  FAILED to create agent for {key}")


def cmd_check_quota(args):
    """Check usage quota status and suggest any needed subs."""
    claude_json = Path(__file__).parent.parent / "claude-usage.json"
    codex_json = Path(__file__).parent.parent / "codex-quota.json"

    print("\nQuota check:")
    if claude_json.exists():
        with open(claude_json, encoding="utf-8") as f:
            d = json.load(f)
        print(f"  Claude Opus: {d.get('opus_used','?')} / {d.get('opus_limit','?')} -- should_use_opus: {d.get('should_use_opus','?')}")
        print(f"  Checked: {d.get('last_checked','?')}")
        if not d.get("should_use_opus", True):
            print("  [!]  Opus limit approached -- consider: python position_manager.py sub CEO fallback1")
            print("  [!]                                    python position_manager.py sub CTO fallback1")
            print("  [!]                                    python position_manager.py sub Yoda fallback1")
    else:
        print("  Claude usage: no data (run check_claude_usage.py)")

    if codex_json.exists():
        with open(codex_json, encoding="utf-8") as f:
            d = json.load(f)
        print(f"  Codex: used {d.get('used','?')} -- should_use_codex: {d.get('should_use_codex','?')}")
        if not d.get("should_use_codex", True):
            print("  [!]  Codex limit hit -- run: python position_manager.py sub Engineer fallback1")
            print("  [!]                          python position_manager.py sub CouncilTech fallback1")
    else:
        print("  Codex quota: no data (run check_codex_quota.py)")
    print()


# ─── Main ─────────────────────────────────────────────────────────────────────

COMMANDS = {
    "status": cmd_status,
    "sub": cmd_sub,
    "restore": cmd_restore,
    "sync": cmd_sync,
    "dashboard": cmd_dashboard,
    "provision": cmd_provision,
    "check-quota": cmd_check_quota,
    "init": lambda _: build_positions_from_api(),
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(COMMANDS.keys())}")
        sys.exit(1)

    COMMANDS[cmd](args)
