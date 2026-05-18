r"""
check_model_lineups.py -- LLM model lineup monitor for Life Admin agents

Compares the top-ranked model from the LLM hiring algorithm against what each
Paperclip agent is actually running. Posts a Paperclip issue when a meaningfully
better model is available. Greg reviews and approves; changes are applied in the
next Claude Code session.

Usage:
    python check_model_lineups.py              # check and post issues
    python check_model_lineups.py --dry-run    # print recommendations only, no posting
    python check_model_lineups.py --force      # re-post even if already in state.json
    python check_model_lineups.py --json       # machine-readable JSON output

Reuses:
    update_llm_matrix.py  -- compute_rankings(), load_data()
    position_manager.py   -- POSITION_MAP, LOCAL_ONLY

Schedule: Task Scheduler "Model Lineup Monitor" -- 1st of each month, 9:00 AM
Log:      D:\paperclip\scripts\model-lineups.log
State:    D:\paperclip\scripts\check_model_lineups_state.json
"""

import argparse
import json
import logging
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

# Reuse existing algorithm and position map -- no duplication
from update_llm_matrix import (  # noqa: E402
    compute_rankings,
    load_data,
    _parse_guidelines_sections,
    GUIDELINES_STALE_DAYS,
)
from position_manager import LOCAL_ONLY, POSITION_MAP      # noqa: E402

# ── Constants ─────────────────────────────────────────────────────────────────

PAPERCLIP_BASE = "http://localhost:3100"
COMPANY_ID     = "505ab906-66b5-4400-b131-96b8aee91c5d"
LOG_FILE       = SCRIPTS_DIR / "model-lineups.log"
STATE_FILE     = SCRIPTS_DIR / "check_model_lineups_state.json"

# Only flag if top-recommended score exceeds current model's score by at least this
SCORE_THRESHOLD = 0.3

# Positions to skip (hard privacy constraint + standalone utility agents)
SKIP_POSITIONS = LOCAL_ONLY | {"Gemini"}

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)


# ── Helpers ───────────────────────────────────────────────────────────────────

def norm(model_id: str) -> str:
    """Normalise model ID for comparison (case/punctuation-insensitive)."""
    return model_id.lower().translate(str.maketrans("", "", "-_. /"))


def paperclip_get(path: str) -> dict:
    req = urllib.request.Request(
        f"{PAPERCLIP_BASE}{path}",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def paperclip_post(path: str, body: dict) -> dict:
    payload = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{PAPERCLIP_BASE}{path}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()[:200]}"}


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


# ── Core logic ────────────────────────────────────────────────────────────────

def get_live_models() -> dict:
    """Return {agent_id: model_id} from live Paperclip agent configs."""
    data = paperclip_get(f"/api/companies/{COMPANY_ID}/agents")
    agents = data if isinstance(data, list) else data.get("agents", data.get("data", []))
    return {
        a["id"]: a.get("adapterConfig", {}).get("model", "unknown")
        for a in agents
    }


def find_current_score(candidates: list, live_model: str) -> float | None:
    """Find the score of the live model in the ranked candidates list."""
    live_norm = norm(live_model)
    for c in candidates:
        if norm(c["model_id"]) == live_norm:
            return c["score"]
    return None


def build_recommendations(data: dict, rankings: dict, live_models: dict) -> list:
    """
    For each monitored position, compare top-1 recommendation vs live model.
    Returns a list of recommendation dicts for positions needing a change.
    """
    recs = []
    all_results = []  # for summary table (all positions)

    for pos_key, (dept_path, character, agent_id) in POSITION_MAP.items():
        if pos_key in SKIP_POSITIONS:
            all_results.append({
                "pos_key": pos_key,
                "character": character,
                "live_model": "—",
                "recommended": "—",
                "current_score": None,
                "top_score": None,
                "delta": None,
                "status": "skipped",
            })
            continue

        candidates = rankings.get(pos_key)
        if not candidates:
            all_results.append({
                "pos_key": pos_key,
                "character": character,
                "live_model": "—",
                "recommended": "—",
                "current_score": None,
                "top_score": None,
                "delta": None,
                "status": "no_profile",
            })
            continue

        live_model = live_models.get(agent_id, "unknown")
        top = candidates[0]
        top_score = top["score"]
        current_score = find_current_score(candidates, live_model)

        is_match = norm(top["model_id"]) == norm(live_model)

        if is_match:
            status = "ok"
            delta = 0.0
        elif current_score is None:
            # Live model not in matrix rankings (e.g. provisioned outside matrix)
            status = "untracked"
            delta = None
        else:
            delta = round(top_score - current_score, 2)
            status = "upgrade" if delta >= SCORE_THRESHOLD else "marginal"

        result = {
            "pos_key": pos_key,
            "character": character,
            "agent_id": agent_id,
            "live_model": live_model,
            "recommended": top["model_id"],
            "recommended_name": top["name"],
            "current_score": current_score,
            "top_score": top_score,
            "delta": delta,
            "status": status,
            "cost_note": top["cost_note"],
        }
        all_results.append(result)

        if status == "upgrade":
            recs.append(result)

    return recs, all_results


