"""Weekly refresh of MODEL-RESEARCH.md and MODEL-PROMPTING-GUIDELINES.md with Claude Code.

Why: the Paperclip Researcher runs on the ollama_local adapter, which only sends
one chat request. It cannot search the web or edit files, so the weekly refresh
never happened (Greg's decision, 10 November 2026: run it with Claude Code on
the Max plan instead).

What it does:
1. Runs `claude -p` in D:\\paperclip with web search and edit rights on the two
   files only (plus the read-only guideline audit command).
2. Commits and pushes the two files if they changed.
3. Comments on this week's "Weekly model research" issue and marks it done.
   If the guideline audit is now clean, closes the open drift issue too.

Schedule: Task Scheduler "Paperclip Weekly Guidelines Refresh", Monday 10:00 AM,
via scripts/weekly-guidelines-refresh-hidden.vbs (after Model Lineup Monitor at 9:00).
Log:      D:\\paperclip\\scripts\\weekly-guidelines-refresh.log
Flags:    --dry-run (no Claude run, just checks), --no-push
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
REPO = SCRIPTS_DIR.parent
LOG_FILE = SCRIPTS_DIR / "weekly-guidelines-refresh.log"
FILES = ["MODEL-RESEARCH.md", "MODEL-PROMPTING-GUIDELINES.md"]
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
TIMEOUT_SECONDS = 45 * 60

sys.path.insert(0, str(SCRIPTS_DIR))
import check_model_lineups as lineups  # noqa: E402  (load_state, paperclip_*, audit_guidelines)

logging.basicConfig(filename=str(LOG_FILE), level=logging.INFO,
                    format="%(asctime)s %(levelname)-6s %(message)s",
                    force=True)  # check_model_lineups already configured logging on import
log = logging.getLogger("guidelines-refresh")

SYSTEM = (
    "You are the weekly model researcher for Greg's Paperclip repo. You keep two reference "
    "files accurate: MODEL-RESEARCH.md (models, pricing, capabilities) and "
    "MODEL-PROMPTING-GUIDELINES.md (per-model prompting rules from official provider docs). "
    "Use web search and the providers' own documentation; never guess a price, model id or "
    "API parameter. Write in Australian English and never use em dashes."
)

PROMPT = """Refresh the two model reference files for this week ({today}).

<context>
- Files you may edit: MODEL-RESEARCH.md and MODEL-PROMPTING-GUIDELINES.md (repo root). Do not edit anything else.
- The maintenance contract is the "Maintenance contract" section at the bottom of MODEL-PROMPTING-GUIDELINES.md, and positions/research/researcher/SOUL.md.
- Run `python scripts/update_llm_matrix.py --guidelines-stale` to see stale, broken or missing sections.
- Providers to cover: Anthropic, OpenAI, Google, xAI, Mistral, DeepSeek, Moonshot, MiniMax, Qwen, GLM.
</context>

<instructions>
1. Run the audit command above and note what it reports.
2. Search each provider's official docs and pricing pages for new models, retired models and price changes since the files were last updated.
3. Update MODEL-RESEARCH.md: add new models, mark retired ones as retired, correct prices, and update its "Last updated" line.
4. Update MODEL-PROMPTING-GUIDELINES.md: refresh every stale or broken section from the provider's current prompting docs, set its "Date captured", and add a section for every newly active model using the file's template.
5. Re-run the audit command to confirm the result.
6. Make only changes you have a source for. Leave a section alone rather than guess.
</instructions>

<output_format>
Finish with a short plain-language summary (under 200 words) for Greg: what changed in each file, which models were added or retired, the final audit line, and anything you could not verify.
</output_format>

