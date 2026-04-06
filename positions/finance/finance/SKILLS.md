# SKILLS — Finance

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- para-memory-files — PARA-method memory across sessions

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `xlsx` — Complex financial models, projections, scenario tables
- [ ] `pdf` — Financial statements, investment reports, research documents

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `finance-accounting (alirezarezvani/claude-skills)` — Financial analysis and modelling frameworks
- [ ] `c-level-advisory (alirezarezvani/claude-skills)` — CFO-level financial advisory frameworks

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **SQLite (claude_local only)** — Query local financial database records

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `gypsy-years-budget-model` — Greg's specific gypsy years budget scenarios, cost-of-living models
