# SKILLS — Council Local

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- council-debate — Participate in Council of Elders debates as the local offline voice

## Notes

**LOCAL ONLY** — No external skills or MCP servers. Participates in debates using only what is provided in the conversation context.
