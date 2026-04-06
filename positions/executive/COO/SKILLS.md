# SKILLS — COO

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- para-memory-files — PARA-method memory across sessions

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `pdf` — Operational documents, process guides, reports
- [ ] `pptx` — Operational presentations and briefing decks
- [ ] `docx` — Structured process documentation and reports

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `c-level-advisory (alirezarezvani/claude-skills)` — Executive advisory and operational frameworks
- [ ] `internal-communications (alirezarezvani/claude-skills)` — Structured internal reporting and team comms

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **Google Workspace (claude_local only)** — Gmail + Calendar + Drive — operational coordination
- [ ] **Sequential Thinking (claude_local only)** — Structured process and operational reasoning
