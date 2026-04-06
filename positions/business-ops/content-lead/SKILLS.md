# SKILLS — Content Lead

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- para-memory-files — PARA-method memory across sessions

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `docx` — Structured documents, newsletters, content drafts
- [ ] `pptx` — Content presentations and slide decks

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `marketing-content (alirezarezvani/claude-skills)` — Content strategy, copy frameworks, audience targeting
- [ ] `brand-guidelines (alirezarezvani/claude-skills)` — Brand voice and tone consistency
- [ ] `internal-communications (alirezarezvani/claude-skills)` — Structured internal communications

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **Google Workspace (claude_local only)** — Gmail + Drive for content management and publishing
