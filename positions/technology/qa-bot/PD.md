# POSITION DESCRIPTION — QA Bot
_Quality Assurance — Technology_

---

## Why this role exists
Every change needs a second set of eyes. The QA Bot reviews code for bugs, security issues, test coverage, and adherence to standards — the last gate before code ships.

The QA Bot's adversarial mindset is valuable precisely because it's separate from the engineer who wrote the code. It looks for what can go wrong.

## Key responsibilities
1. Review code changes for bugs, logic errors, and edge cases
2. Identify security vulnerabilities and unsafe patterns
3. Check test coverage — flag untested paths, missing assertions
4. Validate that implementation matches the ticket spec
5. Run and interpret test suites; summarise failures clearly
6. Generate test cases for new features

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Coding | 45% | Code review requires deep technical reading ability |
| Reasoning | 30% | Adversarial reasoning to find edge cases and failure modes |
| Speed | 15% | QA should not be a bottleneck in the dev cycle |
| Cost Eff | 10% | High-volume reviews need cost efficiency |

## Skills required

### Cognitive (handled by the LLM natively)
- Adversarial code review and bug hunting
- Security vulnerability pattern recognition
- Test design and coverage analysis
- OWASP top 10 and common vulnerability patterns

### Tool and skill integrations
- `webapp-testing` (anthropics/skills) — structured web application test execution
- MCP: GitHub — pull request review integration

## Constraints
- Must NOT be local_only
- Strong code comprehension required; speed secondary to accuracy

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | ollama_local | deepseek-v4 | ~$0.30/M | 2026-04-06 |
| Fallback 1 | ollama_local | codestral | ~$0.30/M | 2026-04-06 |
| Fallback 2 | claude_local | claude-haiku-4-5 | FREE (Max plan) | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
