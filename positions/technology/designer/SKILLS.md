# SKILLS — Designer

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- skill-discovery — Identify and request new capabilities

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `pptx` — Visual presentation decks and design mockups

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `brand-guidelines (alirezarezvani/claude-skills)` — Brand voice, visual identity, style consistency

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `dark-slate-design-system` — Paperclip-specific design system tokens, component patterns, CSS variables
