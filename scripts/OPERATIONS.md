# Life Admin — Operations Guide

_Your reference for everything. Greg, if you can't remember how something works, it's in here._

---

## Quick Reference

| Task | How |
|------|-----|
| Open Paperclip | Browser → `http://localhost:3100` |
| Open this ops hub | Open `D:\paperclip\scripts\ops-hub.html` in browser |
| Check Claude usage | `python scripts\check_claude_usage.py` |
| View agent matrix | Open `D:\paperclip\scripts\lineup_dashboard.html` |
| View monitor log | `python scripts\auto_monitor.py --log` |
| Sub agent to fallback | `python scripts\position_manager.py sub CEO fallback1` |
| Restore agent to primary | `python scripts\position_manager.py restore CEO` |
| Access Paperclip remotely | Open `https://greg-shinedesktop.tail4ef50.ts.net` on any device |

---

## Accessing Paperclip from Your Laptop (while away)

Tailscale Funnel is already set up. Nothing to install on the laptop.

1. Make sure the desktop is on and not asleep
2. On your laptop browser, go to: **https://greg-shinedesktop.tail4ef50.ts.net**
3. Full Paperclip UI — works anywhere in the world

**If the server isn't running** (Paperclip won't load):
- You need RDP to restart it (see Remote Desktop section below)
- Or: wait, the Task Scheduler auto-starts it on boot — restart the PC remotely if you have to

---

## Remote Desktop (to run terminal commands remotely)

Set up once on the desktop:
1. Search "Remote Desktop settings" → turn on "Enable Remote Desktop"

Then from the laptop:
1. Find the desktop's Tailscale IP (run once on desktop): `tailscale ip -4`
2. On laptop: open "Remote Desktop Connection" (Windows) or Microsoft Remote Desktop (Mac)
3. Enter the Tailscale IP
4. Log in with your Windows username and password

---

## Claude Usage Monitoring

The `check_claude_usage.py` script reads your Claude Max plan usage.

**Check now:**
```
python D:\paperclip\scripts\check_claude_usage.py
```

**What the meters mean:**
- **Session (5hr window)** — how much you've used in the current 5-hour rate-limit window. Resets every 5 hours.
- **All Models (weekly)** — total weekly usage across all Claude models. Resets Saturday.
- **Sonnet (weekly)** — separate weekly limit just for Sonnet. Resets Monday.

**If session hits 90%:** The auto-monitor will sub claude_local agents to fallback models automatically.

**Re-run setup** (if session expires — needed once every few weeks):
```
python D:\paperclip\scripts\check_claude_usage.py --setup
```
A Chrome window opens — log in with Google — press ENTER when done.

---

## Auto-Monitor (runs while you're away)

Installed as a Windows Task Scheduler job. Runs every 2 hours automatically.

**What it does:**
1. Checks Claude usage
2. If All Models or Session hits 90% → subs all claude_local agents to fallback1 (Grok-3)
3. When usage resets and drops below 90% → restores all agents to primary
4. Logs everything to `D:\paperclip\monitor.log`

**Check the log:**
```
python D:\paperclip\scripts\auto_monitor.py --log
```

**Run it manually:**
```
python D:\paperclip\scripts\auto_monitor.py
```

---

## Agent Substitution (manual)

Sub a single agent to fallback:
```
python D:\paperclip\scripts\position_manager.py sub CEO fallback1
python D:\paperclip\scripts\position_manager.py sub CEO fallback2
python D:\paperclip\scripts\position_manager.py sub CEO emergency
```

Restore to primary:
```
python D:\paperclip\scripts\position_manager.py restore CEO
python D:\paperclip\scripts\position_manager.py restore all
```

View all positions and their current model:
```
python D:\paperclip\scripts\position_manager.py status
```

**Position names:** CEO, CTO, COO, SeniorEngineer, Engineer, QABot, Designer, ContentLead, Accountant, Spielberg, Finance, TravelAgent, Researcher, Doc, Freud, Yoda, Contrarian, CouncilLocal, CouncilEU, CouncilCH, CouncilTech

---

## Agent Matrix Dashboard

