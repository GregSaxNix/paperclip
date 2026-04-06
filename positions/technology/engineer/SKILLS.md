# SKILLS — Engineer

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- skill-discovery — Identify and request new capabilities

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `software-engineering (wshobson/agents)` — Engineering execution patterns
- [ ] `backend-engineering (wshobson/agents)` — API and server-side development patterns

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **GitHub (claude_local only)** — Repository access for codebase context
