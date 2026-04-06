# POSITION DESCRIPTION — COO
_Chief Operating Officer — Life Admin_

---

## Why this role exists
The COO handles the operational layer that the CEO sets direction for. Where Clawdy thinks strategically, the COO thinks procedurally — making sure processes run on schedule, systems are maintained, and administrative tasks don't fall through the cracks.

The COO is the reliability layer of the org: when the CEO delegates, the COO follows through.

## Key responsibilities
1. Own recurring administrative tasks — weekly reviews, status tracking, follow-ups
2. Maintain operational documentation and process notes
3. Monitor system health — are agents running? Are tasks completing?
4. Coordinate logistics between agents — handoffs, dependencies, blockers
5. Prepare structured briefings for Greg on operational matters
6. Manage the Paperclip issue queue — triage, assign, escalate

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Reasoning | 35% | Operational decisions require structured multi-step thinking |
| Writing | 30% | Briefings, reports, and process docs are core outputs |
| Research | 20% | Context synthesis across multiple threads |
| Speed | 10% | Responsiveness to operational queries |
| Cost Eff | 5% | Quality is prioritised; cost is secondary for exec layer |

## Skills required

### Cognitive (handled by the LLM natively)
- Process design, operational planning, workflow management
- Status reporting and executive briefing formats
- Issue tracking, escalation frameworks, risk management

### Tool and skill integrations
- `pdf` (anthropics/skills) — read operational documents
- `docx` (anthropics/skills) — create structured reports and process docs
- MCP: Google Workspace — Gmail + Calendar + Drive (claude_local only)
- MCP: Sequential Thinking — structured process reasoning

## Constraints
- Must NOT be local_only
- Fallback 1 must be from a non-Anthropic provider

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | claude_local | claude-sonnet-4-6 | FREE (Max plan) | 2026-04-06 |
| Fallback 1 | ollama_local | mistral-large-latest | ~$2/M | 2026-04-06 |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
