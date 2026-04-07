# SKILLS — Senior Engineer

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- skill-discovery — Identify and request new capabilities

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [x] `pdf` — Technical documentation and research papers

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `software-engineering (wshobson/agents)` — Engineering best practices, code quality standards
- [ ] `ci-cd-engineering (wshobson/agents)` — CI/CD pipeline management and deployment automation
- [ ] `code-review (wshobson/agents)` — Structured code review frameworks

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **GitHub (claude_local only)** — Repository access — PR management, issue tracking
- [ ] **Sequential Thinking (claude_local only)** — Structured architectural reasoning
