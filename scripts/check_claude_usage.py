r"""
check_claude_usage.py -- Claude (Anthropic Max plan) usage monitor

Uses a persistent Chrome profile (real Chrome binary) to authenticate and
scrape https://claude.ai/settings/usage. The --setup step opens a real Chrome
window where Google OAuth works normally. Subsequent runs are headless.

Usage:
    python check_claude_usage.py --setup      # First-time: log in via Chrome window
    python check_claude_usage.py              # Check and print status
    python check_claude_usage.py --json       # Print JSON only (for scripting)
    python check_claude_usage.py --sub-if-needed  # Print sub commands if near limit

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
OUTPUT_FILE = BASE_DIR / "claude-usage.json"
PROFILE_DIR = BASE_DIR / "scripts" / ".claude-browser-profile"
USAGE_URL = "https://claude.ai/settings/usage"

WARN_THRESHOLD = 0.70
PAUSE_THRESHOLD = 0.90


def launch_context(p, setup_mode: bool = False):
    """
    Launch a persistent Chrome context.

    setup_mode=True  → visible window, normal position (user logs in)
    setup_mode=False → window positioned off-screen (-10000,-10000) so it's
                       invisible but NOT headless — bypasses Cloudflare detection
    """
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    base_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    if not setup_mode:
        # Off-screen: invisible to user but not headless (bypasses Cloudflare)
        base_args += [
            "--window-position=-10000,-10000",
            "--window-size=1280,720",
        ]
    kwargs = dict(
        user_data_dir=str(PROFILE_DIR),
        headless=False,  # Never headless — Cloudflare blocks headless Chrome
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
    """Open a real Chrome window for login. Session is saved to the profile dir."""
    from playwright.sync_api import sync_playwright

    print("Opening Chrome for claude.ai login...")
    print()
    print("  1. Log in with Google (or email) as you normally would.")
    print("     (Google OAuth will work fine -- automation flag is suppressed)")
    print("  2. Wait until you can see your Claude conversations.")
    print("  3. Come back here and press ENTER.")
    print()

    with sync_playwright() as p:
        ctx = launch_context(p, setup_mode=True)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://claude.ai/login")

        input(">> Press ENTER once you are fully logged in: ")

        if "login" in page.url or "auth" in page.url:
            print("[!] Still looks like the login page.")
            input("   Complete the login then press ENTER again: ")

        ctx.close()  # Persists the session

    print(f"[OK] Session saved to {PROFILE_DIR}")
    print("[OK] Setup complete. Run without --setup to check usage.")


def scrape_usage():
    """Navigate to usage page using the saved profile and parse the data."""
    from playwright.sync_api import sync_playwright
    from playwright_stealth import Stealth

    if not PROFILE_DIR.exists() or not any(PROFILE_DIR.iterdir()):
        return _error_result("No saved session found. Run --setup first.")

    with sync_playwright() as p:
        ctx = launch_context(p, setup_mode=False)
        page = ctx.new_page()

        try:
            page.goto(USAGE_URL, wait_until="load", timeout=30000)
        except Exception as e:
            ctx.close()
            return _error_result(f"Navigation failed: {e}")

        if "login" in page.url or "auth" in page.url:
            ctx.close()
            return _error_result(
                "Session expired. Run --setup again to re-authenticate."
            )

        try:
            page.wait_for_selector("h1, h2, main", timeout=10000)
        except Exception:
            pass
        page.wait_for_timeout(3000)

        content = page.content()
        ctx.close()

    return parse_usage_html(content)


def _error_result(message: str) -> dict:
    return {
        "last_checked": datetime.now(timezone.utc).isoformat(),
        "reset_date": None,
        "models": {},
        "should_use_opus": True,
        "parse_success": False,
        "error": message,
        "raw_snippet": "",
    }


def parse_usage_html(html: str) -> dict:
    """
    Parse claude.ai/settings/usage page.

    Actual page structure (Max plan, verified 2026-04-06):
      - "Current session" progressbar (rate limit per session, resets hourly)
      - "All models" progressbar (weekly usage across all models)
      - "Sonnet only" progressbar (separate weekly Sonnet limit)

    Each uses: role="progressbar" aria-valuenow="<pct 0-100>"
    Labels appear in the ~500 chars of plain text before each bar.
    """
    result = {
        "last_checked": datetime.now(timezone.utc).isoformat(),
        "meters": {},          # keyed by label: {pct, reset_text}
        "should_use_opus": True,
        "parse_success": False,
        "raw_snippet": "",
    }

    # Map label keywords → canonical key
    label_map = [
        (["current session"], "session"),
        (["all models"], "all_models"),
        (["sonnet only", "sonnet"], "sonnet"),
        (["opus"], "opus"),
        (["haiku"], "haiku"),
    ]

    # Find all progressbars
    pb_pattern = re.compile(
        r'role="progressbar"\s[^>]*aria-valuenow="(\d+)"', re.IGNORECASE
    )
    strip_tags = re.compile(r'<[^>]+>')
    collapse_ws = re.compile(r'\s+')

    hits = list(pb_pattern.finditer(html))
    if not hits:
        result["raw_snippet"] = html[html.lower().find("usage"):html.lower().find("usage") + 500] if "usage" in html.lower() else html[:500]
        return result

    result["raw_snippet"] = html[max(0, hits[0].start() - 200):hits[0].start() + 200]

    for m in hits:
        pct = int(m.group(1))
        # Get plain text from 1500 chars before the bar (SVG icons can eat the budget)
        ctx_html = html[max(0, m.start() - 1500):m.start()]
        ctx_text = collapse_ws.sub(" ", strip_tags.sub(" ", ctx_html)).lower().strip()

        # Identify label
        label = "unknown"
        for keywords, key in label_map:
            if any(kw in ctx_text[-300:] for kw in keywords):
                label = key
                break

        # Extract reset text ("Resets in X hr", "Resets Sat 9:00 AM", etc.)
        reset_match = re.search(
            r'resets?\s+(in\s+[\w\s:]+|[A-Z][a-z]+\s+[\d:]+\s*[AP]M|[A-Z][a-z]+)',
            ctx_text[-200:], re.IGNORECASE
        )
        reset_text = reset_match.group(0).strip() if reset_match else None

        result["meters"][label] = {
            "pct": pct,
            "reset_text": reset_text,
        }

    result["parse_success"] = len(result["meters"]) > 0

    # should_use_opus: flag if all_models or session meter is near limit
    all_models_pct = result["meters"].get("all_models", {}).get("pct", 0)
    session_pct = result["meters"].get("session", {}).get("pct", 0)
    result["should_use_opus"] = max(all_models_pct, session_pct) < (PAUSE_THRESHOLD * 100)

    return result


def print_status(data: dict):
    print()
    print("=== Claude Max Plan Usage ===")
    print(f"Checked: {data['last_checked']}")
    print()

    if data.get("error"):
        print(f"[!] {data['error']}")
        return

    if not data.get("parse_success"):
        print("[!] Could not parse usage data from page.")
        print("    Page structure may have changed.")
        if data.get("raw_snippet"):
            print()
            print("    Debug snippet:")
            print("   ", data["raw_snippet"][:400])
        return

    meters = data.get("meters", {})
    if not meters:
        print("[!] No usage meters found.")
        return

    label_display = {
        "session":    "Session  ",
        "all_models": "All models",
        "sonnet":     "Sonnet   ",
        "opus":       "Opus     ",
        "haiku":      "Haiku    ",
        "unknown":    "Unknown  ",
    }

    for key, info in meters.items():
        pct = info.get("pct", 0)
        reset = info.get("reset_text", "")
        bar_filled = int(pct / 5)   # 20 chars = 100%
        bar = "#" * bar_filled + "-" * (20 - bar_filled)
        status = "OK"
        if pct >= PAUSE_THRESHOLD * 100:
            status = "[!] NEAR LIMIT"
        elif pct >= WARN_THRESHOLD * 100:
            status = "[~] WARNING"
        label = label_display.get(key, key.ljust(9))
        reset_str = f"  ({reset})" if reset else ""
        print(f"  {label}  [{bar}] {pct:3d}%  {status}{reset_str}")

    print()
    print(f"  should_use_opus: {data.get('should_use_opus', True)}")
    if not data.get("should_use_opus", True):
        print("  --> Recommend: sub CEO/CTO/Yoda to fallback1 (Grok-3)")


def print_sub_recommendations(data: dict):
    meters = data.get("meters", {})
    claude_positions = ["CEO", "CTO", "COO", "Yoda", "ContentLead", "Spielberg", "Designer", "TravelAgent"]
    needing_fallback = []

    all_models_pct = meters.get("all_models", {}).get("pct", 0)
    session_pct = meters.get("session", {}).get("pct", 0)
    threshold = PAUSE_THRESHOLD * 100

    if all_models_pct >= threshold or session_pct >= threshold:
        needing_fallback.extend(claude_positions)

    if needing_fallback:
        print("\n[!] Recommended substitutions (claude_local near limit):")
        for pos in needing_fallback:
            print(f"    python position_manager.py sub {pos} fallback1")
    else:
        print("\n[OK] All positions can stay on primary models.")


def main():
    parser = argparse.ArgumentParser(description="Check Claude Max plan usage")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument("--setup", action="store_true", help="First-time: open Chrome to log in")
    parser.add_argument("--sub-if-needed", action="store_true", help="Print sub commands if near limit")
    args = parser.parse_args()

    if args.setup:
        setup_auth()
        return

    print("Checking Claude usage...")
    data = scrape_usage()

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
