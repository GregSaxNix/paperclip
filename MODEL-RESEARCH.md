# Life Admin — Model Research Database

**Purpose:** Comprehensive matrix of all available AI models × all agent task types. Used to inform and update LLM-MATRIX.md.  
**Update cadence:** Weekly — re-run model research agent to capture pricing/model changes.  
**Last updated:** 2026-04-06

---

## All Available Models (API access, last 6 months)

### Anthropic — Claude

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Claude Opus 4.6 | 1M | $5.00 | $25.00 | Yes | Yes | Via claude_local | Best reasoning overall; FREE via Max plan |
| Claude Sonnet 4.6 | 200K | $3.00 | $15.00 | Yes | Yes | Via claude_local | Balanced; FREE via Max plan |
| Claude Haiku 4.5 | 200K | $0.80 | $4.00 | Yes | No | Via claude_local | Fast, structured tasks; FREE via Max plan |

> All Claude models are FREE via Greg's Anthropic Max plan. No API key needed — use claude_local adapter.

---

### OpenAI — GPT / Codex

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| gpt-5.3-codex | N/A | **Weekly quota** | **Weekly quota** | No | Yes | codex_local | ChatGPT Plus device auth; finite weekly limit |
| GPT-4o | 128K | $2.50 | $10.00 | Yes | No | Yes | Strong general + vision |
| GPT-4o mini | 128K | $0.15 | $0.60 | Yes | No | Yes | Cheap GPT-4 quality |
| o4-mini | 200K | $1.10 | $4.40 | Yes | Yes | Yes | Fast reasoning model |
| o3 | 200K | $10.00 | $40.00 | Yes | Yes | Yes | Premium reasoning; expensive |

> OpenAI API key is SEPARATE from ChatGPT Plus Codex OAuth — safe to add. Worth evaluating after 1 week of Codex quota tracking.

---

### Google — Gemini

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Gemini 2.5 Pro | 1M | $1.25 | $10.00 | Yes | Yes | Via gemini_local | Best Gemini; 1M context; thinking mode |
| Gemini 2.5 Flash | 1M | $0.15 | $0.60 | Yes | Yes | Via gemini_local | Best value; 201 tok/sec; thinking mode |
| Gemini 2.5 Flash-Lite | 1M | $0.075 | $0.30 | Yes | No | Via gemini_local | Ultra-cheap; simple tasks |
| ~~Gemini 2.0 Flash~~ | — | — | — | — | — | — | **DEPRECATED — shutting down June 1, 2026. Do not use.** |

---

### xAI — Grok

| Model | Context | Input /M | Output /M | Vision | Web Search | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|------------|---------------|-------|
| Grok-4 | 131K | $3.00 | $15.00 | Yes | Via Responses API | Yes (api.x.ai/v1) | Premium reasoning; vision support |
| Grok-4.1 | 131K | $0.20 | $0.50 | Yes | Via Responses API | Yes | **Best value Grok**; vision; web search |
| Grok-3-fast | 131K | $5.00 | $25.00 | Yes | Via Responses API | Yes | Fast Grok-3 variant; expensive |
| Grok-3 | 131K | $3.00 | $15.00 | Yes | Via Responses API | Yes | Current council model; balanced |
| Grok-3 Mini | 131K | $0.30 | $0.50 | Yes | No | Yes | Cheap Grok reasoning |
| Grok-Code-Fast-1 | 128K | $0.20 | $1.50 | No | No | Yes | **Coding specialist** — purpose-built |

> Grok context window updated to 131K (was 2M for "Grok-4.1 Fast" — that was a research error; confirmed 131K).  
> Grok's `x_search` and `web_search` tools (via Responses API) cost $2.50–$5 per 1,000 calls. Use for X/Twitter monitoring and live web research.  
> **Grok-Code-Fast-1** at $0.20/$1.50 is purpose-built for code — strong fallback for Engineer/QA.  
> **Grok-4.1** at $0.20/$0.50 with vision support is the best value Grok; good for Researcher role.

