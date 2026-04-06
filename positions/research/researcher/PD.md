# POSITION DESCRIPTION — Researcher
_Researcher — Research_

---

## Why this role exists
Greg processes a huge volume of information: AI developments, health research, travel intelligence, business trends, financial news. The Researcher is the epistemological anchor — finding the truth in the noise.

Web access is essential. The Researcher synthesises real-time information from the web into concise, well-organised reports.

## Key responsibilities
1. Conduct deep research on topics Greg flags — technology, health, finance, travel
2. Monitor AI model releases, capability announcements, and benchmark results
3. Synthesise contradictory information into clear, balanced summaries
4. Update the LLM Matrix when new models or pricing data emerge
5. Produce research briefs with sourced claims and confidence levels
6. Support CEO and CTO with external context they need for decisions

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Research | 40% | Research quality — accuracy, synthesis, nuance — is the core function |
| Reasoning | 30% | Evaluating conflicting sources requires critical reasoning |
| Writing | 20% | Research briefs must be clear, well-structured, and concise |
| Cost Eff | 10% | Research tasks run frequently; cost efficiency valued |

## Skills required

### Cognitive (handled by the LLM natively)
- Source evaluation, fact-checking, and epistemic confidence assessment
- Multi-source synthesis into structured summaries
- Research methodology across domains (technology, health, finance)
- Citation and reference management

### Tool and skill integrations
- `pdf` (anthropics/skills) — read research papers and reports
- `docx` (anthropics/skills) — create structured research documents
- MCP: Tavily — semantic web search for high-quality research
- MCP: Exa — neural search for finding relevant documents
- MCP: Sequential Thinking — structured research reasoning

## Constraints
- Must NOT be local_only
- Web search capability is essential — model with real-time access preferred
- Fallback 1 must be from a non-Anthropic provider

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | ollama_local | grok-4.1 | ~$0.20/M | 2026-04-06 |
| Fallback 1 | ollama_local | kimi-k2.5 | ~$0.60/M | 2026-04-06 |
| Fallback 2 | ollama_local | qwen-plus | ~$0.26/M | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
