r"""
auto_monitor.py -- Life Admin autonomous usage monitor

Runs on a schedule (via Windows Task Scheduler) to:
  1. Check Claude Max plan usage (via check_claude_usage.py)
  2. Auto-sub any positions that are near their limit
  3. Restore positions when limits reset
  4. Log all actions to D:\paperclip\monitor.log

Setup Task Scheduler (run this once as Admin):
  python auto_monitor.py --install-task

Manual run:
  python auto_monitor.py

To view recent log:
  python auto_monitor.py --log
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(r"D:\paperclip")
SCRIPTS_DIR = BASE_DIR / "scripts"
LOG_FILE = BASE_DIR / "monitor.log"
USAGE_FILE = BASE_DIR / "claude-usage.json"
STATE_FILE = BASE_DIR / "monitor-state.json"

# Positions using claude_local that should sub when Anthropic limits are near
CLAUDE_POSITIONS = ["CEO", "CTO", "COO", "Yoda", "ContentLead", "Spielberg", "Designer", "TravelAgent"]

WARN_PCT = 70    # Log warning
AUTO_SUB_PCT = 90  # Auto-sub to fallback1


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"subbed_positions": [], "last_sub_reason": None, "last_restore_check": None}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def run_usage_check() -> dict:
    """Run check_claude_usage.py and return parsed JSON."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "check_claude_usage.py"), "--json"],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        log(f"[!] Usage check failed: {result.stderr[:200]}")
        return {}
    try:
        # --json outputs JSON to stdout; find the JSON part
        text = result.stdout.strip()
        # Skip any "Checking..." prefix line
        json_start = text.find("{")
        return json.loads(text[json_start:]) if json_start >= 0 else {}
    except Exception as e:
        log(f"[!] Could not parse usage output: {e}")
        return {}


def run_position_manager(args: list) -> bool:
    """Run position_manager.py with given args. Returns True on success."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "position_manager.py")] + args,
        capture_output=True, text=True, cwd=str(BASE_DIR), timeout=60
    )
    output = result.stdout.strip()
    if output:
        for line in output.splitlines():
            log(f"  > {line}")
    return result.returncode == 0


def check_and_act():
    """Main monitor loop: check usage, sub/restore as needed."""
    log("--- Monitor run starting ---")
    state = load_state()

    data = run_usage_check()
    if not data:
        log("[!] No usage data retrieved. Skipping this cycle.")
        return

    if not data.get("parse_success"):
        err = data.get("error", "parse_success=False")
        log(f"[!] Usage page parse failed: {err}")
        return

    meters = data.get("meters", {})
    all_models_pct = meters.get("all_models", {}).get("pct", 0)
    session_pct = meters.get("session", {}).get("pct", 0)
    sonnet_pct = meters.get("sonnet", {}).get("pct", 0)

    log(f"Usage: all_models={all_models_pct}%  session={session_pct}%  sonnet={sonnet_pct}%")

    peak_pct = max(all_models_pct, session_pct)
    already_subbed = set(state.get("subbed_positions", []))

    if peak_pct >= AUTO_SUB_PCT:
        # Auto-sub any claude_local positions not already on fallback
        to_sub = [p for p in CLAUDE_POSITIONS if p not in already_subbed]
        if to_sub:
            log(f"[!] Usage at {peak_pct}% -- auto-subbing {len(to_sub)} positions to fallback1")
            for pos in to_sub:
                log(f"    Subbing {pos}...")
                if run_position_manager(["sub", pos, "fallback1"]):
                    already_subbed.add(pos)
                    log(f"    {pos} -> fallback1 OK")
                else:
                    log(f"    {pos} sub FAILED")
            state["subbed_positions"] = list(already_subbed)
            state["last_sub_reason"] = f"all_models={all_models_pct}%, session={session_pct}%"
            save_state(state)
        else:
            log(f"[~] Usage at {peak_pct}% -- all claude positions already on fallback")

    elif peak_pct >= WARN_PCT:
        log(f"[~] WARNING: usage at {peak_pct}% -- approaching threshold")

    else:
        # Usage is healthy -- restore any previously subbed positions
        if already_subbed:
            log(f"[OK] Usage healthy ({peak_pct}%) -- restoring {len(already_subbed)} positions to primary")
            for pos in list(already_subbed):
                log(f"    Restoring {pos}...")
                if run_position_manager(["restore", pos]):
                    already_subbed.discard(pos)
                    log(f"    {pos} -> primary OK")
                else:
                    log(f"    {pos} restore FAILED")
            state["subbed_positions"] = list(already_subbed)
            state["last_restore_check"] = datetime.now(timezone.utc).isoformat()
            save_state(state)
        else:
            log(f"[OK] Usage healthy ({peak_pct}%) -- all positions on primary")

    # Regenerate dashboard with latest state
    run_position_manager(["dashboard"])
    log("--- Monitor run complete ---\n")


def install_task():
    """Install a Windows Task Scheduler task to run this script every 2 hours."""
    python_exe = sys.executable
    script_path = str(SCRIPTS_DIR / "auto_monitor.py")

    # Task XML
    task_xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Life Admin usage monitor -- auto-subs AI agents when Claude limits are near</Description>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT2H</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2026-01-01T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <ExecutionTimeLimit>PT5M</ExecutionTimeLimit>
    <Enabled>true</Enabled>
  </Settings>
  <Actions>
    <Exec>
      <Command>{python_exe}</Command>
      <Arguments>"{script_path}"</Arguments>
      <WorkingDirectory>{str(BASE_DIR)}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""

    xml_path = BASE_DIR / "scripts" / "monitor-task.xml"
    xml_path.write_text(task_xml, encoding="utf-16")

    import subprocess
    result = subprocess.run(
        ["schtasks", "/Create", "/TN", "LifeAdmin-Monitor", "/XML", str(xml_path), "/F"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("[OK] Task 'LifeAdmin-Monitor' installed -- runs every 2 hours")
        print(f"     Logs: {LOG_FILE}")
    else:
        print(f"[!] Task install failed: {result.stderr}")
        print(f"    XML saved to {xml_path} -- install manually via Task Scheduler if needed")


def show_log(lines: int = 50):
    """Print the last N lines of the monitor log."""
    if not LOG_FILE.exists():
        print("No log file yet.")
        return
    all_lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    for line in all_lines[-lines:]:
        print(line)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Life Admin autonomous usage monitor")
    parser.add_argument("--install-task", action="store_true", help="Install Windows Task Scheduler job")
    parser.add_argument("--log", action="store_true", help="Print recent monitor log")
    parser.add_argument("--lines", type=int, default=50, help="Lines to show with --log")
    args = parser.parse_args()

    if args.install_task:
        install_task()
    elif args.log:
        show_log(args.lines)
    else:
        check_and_act()


if __name__ == "__main__":
    main()
