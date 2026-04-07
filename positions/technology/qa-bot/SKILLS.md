# SKILLS — QA Bot

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- skill-discovery — Identify and request new capabilities

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [x] `webapp-testing` — Structured web application test execution (anthropics/skills)

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `software-engineering (wshobson/agents)` — Code quality and testing frameworks

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **GitHub (claude_local only)** — Pull request review and issue tracking
