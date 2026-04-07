# SKILLS — CEO (Clawdy)

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control — access to all Paperclip API tools
- paperclip-create-agent — Hire new agents on behalf of Greg
- paperclip-create-plugin — Commission new plugin capabilities
- para-memory-files — PARA-method memory across sessions
- council-debate — Trigger multi-LLM Council of Elders debate rounds
- skill-discovery — Identify and request new capabilities

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [x] `pdf` — Board reports, research documents, strategic briefs
- [x] `pptx` — Presentations and strategic briefing decks

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `c-level-advisory (alirezarezvani/claude-skills)` — Executive advisory frameworks, board reporting
- [ ] `strategic-planning-framework (alirezarezvani/claude-skills)` — OKR, SWOT, scenario planning
- [ ] `stakeholder-communication (alirezarezvani/claude-skills)` — Tone and format per audience type

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **Google Workspace (claude_local only)** — Gmail + Calendar + Drive + Docs — workspacemcp.com
- [ ] **Sequential Thinking (claude_local only)** — Structured multi-step reasoning for complex strategic decisions

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `executive-coaching-framework` — Structured coaching prompts, reflective questioning, leadership development
