# POSITION DESCRIPTION — Senior Engineer
_Senior Software Engineer — Technology_

---

## Why this role exists
The Senior Engineer handles complex, high-stakes coding tasks that require context awareness, architectural judgement, and the ability to work across a large codebase (1M+ token context is essential).

Where the Engineer executes defined tasks quickly, the Senior Engineer handles ambiguity — diagnosing root causes, proposing solutions, and owning implementation end-to-end.

## Key responsibilities
1. Implement complex features across the Paperclip stack (TypeScript, React, Node)
2. Diagnose and fix non-trivial bugs — from root cause to resolution
3. Architect new subsystems: adapters, plugins, agent lifecycle
4. Write and maintain tests; uphold code quality standards
5. Support the CTO with large-scope technical investigations
6. Handle tasks too large for the general Engineer slot (> 8K token context needed)

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Coding | 40% | Writing production-quality code is the primary function |
| Reasoning | 35% | Architecture and debugging require deep analytical ability |
| Speed | 15% | Development velocity matters for iteration speed |
| Cost Eff | 10% | API-backed models; cost tracked against output value |

## Skills required

### Cognitive (handled by the LLM natively)
- Full-stack TypeScript/React/Node.js development
- Database design, API architecture, testing patterns
- Performance optimisation, security review
- AI/ML integration patterns (agent systems, LLM adapters)

### Tool and skill integrations
- MCP: GitHub — repository access, PR management, issue tracking
- MCP: Sequential Thinking — structured architectural reasoning

## Constraints
- Must NOT be local_only
- Model must support large context window (>=100K tokens recommended)

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | ollama_local | deepseek-v4 | ~$0.30/M | 2026-04-06 |
| Fallback 1 | ollama_local | grok-code-fast-1 | ~$0.20/M | 2026-04-06 |
| Fallback 2 | ollama_local | deepseek-chat | ~$0.26/M | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