---

### Mistral

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Mistral Large 3 | TBD | $2.00 | $6.00 | Yes | No | No | Strong reasoning, multilingual; free trial tier |
| Mistral Small 4 | TBD | $0.15 | — | Yes | Yes | No | **New (2026):** Unified reasoning+multimodal+coding |
| Mistral Medium 3 | TBD | $1.00 | $3.00 | Yes | No | No | Mid-tier; good value |
| Codestral | 256K | $0.30 | $0.90 | No | No | No | **Code specialist** from Mistral |
| Magistral 1.2 | TBD | TBD | TBD | Yes | Yes | No | Enterprise reasoning variant |
| Mistral Nemo | TBD | $0.02 | — | No | No | No | Cheapest in lineup; minimal tasks |

---

### DeepSeek

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| DeepSeek V4 | 1M | $0.30 | $0.50 | Yes | Yes | Yes | **New (Mar 2026):** 81% SWE-bench, multimodal, hybrid reasoning |
| DeepSeek V3.2 | 128K | $0.26 | $0.38 | Yes | No | Yes | Confirmed current V3; excellent code/analysis |
| DeepSeek R1 | 64K | $0.55 | $2.19 | No | Yes | Yes | Chain-of-thought reasoning specialist |

---

### Moonshot — Kimi

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Kimi K2.5 | 200K+ | $0.60 | $2.50 | Yes | Yes | Yes | **CORRECTED pricing.** Long-context; web search ($0.005/call); caching → $0.15/M input |

---

### MiniMax

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| MiniMax-M2.7 | 205K | $0.30 | $1.20 | Yes | No | No | **CORRECTED pricing.** Two variants: standard + highspeed |

---

### Alibaba — Qwen

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Qwen 2.5-Max | TBD | $2.00 | $6.00 | Yes | No | No | Top Qwen; aligned with Mistral Large pricing |
| Qwen-Plus | 1M | $0.26 | $0.78 | No | No | Yes | 1M context; excellent value |
| Qwen2.5 72B | 128K | $0.23 | $0.23 | No | No | Yes | ~1/10th GPT-4o cost; solid all-rounder |
| Qwen-Turbo | 128K | $0.05 | $0.15 | No | No | Yes | Ultra-cheap; basic tasks |
| Qwen2.5 (local via Ollama) | 128K | FREE | FREE | No | No | Yes | Run on RTX 4090; private |

> Qwen2.5-7B and 14B available locally via Ollama — free, private, runs on RTX 4090.

---

### Zhipu AI — GLM

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| GLM-5 | TBD | TBD | TBD | Yes | Yes | No | **New (Feb 2026):** 30–60% price increase; overseas +67-100% |
| GLM-4.7 | 200K | $0.39 | $1.75 | No | No | No | Strong generalist; 200K context |
| GLM-4.7-Flash | 200K | **FREE** | **FREE** | Yes | No | No | **Free.** Good for bulk/simple tasks |
| GLM-4.5 | TBD | $0.60 | $2.20 | Yes | No | No | General-purpose; cost-effective |
| GLM-4.5-Flash | TBD | **FREE** | **FREE** | Yes | No | No | **Free.** Flash variant |
| GLM-4.5-X | TBD | TBD | $8.90 | Yes | Yes | No | Premium enterprise; expensive |

> GLM-4.5-Flash and GLM-4.7-Flash are FREE — useful for high-volume simple tasks.  
> GLM-5 launched Feb 2026 with significant price increases; overseas pricing adds 67–100% premium. Low priority for Greg's setup.  
> Note: GLM uses Zhipu's proprietary API (open.bigmodel.cn) — not OpenAI-compatible.

---

### Ollama Cloud (NEW — September 2025)

| Plan | Cost | Notes |
|------|------|-------|
| Free | Limited | Session + weekly limits |
| Pro | $20/month | Higher session limits |
| Max | $100/month | Highest limits |