def post_issue(rec: dict, matrix_updated: str) -> dict:
    current_score_str = f"{rec['current_score']:.2f}" if rec["current_score"] is not None else "unranked"
    delta_str = f"+{rec['delta']:.2f}" if rec["delta"] else "n/a"
    title = f"Model upgrade available: {rec['character']} ({rec['live_model']} -> {rec['recommended_name']})"
    body = (
        f"Position: {rec['character']}\n"
        f"Current:     {rec['live_model']:<30} score: {current_score_str}\n"
        f"Recommended: {rec['recommended_name']:<30} score: {rec['top_score']:.2f}  ({delta_str})\n"
        f"Cost: {rec['cost_note']}\n\n"
        f"To apply in next Claude Code session:\n"
        f"  python D:/paperclip/scripts/position_manager.py sub {rec['pos_key']} Primary\n\n"
        f"Approve this issue to action it, or cancel to keep current model.\n"
        f"LLM matrix last updated: {matrix_updated}"
    )
    return paperclip_post(f"/api/companies/{COMPANY_ID}/issues", {
        "title": title,
        "description": body,
        "status": "todo",
    })


# ── MODEL-PROMPTING-GUIDELINES audit (weekly drift check) ─────────────────────

def audit_guidelines() -> dict:
    """Audit MODEL-PROMPTING-GUIDELINES.md for drift.

    Returns a dict: {total, filled, stubs, stale, broken, stale_sections,
    broken_sections, stub_sections, missing_for_models}.

    `missing_for_models` lists active models in MODEL-RESEARCH.md (via
    llm-matrix-data.json) that don't have a section in MODEL-PROMPTING-GUIDELINES.md.
    """
    sections = _parse_guidelines_sections()
    filled = [s for s in sections if not s["is_stub"]]
    stubs = [s for s in sections if s["is_stub"]]
    stale = [s for s in filled if s["stale"]]
    broken = [s for s in filled if s["broken_url"]]

    # Check coverage: every active (non-deprecated, scored) model should be findable
    # in some section. Match by provider OR by token overlap with the models string.
    data = load_data()
    missing = []
    for m in data.get("models", []):
        if m.get("status") == "deprecated":
            continue
        provider = (m.get("provider") or "").lower()
        name = (m.get("name") or "").lower()
        model_id = (m.get("id") or "").lower()
        matched = False
        for s in sections:
            hay = " ".join([s["heading"], s["provider"], s["models"], s["slug"]]).lower()
            # Provider name match (e.g. "Anthropic", "Google", "DeepSeek") is the
            # primary signal — sections are organised by provider.
            if provider and any(tok in hay for tok in provider.split() if len(tok) > 2):
                matched = True
                break
            # Fallback: token-based match on the model name/id.
            tokens = [t for t in (name + " " + model_id).replace("/", " ").split() if len(t) > 2]
            if tokens and all(t in hay for t in tokens):
                matched = True
                break
        if not matched:
            missing.append({"id": m.get("id"), "name": m.get("name"), "provider": m.get("provider")})

    return {
        "total": len(sections),
        "filled": len(filled),
        "stubs": len(stubs),
        "stale_count": len(stale),
        "broken_count": len(broken),
        "stale_sections": [s["heading"] for s in stale],
        "broken_sections": [s["heading"] for s in broken],
        "stub_sections": [s["heading"] for s in stubs],
        "missing_for_models": missing,
    }


