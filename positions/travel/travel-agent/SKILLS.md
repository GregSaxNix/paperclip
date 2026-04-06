# SKILLS — Travel Agent

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- para-memory-files — PARA-method memory across sessions

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `pdf` — Travel guides, visa documents, health advisories

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **Google Workspace (claude_local only)** — Calendar for trip planning and scheduling
- [ ] **Brave Search (claude_local only)** — Real-time travel information and current prices

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `slow-travel-planner` — Long-stay destination research, monthly cost models, visa duration planning
