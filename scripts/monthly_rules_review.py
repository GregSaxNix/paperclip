"""Monthly review of Greg's assistant rules against current model guidance.

Why: Greg asked (18 November 2026) for a monthly check of the rules his assistants
load, to see whether each rule still suits how the models he uses actually behave.
The weekly refresh keeps MODEL-PROMPTING-GUIDELINES.md current; this job ties that
guidance back to the rules themselves.

What it does:
1. Builds a manifest of the rule files: the canonical global rules
   (D:\\assistant-os\\canonical\\core\\rules, the source of ~/.claude/CLAUDE.md and
   ~/.codex/AGENTS.md), the ChatGPT/Grok bootstrap, the global Cursor rules, and
   the CLAUDE.md / AGENTS.md / PROJECT_RULES.md / .cursor/rules files of every
   project registered as trusted-cloud. Local-only projects (My Day, Care
   Planner, house sale, Lana) are left out on purpose (global rules Part 27).
2. Runs `claude -p` with read-only tools, web search, and write access to the
   one report file only. It never edits a rule. The report only recommends.
3. Records the run with `aos.py record paperclip` and adds a "read the report"
   item to D:\\assistant-os\\hot\\open-items\\paperclip.md so the briefing shows it.

Schedule: Task Scheduler "Paperclip Monthly Rules Review", first Tuesday of the
month 10:00 AM (the day after the Monday guidelines refresh), via
scripts/monthly-rules-review-hidden.vbs.
Report:   D:\\paperclip\\reports\\rules-review\\YYYY-MM-rules-review.md (not committed)
Log:      D:\\paperclip\\scripts\\monthly-rules-review.log
Flags:    --dry-run (write the manifest only, no Claude run), --no-record
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

SCRIPTS_DIR = Path(__file__).parent
REPO = SCRIPTS_DIR.parent
REPORT_DIR = REPO / "reports" / "rules-review"
LOG_FILE = SCRIPTS_DIR / "monthly-rules-review.log"
AOS = Path(r"D:\assistant-os")
HOME = Path.home()
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
TIMEOUT_SECONDS = 60 * 60
PROJECT_RULE_FILES = ("CLAUDE.md", "AGENTS.md", "PROJECT_RULES.md")

logging.basicConfig(filename=str(LOG_FILE), level=logging.INFO,
                    format="%(asctime)s %(levelname)-6s %(message)s")
log = logging.getLogger("rules-review")

SYSTEM = (
    "You are the monthly rules reviewer for Greg Sax. Greg is a recruitment professional and "
    "vibe coder, not a developer. You assess the instruction files his AI assistants load and "
    "recommend which rules to keep, change, merge, move or remove so they suit how current models "
    "actually behave. You only write the report file you are given. You never edit a rule file. "
    "Base every recommendation on a source (official provider docs, or the repo's "
    "MODEL-PROMPTING-GUIDELINES.md) and say when something is your judgement. Write in Australian "
    "English, plain words, dates as '18 November 2026', and never use em dashes."
)

PROMPT = """Review Greg's assistant rules for {month} and write the report to {report}.

<context>
- The manifest of rule files, with sizes, is at {manifest}. Read every file it lists.
- The global rules are edited in D:\\assistant-os\\canonical\\core\\rules (one file per Part) and compiled into ~/.claude/CLAUDE.md and ~/.codex/AGENTS.md, so every global rule loads into every Claude Code and Codex session. Recommend changes against the canonical file names.
- The ChatGPT and Grok assistants get a short bootstrap (listed in the manifest). ChatGPT custom instructions, ChatGPT memory and ChatGPT project instructions live in Greg's online account, so you cannot read them; say what Greg would need to paste in for them to be reviewed.
- Which models Greg uses: read D:\\paperclip\\LLM-MATRIX.md and the "Default provider hierarchy" in the global rules. In day-to-day work he uses Claude Code (Opus and Sonnet on the Max plan), Codex (OpenAI GPT models), Cursor, and the ChatGPT app.
- Model prompting guidance kept current weekly: D:\\paperclip\\MODEL-PROMPTING-GUIDELINES.md (read the Anthropic and OpenAI sections).
- Greg's pasted ChatGPT and Grok settings, if he saved them this month: {chatgpt}. Review them like the other rules; if the file is missing, say so.
- Last month's report, if any: {previous}. Do not repeat a recommendation Greg has already turned down there unless the evidence changed; say what changed since then.
</context>

