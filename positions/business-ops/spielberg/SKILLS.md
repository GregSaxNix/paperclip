# SKILLS — Spielberg

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `pptx` — Visually compelling presentation and narrative decks
- [ ] `pdf` — Creative briefs and reference materials

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **ElevenLabs (future)** — Voice synthesis for video narration — pending setup

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `video-production-framework` — Story arc design, script structure, video narrative templates
- [ ] `creative-brief-templates` — Structured creative briefing formats for multimedia projects
