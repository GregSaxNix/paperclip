# If Greg drops the Claude Max plan

Written 10 November 2026. Paperclip's `claude_local` agents run through the Claude Code command line on Greg's Max plan, so they cost nothing extra. If the Max plan ends, they stop working (sign-in or quota errors on every run). Nothing else in Paperclip depends on it.

## What depends on Max today

| What | Model | Notes |
|---|---|---|
| Clawdy (CEO) | claude-opus-4-6 | Runs every few minutes; the busiest agent |
| Gayan (CTO) | claude-opus-4-6 | |
| COO | claude-opus-4-6 | |
| Yoda (Council judge) | claude-opus-4-6 | |
| Travel Agent | claude-sonnet-4-6 | Moved here 10 November 2026; old model `moonshot-v1-32k` was withdrawn |
| Task Scheduler `Paperclip Weekly Guidelines Refresh` | `claude -p` | Monday 10 AM; about US$8 of usage per run |

Check the current list: `python scripts/position_manager.py status`, or any agent with adapter `claude_local`.

## How to move off it

1. Pick the replacement. Two kinds:
   - **Another command-line agent** (Codex on a ChatGPT plan, Gemini CLI): keeps web search and file editing. Adapters `codex_local` / `gemini_local`.
   - **A pay-per-use cloud model** (Kimi, DeepSeek, Grok, MiniMax) through `ollama_local`: cheap, but it only sends one message and gets one reply. It cannot search the web, edit files or close issues. Reasoning models also need `timeoutMs` raised to 600000.
2. Edit each agent's `positions/<dept>/<role>/LINEUP.md`, then switch it with `python scripts/position_manager.py sub <Position> fallback1` (or edit the Primary row and run `restore <Position>`). The script keeps the agent's other settings and fills in the provider address and key from `.env`; it refuses if a key is missing.
3. Check the model still exists first: see `doc/plans/2026-11-10-agent-model-audit.md` for how (provider model list plus a one-word test call).
4. Rewrite `scripts/weekly_guidelines_refresh.py` to use the new command-line agent, or disable that task.
5. Test each agent with a manual run (`POST /api/agents/<id>/heartbeat/invoke`) and check the run succeeded.

Don't run `restore all` or `sync all`: several lineup files name models that providers no longer accept.
