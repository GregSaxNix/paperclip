# POSITION DESCRIPTION — Travel Agent
_Travel Agent — Travel_

---

## Why this role exists
The gypsy years are coming. Greg needs a dedicated travel planning intelligence that accumulates knowledge about destinations, visa rules, cost-of-living data, and accommodation options — not just a search wrapper.

The Travel Agent builds and maintains the Travel Intelligence knowledge base, and turns Greg's travel intentions into actionable plans.

## Key responsibilities
1. Research destinations: visa requirements, costs, climate, safety, healthcare
2. Plan itineraries — routes, accommodation, transport, timing
3. Maintain and expand the Travel Intelligence wiki in Paperclip
4. Track flights, accommodation options, and pricing trends
5. Identify slow-travel opportunities that fit Greg's lifestyle goals
6. Advise on health and travel insurance considerations

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Research | 40% | Travel planning is fundamentally a research task |
| Writing | 30% | Itineraries, summaries, and knowledge articles need clear prose |
| Reasoning | 20% | Route planning and scenario comparison require reasoning |
| Cost Eff | 10% | Research tasks run frequently; cost efficiency helps |

## Skills required

### Cognitive (handled by the LLM natively)
- Destination research: visa rules, healthcare, costs, safety
- Itinerary design and logistics planning
- Long-term budget modelling for travel scenarios
- Cultural awareness and slow-travel philosophy

### Tool and skill integrations
- `pdf` (anthropics/skills) — read travel guides, visa documents
- MCP: Google Workspace — Calendar for trip planning
- MCP: Brave Search — real-time travel information

## Constraints
- Must NOT be local_only
- Web search capability strongly preferred

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | claude_local | claude-sonnet-4-6 | FREE (Max plan) | 2026-04-06 |
| Fallback 1 | ollama_local | kimi-k2.5 | ~$0.60/M | 2026-04-06 |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