def post_guidelines_issue(audit: dict) -> dict:
    """Post a Paperclip issue summarising guideline drift. Called only when there's drift."""
    lines = ["MODEL-PROMPTING-GUIDELINES.md needs the Researcher's attention.\n"]
    lines.append(f"Total sections: {audit['total']}  (filled: {audit['filled']}, stubs: {audit['stubs']})\n")

    if audit["stale_sections"]:
        lines.append(f"\nSTALE sections (Date captured > {GUIDELINES_STALE_DAYS} days old — refresh required):")
        for h in audit["stale_sections"]:
            lines.append(f"  - {h}")

    if audit["broken_sections"]:
        lines.append(f"\nBROKEN URLs (Provider docs URL missing or pending — refresh required):")
        for h in audit["broken_sections"]:
            lines.append(f"  - {h}")

    if audit["missing_for_models"]:
        lines.append(f"\nACTIVE models with NO guideline section (add one using the template):")
        for m in audit["missing_for_models"]:
            lines.append(f"  - {m['provider']}: {m['name']}  (id: {m['id']})")

    if audit["stub_sections"]:
        lines.append(f"\nStub sections (provider not yet active — informational only, no action required unless newly activated in LLM-MATRIX.md):")
        for h in audit["stub_sections"]:
            lines.append(f"  - {h}")

    lines.append("\nTo work this issue, ask the Researcher: \"refresh MODEL-PROMPTING-GUIDELINES.md\" — the weekly checklist is in positions/research/researcher/SOUL.md.")
    lines.append("\nVerify locally: python D:/paperclip/scripts/update_llm_matrix.py --guidelines-stale")

    title_bits = []
    if audit["stale_sections"]:
        title_bits.append(f"{len(audit['stale_sections'])} stale")
    if audit["broken_sections"]:
        title_bits.append(f"{len(audit['broken_sections'])} broken")
    if audit["missing_for_models"]:
        title_bits.append(f"{len(audit['missing_for_models'])} missing")
    title = f"MODEL-PROMPTING-GUIDELINES drift: " + ", ".join(title_bits) if title_bits else "MODEL-PROMPTING-GUIDELINES drift: review"

    return paperclip_post(f"/api/companies/{COMPANY_ID}/issues", {
        "title": title,
        "description": "\n".join(lines),
        "status": "todo",
    })


# ── Output formatters ─────────────────────────────────────────────────────────

def print_table(all_results: list, recs: list) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"\nModel Lineup Monitor -- {now}")
    print(f"{'Position':<22} {'Live Model':<26} {'Recommended':<26} {'Delta':>6}  Status")
    print("-" * 90)
    for r in all_results:
        if r["status"] == "skipped":
            continue
        delta_str = f"+{r['delta']:.2f}" if r["delta"] and r["delta"] > 0 else ("—" if r["delta"] == 0.0 else "?")
        status_label = {
            "ok": "OK",
            "upgrade": "UPGRADE AVAILABLE",
            "marginal": "marginal",
            "untracked": "untracked",
            "no_profile": "no profile",
        }.get(r["status"], r["status"])
        flag = " <--" if r["status"] == "upgrade" else ""
        print(f"  {r['character']:<20} {r['live_model']:<26} {r['recommended']:<26} {delta_str:>6}  {status_label}{flag}")
    print()
    if recs:
        print(f"{len(recs)} upgrade(s) found.")
    else:
        print("All positions on best-fit model.")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Check LLM model lineups for all agents")
    parser.add_argument("--dry-run", action="store_true", help="Print recommendations only, no Paperclip issues posted")
    parser.add_argument("--force",   action="store_true", help="Re-post issues even if already in state.json")
    parser.add_argument("--json",    action="store_true", help="Output JSON only")
    args = parser.parse_args()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    log.info("Lineup check started: %s", now_str)

    # Load matrix data and run algorithm
    data = load_data()
    matrix_updated = data.get("last_updated", "unknown")
    rankings = compute_rankings(data)

    # Get live agent configs from Paperclip
    try:
        live_models = get_live_models()
    except Exception as e:
        log.error("Could not reach Paperclip API: %s", e)
        print(f"ERROR: Could not reach Paperclip at {PAPERCLIP_BASE}: {e}")
        sys.exit(1)

    # Build recommendations
    recs, all_results = build_recommendations(data, rankings, live_models)

    # JSON output mode
    if args.json:
        print(json.dumps({
            "checked_at": now_str,
            "matrix_updated": matrix_updated,
            "upgrades": recs,
            "all": all_results,
        }, indent=2))
        return

    # Print summary table
    print_table(all_results, recs)

    # Log summary
    for r in all_results:
        log.info("  %-20s live=%-26s top=%-26s delta=%s status=%s",
                 r["character"], r["live_model"], r["recommended"],
                 r.get("delta"), r["status"])

    if not recs:
        log.info("No upgrades found.")
        _run_guidelines_audit(load_state(), args, save=not args.dry_run)
        return

    if args.dry_run:
        print("(dry-run: no issues posted)")
        _run_guidelines_audit(load_state(), args, save=False)
        return

    # Post issues
    state = load_state()
    posted = 0
    skipped = 0

    for rec in recs:
        pos_key = rec["pos_key"]
        prev = state.get(pos_key, {})

        # Skip if we already posted this exact recommendation
        if not args.force and prev.get("recommended_model") == rec["recommended"]:
            print(f"  [{pos_key}] already posted ({rec['recommended']}) -- skipping (use --force to re-post)")
            log.info("  Skipped %s -- already posted recommendation for %s", pos_key, rec["recommended"])
            skipped += 1
            continue

        resp = post_issue(rec, matrix_updated)
        if "id" in resp:
            issue_id = resp["id"]
            state[pos_key] = {
                "recommended_model": rec["recommended"],
                "posted_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "issue_id": issue_id,
            }
            print(f"  [{pos_key}] Issue posted: {issue_id[:8]} -- {rec['character']}: {rec['live_model']} -> {rec['recommended_name']}")
            log.info("  Posted issue %s for %s: %s -> %s", issue_id, pos_key, rec["live_model"], rec["recommended"])
            posted += 1
        else:
            print(f"  [{pos_key}] Failed to post issue: {resp.get('error')}")
            log.error("  Failed to post issue for %s: %s", pos_key, resp)

    save_state(state)
    print(f"\n{posted} issue(s) posted, {skipped} skipped (already posted).")
    log.info("Done: %d posted, %d skipped.", posted, skipped)

    _run_guidelines_audit(state, args, save=True)


