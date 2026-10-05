r"""
check_api_balances.py -- API balance/quota monitor for cloud LLM providers

Checks balances for: DeepSeek, Moonshot, MiniMax, xAI (manual).
Reads keys from D:\paperclip\.env.
Posts a Paperclip issue if any balance is below the LOW_BALANCE_THRESHOLD.
Logs results to D:\paperclip\scripts\api-balances.log.

Usage:
    python check_api_balances.py              # Check and print summary
    python check_api_balances.py --json       # Print JSON only
    python check_api_balances.py --no-issue   # Check without posting issues

Schedule: Task Scheduler -- Mondays 8AM AEST (weekly)
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

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(r"D:\paperclip")
ENV_FILE = BASE_DIR / ".env"
LOG_FILE = BASE_DIR / "scripts" / "api-balances.log"

PAPERCLIP_BASE = "http://localhost:3100"
COMPANY_ID = "505ab906-66b5-4400-b131-96b8aee91c5d"

LOW_BALANCE_THRESHOLD = 5.0   # USD — post issue if below this

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)


# ── .env reader ───────────────────────────────────────────────────────────────
def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


# ── HTTP helper ───────────────────────────────────────────────────────────────
def get_json(url: str, bearer: str, timeout: int = 15) -> dict:
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {bearer}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"HTTP {e.code}: {body}") from e
    except Exception as e:
        raise RuntimeError(str(e)) from e


# ── Provider checks ───────────────────────────────────────────────────────────
def check_deepseek(key: str) -> dict:
    """DeepSeek: GET /user/balance — returns balance_infos list."""
    try:
        data = get_json("https://api.deepseek.com/user/balance", key)
        # Response: {"is_available": true, "balance_infos": [{"currency":"CNY","total_balance":"...","granted_balance":"...","topped_up_balance":"..."}]}
        if not data.get("is_available"):
            return {"provider": "DeepSeek", "status": "unavailable", "balance_usd": None}
        infos = data.get("balance_infos", [])
        # Find USD or CNY balance
        usd = None
        for info in infos:
            currency = info.get("currency", "")
            raw = info.get("total_balance") or info.get("topped_up_balance", "0")
            try:
                amount = float(raw)
            except (ValueError, TypeError):
                amount = 0.0
            if currency.upper() == "USD":
                usd = amount
                break
            elif currency.upper() == "CNY" and usd is None:
                usd = round(amount / 7.25, 2)  # approximate CNY→USD
        return {"provider": "DeepSeek", "status": "ok", "balance_usd": usd, "raw": infos}
    except Exception as e:
        return {"provider": "DeepSeek", "status": "error", "error": str(e), "balance_usd": None}


def check_moonshot(key: str) -> dict:
    """Moonshot: GET /v1/users/me/balance (international endpoint: api.moonshot.ai)"""
    try:
        data = get_json("https://api.moonshot.ai/v1/users/me/balance", key)
        # Response: {"code":0,"data":{"available_balance":X,"voucher_balance":Y,"cash_balance":Z}}
        inner = data.get("data", data)
        available = inner.get("available_balance") or inner.get("cash_balance") or 0.0
        try:
            usd = float(available)
        except (ValueError, TypeError):
            usd = 0.0
        return {
            "provider": "Moonshot",
            "status": "ok",
            "balance_usd": usd,
            "raw": inner,
        }
    except RuntimeError as e:
        msg = str(e)
        if "HTTP 401" in msg:
            return {
                "provider": "Moonshot",
                "status": "invalid_key",
                "balance_usd": None,
                "note": "API key rejected (401) -- rotate at platform.moonshot.ai",
            }
        return {"provider": "Moonshot", "status": "error", "error": msg[:80], "balance_usd": None}
    except Exception as e:
        return {"provider": "Moonshot", "status": "error", "error": str(e), "balance_usd": None}


def check_minimax(key: str) -> dict:
    """MiniMax: auth test via chat completion (no public balance API).
    MiniMax returns 200 with base_resp.status_code == 2049 for invalid keys.
    Balance must be checked manually at https://platform.minimax.io.
    """
    import json as _json
    payload = _json.dumps({
        "model": "MiniMax-Text-01",
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 1,
    }).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = _json.loads(resp.read())
        # International API uses standard HTTP error codes, check for auth failure in body too
        if data.get("error", {}).get("type") == "authorized_error":
            return {
                "provider": "MiniMax",
                "status": "invalid_key",
                "balance_usd": None,
                "note": "API key rejected — rotate at platform.minimax.io/user-center/basic-information",
            }
        return {
            "provider": "MiniMax",
            "status": "ok",
            "balance_usd": None,
            "note": "Key valid. Balance: platform.minimax.io/user-center/payment/balance",
        }
    except Exception as e:
        return {
            "provider": "MiniMax",
            "status": "error",
            "error": str(e),
            "balance_usd": None,
            "note": "Check https://platform.minimax.io manually",
        }


def check_xai() -> dict:
    """xAI: No public balance API — manual check required."""
    return {
        "provider": "xAI (Grok)",
        "status": "manual",
        "balance_usd": None,
        "note": "No public balance API. Check https://console.x.ai manually.",
    }


# ── Paperclip issue poster ────────────────────────────────────────────────────
def post_paperclip_issue(title: str, body: str) -> dict:
    payload = json.dumps(
        {"title": title, "description": body, "status": "todo", "priority": "high"}
    ).encode()
    req = urllib.request.Request(
        f"{PAPERCLIP_BASE}/api/companies/{COMPANY_ID}/issues",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}


# ── Main ──────────────────────────────────────────────────────────────────────
def run(args) -> list:
    env = load_env(ENV_FILE)

    results = []

    deepseek_key = env.get("DEEPSEEK_API_KEY", "")
    moonshot_key = env.get("MOONSHOT_API_KEY", "")
    minimax_key = env.get("MINIMAX_API_KEY", "")

    if deepseek_key:
        results.append(check_deepseek(deepseek_key))
    else:
        results.append({"provider": "DeepSeek", "status": "no_key", "balance_usd": None})

    if moonshot_key:
        results.append(check_moonshot(moonshot_key))
    else:
        results.append({"provider": "Moonshot", "status": "no_key", "balance_usd": None})

    if minimax_key:
        results.append(check_minimax(minimax_key))
    else:
        results.append({"provider": "MiniMax", "status": "no_key", "balance_usd": None})

    results.append(check_xai())

    return results


def main():
    parser = argparse.ArgumentParser(description="Check API balances for LLM providers")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument("--no-issue", action="store_true", help="Skip posting Paperclip issues")
    args = parser.parse_args()

    results = run(args)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ── Log ───────────────────────────────────────────────────────────────────
    log.info("Balance check run: %s", now)
    for r in results:
        log.info(
            "  %-20s status=%-12s balance_usd=%s",
            r["provider"],
            r["status"],
            r.get("balance_usd"),
        )

    if args.json:
        print(json.dumps({"checked_at": now, "results": results}, indent=2))
        return

    # ── Print table ───────────────────────────────────────────────────────────
    print(f"\nAPI Balance Check — {now}")
    print(f"{'Provider':<22} {'Status':<12} {'Balance (USD)':<16} Notes")
    print("-" * 70)
    low = []
    for r in results:
        bal = r.get("balance_usd")
        bal_str = f"${bal:.2f}" if isinstance(bal, (int, float)) else "—"
        note = r.get("note", r.get("error", ""))[:35]
        status = r["status"]
        flag = ""
        if isinstance(bal, (int, float)) and bal < LOW_BALANCE_THRESHOLD:
            flag = " ⚠ LOW"
            low.append(r)
        print(f"{r['provider']:<22} {status:<12} {bal_str:<16} {note}{flag}")
    print()

    # ── Post issue if low ─────────────────────────────────────────────────────
    if low and not args.no_issue:
        lines = [f"- **{r['provider']}**: ${r['balance_usd']:.2f}" for r in low]
        body = (
            f"Balance check run {now}\n\n"
            f"The following providers are below the ${LOW_BALANCE_THRESHOLD:.0f} threshold:\n\n"
            + "\n".join(lines)
            + "\n\nPlease top up to avoid agent failures."
        )
        title = f"⚠ Low API balance alert — {', '.join(r['provider'] for r in low)}"
        resp = post_paperclip_issue(title, body)
        if "id" in resp:
            print(f"Paperclip issue posted: {resp['id'][:8]} — {title}")
            log.info("Posted Paperclip issue: %s", resp.get("id"))
        else:
            print(f"Failed to post issue: {resp.get('error')}")
            log.error("Failed to post issue: %s", resp)
    elif low and args.no_issue:
        print(f"⚠  {len(low)} low balance(s) detected — issue posting skipped (--no-issue)")


if __name__ == "__main__":
    main()
