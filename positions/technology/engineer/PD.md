# POSITION DESCRIPTION — Engineer
_Software Engineer — Technology_

---

## Why this role exists
The Engineer handles routine coding tasks quickly and cheaply. Well-defined tickets, script writing, utility functions, small bug fixes — tasks where the spec is clear and execution speed matters more than architectural depth.

The Codex model is purpose-built for this: fast, accurate, tool-aware, and integrated with agentic coding workflows.

## Key responsibilities
1. Implement well-defined feature tickets with clear specs
2. Write utility scripts, data transforms, and automation tasks
3. Fix simple, well-scoped bugs with clear reproduction steps
4. Execute code-generation tasks from templates and patterns
5. Handle high-volume, low-complexity coding work efficiently

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Coding | 70% | Pure coding execution is 70% of the role |
| Reasoning | 20% | Sufficient reasoning to interpret tickets and handle edge cases |
| Speed | 10% | Fast turnaround on routine work |

## Skills required

### Cognitive (handled by the LLM natively)
- Task-oriented code generation from clear specifications
- Pattern matching against existing codebase conventions
- Script writing, data processing, automation

### Tool and skill integrations
- MCP: GitHub — repository access for context

## Constraints
- Must NOT be local_only
- Speed and throughput prioritised over deep reasoning

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | codex_local | gpt-5.3-codex | Weekly quota | 2026-04-06 |
| Fallback 1 | ollama_local | grok-code-fast-1 | ~$0.20/M | 2026-04-06 |
| Fallback 2 | ollama_local | minimax-m2.7 | ~$0.30/M | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