def _run_guidelines_audit(state: dict, args, save: bool) -> None:
    """Weekly MODEL-PROMPTING-GUIDELINES drift audit.

    Always logs the audit summary. Posts a Paperclip issue if drift is
    detected AND fingerprint differs from the previously posted issue.
    """
    audit = audit_guidelines()
    print(
        f"\nGuidelines audit: {audit['filled']} filled, {audit['stubs']} stubs, "
        f"{audit['stale_count']} stale, {audit['broken_count']} broken-URL, "
        f"{len(audit['missing_for_models'])} missing-for-active-models."
    )
    log.info(
        "Guidelines audit: filled=%d stubs=%d stale=%d broken=%d missing=%d",
        audit["filled"], audit["stubs"], audit["stale_count"],
        audit["broken_count"], len(audit["missing_for_models"]),
    )

    drift = (
        audit["stale_count"] > 0
        or audit["broken_count"] > 0
        or len(audit["missing_for_models"]) > 0
    )
    if not drift:
        log.info("Guidelines audit: no drift, no issue posted.")
        return

    if args.dry_run:
        print("(dry-run: guidelines drift detected but no issue posted)")
        for h in audit["stale_sections"]:
            print(f"  STALE:   {h}")
        for h in audit["broken_sections"]:
            print(f"  BROKEN:  {h}")
        for m in audit["missing_for_models"]:
            print(f"  MISSING: {m['provider']} {m['name']}")
        return

    fingerprint = json.dumps({
        "stale": sorted(audit["stale_sections"]),
        "broken": sorted(audit["broken_sections"]),
        "missing": sorted(m["id"] for m in audit["missing_for_models"]),
    }, sort_keys=True)
    prev_fp = state.get("__guidelines_audit__", {}).get("fingerprint")
    if not args.force and prev_fp == fingerprint:
        print("  Guidelines drift unchanged since last post -- skipping (use --force to re-post)")
        log.info("Guidelines drift fingerprint unchanged, not re-posting.")
        return

    resp = post_guidelines_issue(audit)
    if "id" in resp:
        issue_id = resp["id"]
        state["__guidelines_audit__"] = {
            "fingerprint": fingerprint,
            "posted_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "issue_id": issue_id,
        }
        if save:
            save_state(state)
        print(f"  Guidelines drift issue posted: {issue_id[:8]}")
        log.info("Posted guidelines drift issue %s", issue_id)
    else:
        print(f"  Failed to post guidelines drift issue: {resp.get('error')}")
        log.error("Failed to post guidelines drift issue: %s", resp)


if __name__ == "__main__":
    main()