Visual display of all 21 agents, their full fallback chains, and usage meters.

Open: `D:\paperclip\scripts\lineup_dashboard.html`

Regenerate (after any changes):
```
python D:\paperclip\scripts\position_manager.py dashboard
```

---

## Codex (OpenAI) Quota

Engineer and CouncilTech use Codex. Check quota:
```
python D:\paperclip\scripts\check_codex_quota.py
```

Setup (first time / session expired):
```
python D:\paperclip\scripts\check_codex_quota.py --setup
```

If quota is near limit:
```
python D:\paperclip\scripts\position_manager.py sub Engineer fallback1
python D:\paperclip\scripts\position_manager.py sub CouncilTech fallback1
```

---

## Paperclip Server

**Auto-starts on boot** via Windows Task Scheduler.

Check it's running:
```
curl http://localhost:3100/api/health
```

Start manually if needed:
```
D:\paperclip\start.cmd
```

Always start from `D:\paperclip\` using `pnpm dev` — not `pnpm dev:server` (UI won't load).

---

## Memory System

Each agent stores memory in markdown files. Memory is how agents remember context across sessions.

**Location:**
```
C:\Users\Administrator\.paperclip\instances\default\companies\505ab906...\agents\{agent-id}\instructions\MEMORY.md
```

**Claude Code's own memory** (this assistant remembers things between conversations):
```
C:\Users\Administrator\.claude\projects\d--paperclip\memory\
```

Agents with the `para-memory-files` skill can read and write their own MEMORY.md automatically.

---

## Dismissing Stale Failed Runs (inbox)

If you see old "Failed run" notifications in the Paperclip inbox, paste this in the browser console (F12 → Console tab while on Paperclip):

```javascript
const key = "paperclip:inbox:dismissed";
const ids = ["run:432533d4-f3a7-46d4-b18e-3d7187bb69a2","run:b3ba92b1-f96b-4c21-aefd-7df0445e6299","run:2994be46-3a8c-4e65-98f9-2f9da837d088","run:1ab619c8-8117-4de3-a0e2-dfb7cd626f98","run:9d770c05-f2c8-497f-8393-3409a6d730ed","run:2ddbdb90-8ada-4e54-b103-f2ea08da9ef9","run:b78c1f36-5324-471d-a2c9-3d806abcf25f","run:ac0f7f16-8a06-44dd-9e41-98c7508f2dec","run:4ca1b093-3c1a-4627-92b4-ab7111faa807","run:49726eb1-532d-40ad-b352-191cae640810","run:3cf8344d-6ba3-4b8a-9219-4c0e616c8877","run:faabc672-0c57-4c49-bd10-e928f8e32088","run:e8c401c3-7292-4170-a005-2cf6311a7cbe"];
const existing = JSON.parse(localStorage.getItem(key) || "[]");
localStorage.setItem(key, JSON.stringify([...new Set([...existing,...ids])]));
console.log("Done — refresh the page.");
```

Then refresh the page.

---

## File Locations Reference

| File | Purpose |
|------|---------|
| `D:\paperclip\scripts\ops-hub.html` | Central ops interface — open in browser |
| `D:\paperclip\scripts\lineup_dashboard.html` | Agent matrix with fallback chains |
| `D:\paperclip\scripts\position_manager.py` | CLI for managing agent positions |
| `D:\paperclip\scripts\check_claude_usage.py` | Check Claude Max plan usage |
| `D:\paperclip\scripts\check_codex_quota.py` | Check Codex task quota |
| `D:\paperclip\scripts\auto_monitor.py` | Auto-monitor (runs via Task Scheduler) |
| `D:\paperclip\monitor.log` | Auto-monitor log |
| `D:\paperclip\claude-usage.json` | Latest Claude usage data |
| `D:\paperclip\positions\` | All 21 position definitions (SOUL, LINEUP, SKILLS) |
| `D:\paperclip\positions\positions.json` | Live state — active model per position |
| `C:\Users\Administrator\.paperclip\instances\default\GREG.md` | Master GREG.md (distributed to all agents) |

---

_Last updated: 2026-04-06_
