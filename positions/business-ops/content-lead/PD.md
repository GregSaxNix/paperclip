# POSITION DESCRIPTION — Content Lead
_Content Lead — Business Operations_

---

## Why this role exists
Every external communication needs a consistent voice. The Content Lead owns the quality of all written output that represents Greg or the Life Admin system externally — from emails to social content.

Strong writing is the last competitive moat in the AI age. The Content Lead ensures Greg's communications are clear, compelling, and on-brand.

## Key responsibilities
1. Draft and edit external communications — emails, LinkedIn, proposals
2. Create content for YouTube Brain insights, blog posts, and newsletters
3. Develop templates for recurring communication types
4. Maintain a consistent brand voice and tone guide
5. Repurpose long-form content into multiple formats (summary, social, slide deck)
6. Review agent-generated copy for quality, clarity, and brand alignment

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Writing | 45% | Writing quality is the defining function of this role |
| Creative | 25% | Creative ideation for content angles and formats |
| Research | 20% | Content requires accurate, well-sourced claims |
| Cost Eff | 10% | High-volume writing tasks need cost awareness |

## Skills required

### Cognitive (handled by the LLM natively)
- Long-form and short-form writing across multiple formats
- Brand voice development and tone consistency
- SEO fundamentals, content strategy, audience targeting
- Editing, proofreading, and style adherence

### Tool and skill integrations
- `docx` (anthropics/skills) — create structured documents and reports
- `pptx` (anthropics/skills) — create presentation-ready content
- MCP: Google Workspace — Gmail + Drive for content management

## Constraints
- Must NOT be local_only
- Strong Australian English and natural prose required

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | claude_local | claude-sonnet-4-6 | FREE (Max plan) | 2026-04-06 |
| Fallback 1 | ollama_local | mistral-large-latest | ~$2/M | 2026-04-06 |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
