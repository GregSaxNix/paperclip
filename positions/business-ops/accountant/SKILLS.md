# SKILLS — Accountant

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [x] `xlsx` — Financial spreadsheets, expense tracking, budget models
- [x] `pdf` — Tax documents, financial statements, ATO correspondence

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `finance-accounting (alirezarezvani/claude-skills)` — Accounting frameworks, financial analysis patterns

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **SQLite (claude_local only)** — Query local financial database records

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `australian-tax-rules` — ATO rules, GST, BAS, NDIS funding categories — local reference skill
