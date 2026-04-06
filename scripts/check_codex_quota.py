r"""
check_codex_quota.py -- OpenAI Codex (ChatGPT) quota monitor

Uses a persistent Chrome profile (real Chrome binary) to authenticate and
scrape the Codex usage page. The --setup step opens a real Chrome window
where Google/OpenAI OAuth works normally. Subsequent runs are off-screen.

Usage:
    python check_codex_quota.py --setup      # First-time: log in via Chrome window
    python check_codex_quota.py              # Check and print status
    python check_codex_quota.py --json       # Print JSON only (for scripting)
    python check_codex_quota.py --sub-if-needed  # Print sub commands if near limit

Requirements:
    pip install playwright
    playwright install chrome
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(r"D:\paperclip")
OUTPUT_FILE = BASE_DIR / "codex-quota.json"
PROFILE_DIR = BASE_DIR / "scripts" / ".codex-browser-profile"

USAGE_URLS = [
    "https://chatgpt.com/codex",
    "https://chatgpt.com/settings",
    "https://platform.openai.com/usage",
]

WARN_THRESHOLD = 0.70
PAUSE_THRESHOLD = 0.90


def launch_context(p, setup_mode: bool = False):
    """
    Launch a persistent Chrome context.
    setup_mode=True  -> visible window for login
    setup_mode=False -> off-screen window (invisible but not headless, bypasses Cloudflare)
    """
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    base_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    if not setup_mode:
        base_args += ["--window-position=-10000,-10000", "--window-size=1280,720"]

    kwargs = dict(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        channel="chrome",
        args=base_args,
        ignore_default_args=["--enable-automation"],
    )
    try:
        return p.chromium.launch_persistent_context(**kwargs)
    except Exception:
        kwargs.pop("channel", None)
        return p.chromium.launch_persistent_context(**kwargs)


def setup_auth():
    """Open Chrome for ChatGPT/OpenAI login. Session saved to profile dir."""
    from playwright.sync_api import sync_playwright

    print("Opening Chrome for chatgpt.com login...")
    print()
    print("  1. Log in with your OpenAI / Google account as normal.")
    print("     (Google OAuth works fine -- automation flag is suppressed)")
    print("  2. Wait until you can see the ChatGPT interface.")
    print("  3. Come back here and press ENTER.")
    print()

    with sync_playwright() as p:
        ctx = launch_context(p, setup_mode=True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://chatgpt.com/login")

        input(">> Press ENTER once you are fully logged in: ")

        if "login" in page.url or "auth" in page.url:
            print("[!] Still looks like the login page.")
            input("   Complete the login then press ENTER again: ")

        ctx.close()

    print(f"[OK] Session saved to {PROFILE_DIR}")
    print("[OK] Setup complete. Run without --setup to check quota.")


def scrape_codex_quota():
    """Load chatgpt.com/codex using the saved profile and parse quota data."""
    from playwright.sync_api import sync_playwright

    if not PROFILE_DIR.exists() or not any(PROFILE_DIR.iterdir()):
        return _error_result("No saved session found. Run --setup first.")

    result = {
        "last_checked": datetime.now(timezone.utc).isoformat(),
        "reset_date": None,
        "tasks_used": None,
        "tasks_limit": None,
        "pct_used": None,
        "quota_ok": True,
        "parse_success": False,
        "source_url": None,
        "raw_snippet": "",
    }

    with sync_playwright() as p:
        ctx = launch_context(p, setup_mode=False)
        page = ctx.new_page()

        best_content = ""
        best_url = None

        for url in USAGE_URLS:
            try:
                page.goto(url, wait_until="load", timeout=20000)

                if "login" in page.url or "auth" in page.url:
                    ctx.close()
                    result["error"] = "Redirected to login -- session expired. Run --setup again."
                    return result

                page.wait_for_timeout(3000)
                content = page.content()

                if any(kw in content.lower() for kw in ["quota", "tasks", "codex", "limit", "remaining"]):
                    best_content = content
                    best_url = url
                    break
            except Exception:
                continue

        ctx.close()

    if not best_content:
        result["error"] = "No quota data found on any of the checked URLs."
        return result

    result["source_url"] = best_url
    return parse_codex_html(best_content, result)


def _error_result(message: str) -> dict:
    return {
        "last_checked": datetime.now(timezone.utc).isoformat(),
        "reset_date": None,
        "tasks_used": None,
        "tasks_limit": None,
        "pct_used": None,
        "quota_ok": True,
        "parse_success": False,
        "error": message,
        "raw_snippet": "",
    }


def parse_codex_html(html: str, result: dict) -> dict:
    lower = html.lower()
    for kw in ["quota", "tasks", "codex", "remaining"]:
        idx = lower.find(kw)
        if idx >= 0:
            result["raw_snippet"] = html[max(0, idx - 100):idx + 500]
            break

    patterns = [
        r"(\d+)\s+of\s+(\d+)\s+tasks?",
        r"(\d+)\s*/\s*(\d+)\s+tasks?",
        r'"tasksUsed":\s*(\d+)[^}]*"tasksLimit":\s*(\d+)',
        r'"used":\s*(\d+)[^}]*"limit":\s*(\d+)',
        r"(\d+)\s+tasks?\s+(?:used|remaining)",
    ]

    for pat in patterns:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            used = int(m.group(1))
            limit = int(m.group(2)) if len(m.groups()) >= 2 else None
            if "remaining" in pat and limit:
                used = limit - used
            result["tasks_used"] = used
            result["tasks_limit"] = limit
            if limit and limit > 0:
                result["pct_used"] = round(used / limit, 3)
                result["quota_ok"] = result["pct_used"] < PAUSE_THRESHOLD
            result["parse_success"] = True
            break

    reset_m = re.search(
        r'reset[s]?\s+(?:on\s+)?([A-Z][a-z]+\s+\d+|\d{1,2}/\d{1,2}/\d{4})',
        html, re.IGNORECASE
    )
    if reset_m:
        result["reset_date"] = reset_m.group(1)

    if not result["parse_success"]:
        for block in re.findall(r'\{[^{}]{20,500}\}', html):
            try:
                d = json.loads(block)
                if "tasksUsed" in d or "tasks_used" in d:
                    used = d.get("tasksUsed") or d.get("tasks_used")
                    limit = d.get("tasksLimit") or d.get("tasks_limit")
                    result["tasks_used"] = used
                    result["tasks_limit"] = limit
                    if limit and limit > 0:
                        result["pct_used"] = round(used / limit, 3)
                        result["quota_ok"] = result["pct_used"] < PAUSE_THRESHOLD
                    result["parse_success"] = True
                    break
            except Exception:
                continue

    return result


def print_status(data: dict):
    print()
    print("=== OpenAI Codex Quota ===")
    print(f"Checked: {data['last_checked']}")
    if data.get("reset_date"):
        print(f"Resets:  {data['reset_date']}")
    if data.get("source_url"):
        print(f"Source:  {data['source_url']}")
    print()

    if data.get("error"):
        print(f"[!] {data['error']}")
        return

    if not data.get("parse_success"):
        print("[!] Could not parse quota data from page.")
        print("    Page structure may have changed.")
        if data.get("raw_snippet"):
            print("\n    Debug snippet:")
            print("   ", data["raw_snippet"][:400])
        return

    used = data.get("tasks_used", "?")
    limit = data.get("tasks_limit", "?")
    pct = data.get("pct_used") or 0
    bar_filled = int(pct * 20)
    bar = "#" * bar_filled + "-" * (20 - bar_filled)

    status = "OK"
    if pct >= PAUSE_THRESHOLD:
        status = "[!] NEAR LIMIT - use fallback"
    elif pct >= WARN_THRESHOLD:
        status = "[~] WARNING"

    print(f"  CODEX      [{bar}] {int(pct * 100):3d}%  ({used}/{limit} tasks)  {status}")
    print()
    print(f"  quota_ok: {data.get('quota_ok', True)}")


def print_sub_recommendations(data: dict):
    if not data.get("parse_success"):
        print("\n[?] Could not determine quota status -- no recommendation.")
        return
    if not data.get("quota_ok", True):
        print("\n[!] Recommended substitution:")
        print("    python position_manager.py sub Engineer fallback1")
        print("    python position_manager.py sub CouncilTech fallback1")
    else:
        print("\n[OK] Engineer and CouncilTech can stay on Codex primary.")


def main():
    parser = argparse.ArgumentParser(description="Check OpenAI Codex task quota")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument("--setup", action="store_true", help="First-time: open Chrome to log in")
    parser.add_argument("--sub-if-needed", action="store_true", help="Print sub commands if near limit")
    args = parser.parse_args()

    if args.setup:
        setup_auth()
        return

    print("Checking Codex quota...")
    data = scrape_codex_quota()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print_status(data)

    if args.sub_if_needed:
        print_sub_recommendations(data)

    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
