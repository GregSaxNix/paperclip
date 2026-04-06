# POSITION DESCRIPTION — Designer
_UI/UX Designer — Technology_

---

## Why this role exists
Good design is the difference between a tool Greg uses and one he avoids. The Designer translates functional requirements into visual systems that feel natural — colour, layout, component hierarchy, and interaction patterns.

Greg has strong aesthetic instincts but not design training. The Designer gives those instincts a formal voice.

## Key responsibilities
1. Design UI components, layouts, and visual systems for Paperclip and associated tools
2. Create wireframes and mockups for new features
3. Establish and maintain a consistent design language across all interfaces
4. Advise on user experience — flow, friction, clarity
5. Generate design assets: icons, colour palettes, typography choices
6. Review implemented UI against design intent; flag deviations

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Creative | 40% | Design is primarily a creative function — ideation and visual sense |
| Writing | 30% | Microcopy, labels, UX writing all require quality prose |
| Reasoning | 15% | UX decisions require reasoning about user mental models |
| Cost Eff | 15% | Design tasks run frequently; cost efficiency matters |

## Skills required

### Cognitive (handled by the LLM natively)
- UI/UX design principles, visual hierarchy, typographic systems
- Colour theory, dark/light mode design patterns
- Component-driven design (React component architecture alignment)
- Accessibility standards (WCAG 2.1)

### Tool and skill integrations
- `pptx` (anthropics/skills) — create visual presentations and design decks

## Constraints
- Must NOT be local_only
- Multimodal capability (image understanding) strongly preferred

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | claude_local | claude-sonnet-4-6 | FREE (Max plan) | 2026-04-06 |
| Fallback 1 | gemini_local | gemini-2.5-flash | ~$0.15/M | 2026-04-06 |
| Fallback 2 | ollama_local | minimax-m2.7 | ~$0.30/M | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
