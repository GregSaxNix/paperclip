# SKILLS — Researcher

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- para-memory-files — PARA-method memory across sessions
- council-debate — Trigger Council of Elders research debates
- skill-discovery — Identify and request new capabilities

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `pdf` — Research papers, technical reports, whitepapers
- [ ] `docx` — Structured research briefs and summaries

## MCP Tool Integrations
_Model Context Protocol servers. Available to claude_local adapter agents only._

- [ ] **Tavily (claude_local only)** — Semantic web search for high-quality research results
- [ ] **Exa (claude_local only)** — Neural search for finding relevant documents
- [ ] **Sequential Thinking (claude_local only)** — Structured multi-source research synthesis

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `llm-matrix-updater` — Research protocol for updating llm-matrix-data.json — pricing, benchmarks, new releases