<instructions>
1. Read the manifest, then every rule file in it, and the guidance files above.
2. Check the current official guidance with web search and fetch, and note the date of each source:
   - Anthropic: Claude Code memory and CLAUDE.md docs, Claude Code best practices, and the prompting best practices for the current Claude models (what newer models do by default, so rules that only repeat default behaviour can go; how long CLAUDE.md should be; what belongs in skills, hooks, slash commands or project files instead).
   - OpenAI: Codex AGENTS.md docs (including any size limit on what Codex loads), the GPT prompting guide for the GPT model Codex uses, and ChatGPT custom instructions, memory and projects help pages.
   - Cursor: the Cursor rules docs (.mdc rules, alwaysApply, globs, AGENTS.md support, size advice).
3. For each rule (each Part of the global rules, then each Cursor and project rule), decide one action: Keep, Change, Shorten, Merge (with which rule), Move (to a skill, hook, project file or the rules library), or Remove. Most rules should be Keep; only recommend a change you can justify.
4. Look in particular for: rules that repeat what the model already does by default; overlapping or contradicting rules (including between Claude, Cursor and Codex copies); rules written for an older model's quirks; rules that only fire in rare situations but load in every session; heavy emphasis (IMPORTANT, MUST, ALWAYS in capitals) that current Claude models now over-apply; total size against each tool's advice or limit; stale facts (dates, model names, file paths that no longer exist, which you can check with Glob).
5. Never recommend weakening a safety, privacy, security, secrets or approval rule just to save space. You may suggest moving it somewhere it still always applies.
6. Write the report. Write nothing else.
</instructions>

<output_format>
Markdown, in this order, with one flat numbered series across the whole report so Greg can reply by number:
1. "## Summary": three to five sentences: the overall verdict, the total size of what loads in every session (in KB and approximate tokens) against the advice, and the top three changes.
2. "## Changes recommended": a table with columns: No., Where (canonical file or project file), Rule (short name), Action, Why (with source), Suggested wording or destination. Recommended changes first, highest value first.
3. "## Rules to keep as they are": a short list grouped by file; one line each is enough.
4. "## Cursor": what Cursor supports, what Greg's Cursor rules look like, and the recommendations for them.
5. "## Codex and ChatGPT": what Codex AGENTS.md and ChatGPT custom instructions, memory and projects support, whether Greg's rules there fit (including any size limit), and what Greg would need to paste in for the next review to cover ChatGPT.
6. "## What changed since last month": or "First run" if there is no previous report.
7. "## Sources": each with its title, link and the date you read it.
Keep the report under 2,500 words. Plain words; technical terms only where needed, explained once.
</output_format>

