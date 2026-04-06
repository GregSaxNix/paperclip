# POSITION DESCRIPTION — Finance
_Financial Analyst — Finance_

---

## Why this role exists
Beyond bookkeeping, Greg needs sophisticated financial analysis: scenario modelling for the gypsy years, investment options, Shine wind-down cashflow projections, and long-term wealth planning.

The Finance agent runs deeper analysis than the Accountant — it models scenarios, identifies patterns, and thinks several moves ahead.

## Key responsibilities
1. Build and maintain financial models for gypsy years budget scenarios
2. Analyse investment options, returns, and risk profiles
3. Model Shine Recruitment wind-down cash flow
4. Research financial products, rates, and ATO rulings
5. Prepare structured financial analysis reports for Greg
6. Identify cost-saving opportunities and financial risks

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Reasoning | 40% | Financial modelling requires rigorous, multi-step analytical reasoning |
| Research | 30% | Rates, rulings, and market data require deep research |
| Writing | 15% | Clear financial reports and analysis summaries |
| Cost Eff | 15% | Long-context analysis tasks; cost matters |

## Skills required

### Cognitive (handled by the LLM natively)
- Financial modelling, scenario analysis, DCF and ROI calculations
- Investment analysis, portfolio theory basics
- Australian tax and superannuation rules
- Risk analysis and sensitivity modelling

### Tool and skill integrations
- `xlsx` (anthropics/skills) — parse complex financial spreadsheets
- `pdf` (anthropics/skills) — read financial statements and research reports
- MCP: SQLite — query financial database records

## Constraints
- Must NOT be local_only
- Chain-of-thought reasoning preferred (R1-style models excel here)
- Long context window important for large financial documents

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | ollama_local | deepseek-reasoner | ~$0.55/M | 2026-04-06 |
| Fallback 1 | ollama_local | kimi-k2.5 | ~$0.60/M | 2026-04-06 |
| Fallback 2 | claude_local | claude-sonnet-4-6 | FREE (Max plan) | 2026-04-06 |
| Emergency | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
