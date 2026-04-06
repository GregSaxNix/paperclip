# SKILLS — CTO (Gayan)

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- para-memory-files — PARA-method memory across sessions
- skill-discovery — Identify and request new capabilities
- paperclip-create-agent — Spin up new technical agents when needed

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `pdf` — Technical documentation, architecture diagrams, research papers
- [ ] `pptx` — Technical presentations and architecture decks

## Job Skills (vet then install)
_Community skills requiring manual review before installation._

- [ ] `software-engineering (wshobson/agents)` — Engineering best practices, code architecture patterns
- [ ] `llm-development (wshobson/agents)` — LLM integration patterns, AI system design
- [ ] `backend-engineering (wshobson/agents)` — API design, server architecture, database patterns

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **GitHub (claude_local only)** — Repository access — 51 tools for code management, PRs, issues
- [ ] **Sequential Thinking (claude_local only)** — Structured architectural reasoning
- [ ] **Tavily (claude_local only)** — Research new technologies and evaluate frameworks