> Fixed subscription, not per-token. NVIDIA-hosted. Provides same models as local Ollama (including cloud variants like `qwen3.5:cloud`).  
> **Adapter compatibility:** Requires new `ollama_cloud` adapter or OpenAI-compatible HTTP adapter — the existing `ollama_local` adapter points to localhost and won't work with cloud endpoint.  
> For Greg's use case (RTX 4090 already available), local Ollama is better value. Ollama Cloud is for machines without GPUs.

---

## OpenRouter — Recommended Integration Strategy

**What it is:** Single API gateway to 167+ models from all major providers. OpenAI-compatible. No markup — direct provider pricing.

**Key benefits for this system:**
- One API key replaces ~10 individual provider keys
- Automatic model fallback chains built in (configure in request, not code)
- Auto-router selects best model for the prompt automatically
- Easy A/B testing — swap model via parameter, no code change
- BYOK option: bring your own provider keys, 1M requests/month free, then 5% fee
- Free tier available (free models, limited rate)

**How to use in Paperclip:**  
The `http` adapter (or `ollama_local` with cloud URL) can call OpenRouter:
```
URL: https://openrouter.ai/api/v1/chat/completions
Auth: Bearer <OPENROUTER_API_KEY>
Body: { "model": "anthropic/claude-opus-4-6", "messages": [...] }
```

**Drawback:** 5% markup on BYOK usage above 1M/month. Negligible at Greg's usage levels.

**Recommendation: Evaluate as the primary API management layer** for all cloud agents except Claude (which uses the free claude_local adapter). This would simplify managing Grok, Mistral, DeepSeek, Kimi, MiniMax, Qwen, GLM into a single OpenRouter key and fallback config.

---

## Codex Usage Monitoring Design

**Problem:** ChatGPT Plus gives a weekly Codex quota that resets on a fixed day. We need to track usage and auto-swap Engineer → MiniMax when the daily budget is consumed.

**Daily budget formula:**
```
daily_allowed = weekly_quota × (day_of_week / 7)
```
Monday = 1/7, Tuesday = 2/7, ..., Sunday = 7/7. This prevents front-loading consumption.

**Monitoring approach (recommended):**

The `https://chatgpt.com/codex/settings/usage` page requires ChatGPT OAuth login — it is a client-side rendered React app, not scrapeable with simple HTTP. Options:

1. **Playwright script (best):** Python script runs headless browser with saved session cookies, scrapes usage data, writes to `D:\paperclip\codex-quota.json`. A Paperclip scheduled task (cron) reads this file before each Codex invocation.

2. **Manual weekly log:** Greg manually notes the weekly quota on Monday. Paperclip uses this value × (day/7) formula. Simpler but requires weekly input.

3. **OpenAI Usage API (fallback):** `GET https://api.openai.com/v1/usage?date=YYYY-MM-DD` — this tracks API key usage (gpt-4o etc.), NOT ChatGPT Plus Codex. Not directly useful for Codex quota but useful if we later add an OpenAI API key.

**Implementation plan (separate task):**
- Python script: `D:\paperclip\scripts\check_codex_quota.py`
- Output: `D:\paperclip\codex-quota.json` with `{ weekly_quota, used, daily_budget, should_use_codex, reset_date }`
- Paperclip agent config reads this file via a startup check in the Codex agent's SOUL.md
- If `should_use_codex = false`, agent instructions direct it to switch to MiniMax fallback

---

## Model × Task Suitability Matrix

**Scoring:** 0 = unsuitable, 5 = best-in-class  
**Adjusted score** = suitability × (1 / relative_cost_rank) — rewards high suitability at low cost  
**Cost rank:** 1 = free/cheapest, 5 = most expensive

### Task Categories