Now do the review."""

ALLOWED = ["Read", "Grep", "Glob", "WebSearch", "WebFetch"]
DENIED = ["Read(**/.env*)", "Read(**/.secrets/**)", "Read(**/*secret*)", "Read(**/*credential*)",
          "Read(**/auth.json)", "Read(**/*.key)", "Read(**/*.pem)",
          "Grep(**/.env*)", "Grep(**/.secrets/**)"]


def in_blackout(now: datetime) -> bool:
    """Club Wyndham midnight blackout (global rules Part 24): 23:29 to 00:10."""
    return (now.hour == 23 and now.minute >= 29) or (now.hour == 0 and now.minute <= 10)


def trusted_project_folders() -> list[Path]:
    data = yaml.safe_load((AOS / "registry" / "projects.yaml").read_text(encoding="utf-8")) or {}
    folders = []
    for p in data.get("projects", []):
        if p.get("visibility") == "local-only" or not p.get("folder"):
            continue
        folder = Path(p["folder"])
        if folder.is_dir() and folder not in folders:
            folders.append(folder)
    return folders


def build_manifest() -> list[tuple[str, Path]]:
    items: list[tuple[str, Path]] = []
    items += [("Global rules (canonical source)", f)
              for f in sorted((AOS / "canonical" / "core" / "rules").glob("*.md"))]
    bootstrap = AOS / "exports" / "global" / "bootstrap" / "BOOTSTRAP.md"
    if bootstrap.exists():
        items.append(("ChatGPT and Grok bootstrap", bootstrap))
    items += [("Global Cursor rules", f) for f in sorted((HOME / ".cursor" / "rules").glob("*.mdc"))]
    for folder in trusted_project_folders():
        for name in PROJECT_RULE_FILES:
            if (folder / name).is_file():
                items.append((f"Project: {folder.name}", folder / name))
        items += [(f"Project: {folder.name} (Cursor)", f)
                  for f in sorted((folder / ".cursor" / "rules").glob("*.mdc"))]
    return items


def write_manifest(path: Path, items: list[tuple[str, Path]]) -> None:
    installed = [HOME / ".claude" / "CLAUDE.md", HOME / ".codex" / "AGENTS.md"]
    lines = [f"# Rules review manifest, {datetime.now():%d %B %Y}".replace(" 0", " "), "",
             "Installed global files (generated from the canonical rules; sizes only, do not review twice):"]
    lines += [f"- {f} ({f.stat().st_size:,} bytes)" for f in installed if f.exists()]
    lines += ["", "Files to review:", ""]
    group = None
    for label, f in items:
        if label != group:
            lines += ["", f"## {label}"]
            group = label
        lines.append(f"- {f} ({f.stat().st_size:,} bytes)")
    lines += ["", "Left out on purpose: local-only projects (My Day, Care Planner, house sale, Lana), "
              "per global rules Part 27."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_claude(prompt: str, add_dirs: list[str]) -> dict:
    # Write is governed by Edit(...) permission rules; this one path only.
    report_rule = "Edit(/reports/rules-review/*-rules-review.md)"
    cmd = ["claude", "-p", "--tools", "Read,Grep,Glob,Write,WebSearch,WebFetch",
           "--allowedTools", *ALLOWED, report_rule, "--disallowedTools", *DENIED,
           "--add-dir", *add_dirs,
           "--permission-mode", "dontAsk", "--strict-mcp-config", "--no-session-persistence",
           "--output-format", "json", "--max-turns", "150", "--model", "opus",
           "--fallback-model", "sonnet", "--append-system-prompt", SYSTEM]
    out = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=TIMEOUT_SECONDS, cwd=REPO, creationflags=NO_WINDOW)
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude exit {out.returncode}: {(out.stderr or out.stdout)[:300]}")
    if data.get("is_error"):
        raise RuntimeError(f"claude returned {data.get('subtype')}: {str(data.get('result'))[:300]}")
    return data


def add_open_item(report: Path, month_label: str) -> None:
    items_file = AOS / "hot" / "open-items" / "paperclip.md"
    marker = f"rules-review-{report.stem[:7]}"
    text = items_file.read_text(encoding="utf-8")
    if marker in text:
        return
    entry = (f"\n- **[greg, P2, review]** **Read the {month_label} rules review report** "
             f"<!-- {marker} -->. Monthly check of the Claude, Cursor and Codex rules against current "
             f"model guidance: [{report.name}]({report}). It only recommends; reply by number with "
             f"which changes to make, and an assistant edits the canonical rules.\n"
             f"  **Trigger:** now (report written {datetime.now():%d %B %Y}).\n"
             f"  **Why:** the scheduled job never edits rules itself.\n")
    items_file.write_text(text.rstrip("\n") + "\n" + entry, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-record", action="store_true")
    args = ap.parse_args()

    now = datetime.now()
    if in_blackout(now):
        return 0
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    month_label = now.strftime("%B %Y")
    report = REPORT_DIR / f"{now:%Y-%m}-rules-review.md"
    manifest = REPORT_DIR / f"{now:%Y-%m}-manifest.md"
    previous = sorted(p for p in REPORT_DIR.glob("*-rules-review.md") if p != report)

    items = build_manifest()
    write_manifest(manifest, items)
    log.info("Review started (dry_run=%s): %d files in manifest", args.dry_run, len(items))
    if args.dry_run:
        return 0

    add_dirs = sorted({str(AOS), str(HOME / ".cursor"), str(HOME / ".codex"),
                       *(str(f) for f in trusted_project_folders())})
    prompt = PROMPT.format(month=month_label, report=report, manifest=manifest,
                           previous=previous[-1] if previous else "none (first run)",
                           chatgpt=REPORT_DIR / "inputs" / f"{now:%Y-%m}-chatgpt.md")
    data = run_claude(prompt, add_dirs)
    log.info("Claude finished: turns=%s cost_usd=%s", data.get("num_turns"), data.get("total_cost_usd"))
    if not report.exists():
        log.error("Denied tool calls: %s", data.get("permission_denials"))
        raise RuntimeError(f"Claude finished but no report was written: {str(data.get('result'))[-300:]}")

    if not args.no_record:
        subprocess.run([sys.executable.replace("pythonw", "python"), str(AOS / "tooling" / "aos.py"),
                        "record", "paperclip",
                        f"Monthly rules review for {month_label} written (recommendations only, no rules edited)",
                        "--evidence", str(report), "--key", f"rules-review-{now:%Y-%m}"],
                       capture_output=True, text=True, creationflags=NO_WINDOW, check=True)
        add_open_item(report, month_label)
    log.info("Report written: %s", report)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # pythonw has no stderr, so the log is the only record
        log.exception("Review failed: %s", e)
        sys.exit(1)