Now do the refresh."""

ALLOWED = [
    "Read", "Grep", "Glob", "WebSearch", "WebFetch",
    "Edit(/MODEL-RESEARCH.md)", "Edit(/MODEL-PROMPTING-GUIDELINES.md)",
    "Bash(python scripts/update_llm_matrix.py --guidelines-stale)",
]
DENIED = ["Read(**/.env*)", "Read(**/.secrets/**)", "Read(**/*secret*)", "Read(**/*credential*)",
          "Grep(**/.env*)", "Grep(**/.secrets/**)"]


def in_blackout(now: datetime) -> bool:
    """Club Wyndham midnight blackout (global rules Part 24): 23:29 to 00:10."""
    return (now.hour == 23 and now.minute >= 29) or (now.hour == 0 and now.minute <= 10)


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", creationflags=NO_WINDOW)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {out.stderr.strip()[:300]}")
    return out.stdout


def run_claude() -> dict:
    cmd = ["claude", "-p", "--tools", "Read,Grep,Glob,Edit,Bash,WebSearch,WebFetch",
           "--allowedTools", *ALLOWED, "--disallowedTools", *DENIED,
           "--permission-mode", "dontAsk", "--strict-mcp-config", "--no-session-persistence",
           "--output-format", "json", "--max-turns", "120", "--model", "opus",
           "--fallback-model", "sonnet", "--append-system-prompt", SYSTEM]
    out = subprocess.run(cmd, input=PROMPT.format(today=datetime.now().strftime("%d %B %Y").lstrip("0")),
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         timeout=TIMEOUT_SECONDS, cwd=REPO, creationflags=NO_WINDOW)
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude exit {out.returncode}: {(out.stderr or out.stdout)[:300]}")
    if data.get("is_error"):
        raise RuntimeError(f"claude returned {data.get('subtype')}: {str(data.get('result'))[:300]}")
    return data


def close_issue(issue_id: str, comment: str) -> None:
    lineups.paperclip_post(f"/api/issues/{issue_id}/comments", {"body": comment})
    import urllib.request
    req = urllib.request.Request(f"{lineups.PAPERCLIP_BASE}/api/issues/{issue_id}",
                                 data=json.dumps({"status": "done"}).encode(),
                                 headers={"Content-Type": "application/json"}, method="PATCH")
    urllib.request.urlopen(req, timeout=15).read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    if in_blackout(datetime.now()):
        return 0
    log.info("Refresh started (dry_run=%s)", args.dry_run)

    dirty = [f for f in FILES if git("status", "--porcelain", "--", f).strip()]
    if dirty:
        log.error("Uncommitted changes already in %s, not running", dirty)
        return 1
    if args.dry_run:
        log.info("Dry run: checks passed, Claude not run")
        return 0

    before = set(git("status", "--porcelain").splitlines())
    data = run_claude()
    summary = (data.get("result") or "").strip()
    log.info("Claude finished: turns=%s cost_usd=%s", data.get("num_turns"), data.get("total_cost_usd"))

    after = git("status", "--porcelain").splitlines()
    changed = [l for l in after if l[3:].strip() in FILES]
    stray = [l for l in after if l not in before and l[3:].strip() not in FILES]
    if stray:
        log.warning("Files outside the two references changed (not committed): %s", stray)
    commit = None
    if changed:
        git("add", "--", *FILES)
        git("commit", "-m", f"docs(models): weekly model research refresh {datetime.now():%Y-%m-%d}\n\n"
            "Co-Authored-By: Claude Code (scheduled) <noreply@anthropic.com>")
        commit = git("rev-parse", "--short", "HEAD").strip()
        if not args.no_push:
            git("push", "origin", "HEAD")
        log.info("Committed %s", commit)
    else:
        log.info("No changes to the two files")

    audit = lineups.audit_guidelines()
    audit_line = (f"filled={audit['filled']} stubs={audit['stubs']} stale={audit['stale_count']} "
                  f"broken={len(audit['broken_sections'])} missing={len(audit['missing_for_models'])}")
    log.info("Audit after refresh: %s", audit_line)

    state = lineups.load_state()
    note = (f"Weekly refresh by Claude Code ({'commit ' + commit if commit else 'no file changes'}).\n"
            f"Guideline audit: {audit_line}\n\n{summary}")
    weekly = state.get("__weekly_research__", {})
    if weekly.get("issue_id") and weekly.get("week") == datetime.now().strftime("%G-W%V"):
        close_issue(weekly["issue_id"], note)
        log.info("Closed weekly issue %s", weekly["issue_id"])
    drift = state.get("__guidelines_audit__", {})
    if drift.get("issue_id") and not (audit["stale_sections"] or audit["broken_sections"]
                                      or audit["missing_for_models"]):
        close_issue(drift["issue_id"], note)
        log.info("Closed drift issue %s", drift["issue_id"])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # pythonw has no stderr, so the log is the only record
        log.exception("Refresh failed: %s", e)
        sys.exit(1)