| # | Task | Description |
|---|------|-------------|
| T1 | Strategic reasoning | Planning, decision-making, complex orchestration |
| T2 | Code generation | Writing new code, algorithms, implementations |
| T3 | Code review / QA | Bug finding, test writing, code analysis |
| T4 | Long-context research | Reading/synthesising 50K+ token documents |
| T5 | Business writing | Proposals, comms, reports, Shine/HR content |
| T6 | Financial analysis | Budgets, investment research, structured numbers |
| T7 | Creative / video | Scripts, shot lists, creative storytelling |
| T8 | Contrarian / debate | Devil's advocate, challenging assumptions |
| T9 | Web / X research | Live web search, X/Twitter monitoring |
| T10 | Local/private | Health data, sensitive info — must be local |

### Suitability Scores

| Model | Cost rank | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | T10 |
|-------|-----------|----|----|----|----|----|----|----|----|----|----|
| **Claude Opus 4.6** | 1 (free) | **5** | 5 | 5 | 4 | **5** | 4 | 5 | 4 | 0 | 0 |
| **Claude Sonnet 4.6** | 1 (free) | 4 | 4 | 4 | 4 | **5** | 4 | **5** | 3 | 0 | 0 |
| **Claude Haiku 4.5** | 1 (free) | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 2 | 0 | 0 |
| **gemma4:26b (local)** | 1 (free) | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 0 | **5** |
| **GLM-4.7-Flash** | 1 (free) | 2 | 3 | 3 | 4 | 3 | 3 | 2 | 1 | 0 | 0 |
| **Gemini 2.5 Flash** | 2 ($0.15) | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 2 | 0 | 0 |
| **Mistral Small 4** | 2 ($0.15) | 3 | 4 | 4 | 3 | 4 | 3 | 3 | 2 | 0 | 0 |
| **Grok-4.1** | 2 ($0.20) | 4 | 4 | 4 | 4 | 3 | 3 | 3 | 4 | 4 | 0 |
| **Grok-Code-Fast-1** | 2 ($0.20) | 2 | **5** | **5** | 2 | 2 | 2 | 1 | 1 | 0 | 0 |
| **Qwen2.5 72B** | 2 ($0.23) | 3 | 4 | 4 | 4 | 3 | 3 | 3 | 2 | 0 | 0 |
| **DeepSeek V3.2** | 2 ($0.26) | 4 | **5** | **5** | 3 | 3 | 4 | 2 | 2 | 0 | 0 |
| **Qwen-Plus** | 2 ($0.26) | 3 | 4 | 4 | **5** | 4 | 3 | 3 | 2 | 0 | 0 |
| **Codestral** | 2 ($0.30) | 1 | **5** | **5** | 2 | 1 | 1 | 1 | 1 | 0 | 0 |
| **DeepSeek V4** | 2 ($0.30) | 4 | **5** | **5** | 4 | 3 | 4 | 2 | 2 | 0 | 0 |
| **MiniMax-M2.7** | 2 ($0.30) | 3 | 4 | 4 | 3 | 3 | 3 | 3 | 2 | 0 | 0 |
| **Grok-3 Mini** | 2 ($0.30) | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 4 | 4 | 0 |
| **GLM-4.7** | 3 ($0.39) | 3 | 4 | 4 | 4 | 4 | 3 | 3 | 2 | 0 | 0 |
| **DeepSeek R1** | 3 ($0.55) | **5** | 4 | 4 | 3 | 3 | 4 | 2 | 3 | 0 | 0 |
| **Kimi K2.5** | 3 ($0.60) | 4 | 3 | 3 | **5** | 3 | 4 | 3 | 3 | 3 | 0 |
| **Gemini 2.5 Pro** | 4 ($1.25) | 5 | 4 | 5 | 5 | 4 | 4 | 4 | 3 | 0 | 0 |
| **Mistral Large 3** | 4 ($2.00) | 4 | 3 | 4 | 3 | 4 | 3 | 3 | 3 | 0 | 0 |
| **Qwen-Max** | 4 ($2.00) | 4 | 4 | 4 | 3 | 4 | 4 | 3 | 2 | 0 | 0 |
| **Grok-3** | 4 ($3.00) | 4 | 4 | 4 | 3 | 3 | 3 | 4 | **5** | **5** | 0 |
| **Grok-4** | 4 ($3.00) | **5** | 5 | 5 | 4 | 4 | 4 | 4 | 5 | **5** | 0 |
| **gpt-5.3-codex** | 5 (finite) | 4 | **5** | **5** | 3 | 3 | 3 | 3 | 3 | 0 | 0 |
| **Claude Opus API** | 5 ($5.00) | **5** | 5 | 5 | 4 | **5** | 4 | 5 | 4 | 0 | 0 |

