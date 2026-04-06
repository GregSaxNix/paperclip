# SKILLS — Yoda

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- council-debate — Participate in and trigger Council of Elders debates

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **Sequential Thinking (claude_local only)** — Structured multi-step wisdom reasoning for complex decisions
