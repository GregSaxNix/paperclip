# SKILLS — Council Tech

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- council-debate — Participate in Council of Elders debates as the technical voice

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `software-engineering (wshobson/agents)` — Technical feasibility evaluation and architecture assessment

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **GitHub (claude_local only)** — Access current codebase for technical context in debates