### Top Performers by Task (cost-adjusted)

| Task | Best value pick | Premium pick |
|------|----------------|-------------|
| T1 Strategic reasoning | DeepSeek R1 ($0.55) or DeepSeek V4 ($0.30) | Claude Opus (free) |
| T2 Code generation | DeepSeek V4 ($0.30) or Grok-Code-Fast-1 ($0.20) | gpt-5.3-codex |
| T3 Code review / QA | DeepSeek V4 ($0.30) or Codestral ($0.30) | gpt-5.3-codex |
| T4 Long-context research | Qwen-Plus ($0.26, 1M ctx) or Kimi K2.5 ($0.60, web search) | Gemini 2.5 Pro (1M ctx) |
| T5 Business writing | Claude Sonnet (free) | Claude Opus (free) |
| T6 Financial analysis | DeepSeek R1 ($0.55) — reasoning chain | Claude Opus (free) |
| T7 Creative / video | Claude Sonnet (free) | Claude Opus (free) |
| T8 Contrarian / debate | Grok-3-Mini ($0.30) | Grok-4 ($3) |
| T9 Web / X research | Grok-4.1 ($0.20 + search) | Grok-4 ($3 + search) |
| T10 Local / private | gemma4:26b (free, local) | gemma4:26b only |

---

## Revised Agent Model Recommendations (post-research)

Based on this matrix, some original recommendations can be improved:

| Agent | Previous | Updated | Reason |
|-------|---------|---------|--------|
| Senior Engineer | MiniMax-M2.7 → DeepSeek V3 | **DeepSeek V4** | New release (Mar 2026): 1M context, 81% SWE-bench, same $0.30/M tier |
| Engineer | Codex → MiniMax | Codex → **Grok-Code-Fast-1** → MiniMax-M2.7 | Code-specialist Grok as middle tier; MiniMax now $0.30/M |
| QA Bot | DeepSeek V3 | **DeepSeek V4 or Codestral** | V4 better scores; Codestral worth testing for pure code review |
| Researcher | DeepSeek | **Grok-4.1 ($0.20, web search)** → Kimi K2.5 ($0.60, web search) | Both have web search; Grok cheaper primary, Kimi as fallback |
| Finance | DeepSeek | **DeepSeek R1** → Kimi K2.5 | R1 for reasoning chain; Kimi now $0.60 (corrected) — excellent fallback analyst |
| Council Contrarian | Grok-3 | **Grok-3 (unchanged)** | Grok-4 is premium option; Grok-3 Mini as budget fallback |
| Council CH (Kimi) | Kimi K2.5 ($2.50) | **Kimi K2.5 ($0.60 corrected)** | Pricing was 4x wrong; Kimi now excellent value — confirmed for this role |

> These are recommendations to consider — final decisions belong in LLM-MATRIX.md after Greg's review.

---

## Update Schedule

This file should be refreshed weekly. Run the model research agent with prompt:
> "Research all major AI providers (Anthropic, OpenAI, Google, xAI, Mistral, DeepSeek, Moonshot, MiniMax, Qwen, GLM) for new models and pricing changes in the past 7 days. Update MODEL-RESEARCH.md."

Track: new model releases, pricing changes, free tier changes, context window updates, new capabilities.
