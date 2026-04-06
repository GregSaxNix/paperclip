# Life Admin — LLM Job Interview Matrix

**Purpose:** Assign the best-fit LLM to each agent role based on required capabilities and cost.  
**Approach:** "Job interview" — each position has a description, models rated on fit and cost.  
**Last updated:** 2026-04-06

> ⚠️ **Codex weekly limit hit (2026-04-06):** Engineer and CTO fall back to Grok-Code-Fast-1 → MiniMax-M2.7 until weekly Codex reset. See Codex Usage Monitoring section.

> 📋 **Companion file:** [MODEL-RESEARCH.md](./MODEL-RESEARCH.md) — full model × task suitability matrix, provider comparisons, Codex monitoring design. Update weekly.

---

## Available Models (researched 2026-04-06 — see MODEL-RESEARCH.md for full matrix)

| Provider | Model | Input /M | Output /M | Adapter | Key Strength |
|----------|-------|---------|---------|---------|-------------|
| Anthropic (Max) | Claude Opus 4.6 | **FREE** | **FREE** | claude_local | Best reasoning overall |
| Anthropic (Max) | Claude Sonnet 4.6 | **FREE** | **FREE** | claude_local | Balanced, fast, highly capable |
| Anthropic (Max) | Claude Haiku 4.5 | **FREE** | **FREE** | claude_local | Ultra-fast, structured tasks |
| Local Ollama | gemma4:26b | **FREE** | **FREE** | ollama_local | Private, on-device, always available |
| Qwen (local) | Qwen2.5-7B/14B | **FREE** | **FREE** | ollama_local | Runs on RTX 4090; private Qwen option |
| GLM (Zhipu) | GLM-4.5-Flash / 4.7-Flash | **FREE** | **FREE** | ollama_local + apiKey | Free flash models; basic/simple tasks |
| Qwen (Alibaba) | Qwen-Turbo | $0.05 | $0.15 | ollama_local + apiKey | Ultra-cheap simple tasks |
| Mistral | Mistral Nemo | $0.02 | — | ollama_local + apiKey | Cheapest Mistral; minimal tasks |
| GLM (Zhipu) | GLM-4.7 | $0.39 | $1.75 | ollama_local + apiKey | Strong generalist; 200K context |
| Google | Gemini 2.5 Flash | $0.15 | $0.60 | gemini_local | Fast, multimodal, 1M context, thinking mode |
| Mistral | Mistral Small 4 | $0.15 | — | ollama_local + apiKey | **New (2026):** reasoning + multimodal + coding unified |
| xAI | Grok-4.1 | $0.20 | $0.50 | ollama_local + apiKey | 131K context; vision; web+X search; best value |
| xAI | Grok-Code-Fast-1 | $0.20 | $1.50 | ollama_local + apiKey | **Coding specialist**; cheaper than Grok-3 |
| Qwen (Alibaba) | Qwen2.5 72B | $0.23 | $0.23 | ollama_local + apiKey | 1/10th GPT-4o cost; solid all-rounder |
| DeepSeek | DeepSeek V3.2 | $0.26 | $0.38 | ollama_local + apiKey | **Best code + analysis at lowest price** |
| Qwen (Alibaba) | Qwen-Plus | $0.26 | $0.78 | ollama_local + apiKey | 1M context; excellent value |
| xAI | Grok-3 Mini | $0.30 | $0.50 | ollama_local + apiKey | Cheap Grok reasoning |
| Mistral | Codestral | $0.30 | $0.90 | ollama_local + apiKey | Code specialist from Mistral |
| DeepSeek | DeepSeek V4 | $0.30 | $0.50 | ollama_local + apiKey | **New (Mar 2026):** 1M context, 81% SWE-bench, multimodal |
| MiniMax | MiniMax-M2.7 | $0.30 | $1.20 | ollama_local + apiKey | 205K context; code + content generalist |
| DeepSeek | DeepSeek R1 | $0.55 | $2.19 | ollama_local + apiKey | Chain-of-thought reasoning |
| Kimi (Moonshot) | Kimi K2.5 | $0.60 | $2.50 | ollama_local + apiKey | **Long-context analyst; web search ($0.005/call)** |
| Qwen (Alibaba) | Qwen-Max | $2.00 | $6.00 | ollama_local + apiKey | Top Qwen; strong reasoning |
| Google | Gemini 2.5 Pro | $1.25 | $10.00 | gemini_local | Best Gemini; 1M context; use sparingly |
| Mistral | Mistral Large 3 | $2.00 | $6.00 | ollama_local + apiKey | Rigorous reasoning, multilingual |
| xAI | Grok-3 | $3.00 | $15.00 | ollama_local + apiKey | Bold, web-aware, contrarian |
| xAI | Grok-4 | $3.00 | $15.00 | ollama_local + apiKey | Premium Grok reasoning |
| OpenAI | gpt-5.3-codex | **Weekly quota** | — | codex_local | Best code generation; treat carefully |
| OpenAI | GPT-4o / o4-mini | $2.50 / $1.10 | — | Via API key | Worth evaluating after 1 week Codex tracking |

> ⚠️ **Gemini 2.0 Flash is DEPRECATED** — shutting down June 1, 2026. Replaced by Gemini 2.5 Flash above.  
> **OpenAI API key:** Completely separate from Codex OAuth auth — safe to add after tracking quota for 1 week.  
> **Grok web/X search:** Built-in `x_search` and `web_search` via Responses API ($2.50–5 per 1K calls). Available for any agent, not just Council Contrarian.  
> **Qwen local:** Qwen2.5-7B and 14B run on the RTX 4090 via Ollama — free and private.  
> **Kimi K2.5 pricing corrected:** $0.60/$2.50 per million tokens (was incorrectly documented as $2.50/$10).  
> **MiniMax M2.7 pricing corrected:** $0.30/$1.20 per million tokens (was $0.80/$2.40).  
> **Full model × task scores:** See [MODEL-RESEARCH.md](./MODEL-RESEARCH.md)

---

## OpenRouter — Recommended for Multi-Provider Management

**OpenRouter** (openrouter.ai) provides a single OpenAI-compatible API gateway to 167+ models from all providers above. No markup on pricing — identical to going direct.

**Why use it:**
- One API key instead of 10+ individual provider keys
- Built-in model fallback chains (configure in request, not code)
- Auto-router selects best model for the task automatically
- Unified interface — swap models via parameter, not code changes
- BYOK (bring your own keys): 1M requests/month free, then 5% fee

**Endpoint:** `https://openrouter.ai/api/v1/chat/completions` (OpenAI-compatible)

**Recommendation:** Use OpenRouter as the primary gateway for all cloud agents (Grok, Mistral, DeepSeek, Kimi, MiniMax, Qwen, GLM). Continue using `claude_local` (free Max plan) and `gemini_local` directly. This reduces provider key management from ~8 keys to 2 (OpenRouter + local adapters).

---

## Ollama Cloud (new — September 2025)

Ollama now offers hosted cloud inference at $20/month (Pro) or $100/month (Max). Fixed subscription, not per-token. Runs on NVIDIA infrastructure, same models as local Ollama.

**Not recommended for Greg's setup** — the RTX 4090 already handles local inference for free. Ollama Cloud is valuable for machines without GPUs. Note: the existing `ollama_local` adapter points to localhost and won't work with Ollama Cloud without a new adapter or proxy.

---

## Guiding Principles

1. **Cheapest model that meets the bar** — no overspending on luxury models for simple tasks
2. **Free tier first:** Claude Opus/Sonnet/Haiku (Max) ≫ gemma4:26b (local, always available) ≫ Qwen2.5 local
3. **Cost tiers:** GLM-Flash/Mistral-Nemo (free-$0.02) > DeepSeek/Grok-Code/Grok-4.1/Gemini-Flash/Mistral-Small4 (~$0.14–0.30) > Kimi/DeepSeek-R1/MiniMax (~$0.30–0.60) > Mistral-Large/Qwen-Max (~$2) > Grok-3/4 (~$3)
4. **Expensive last:** Gemini Pro, gpt-5.3-codex — only for tasks only they can do
5. **Codex fallback chain (⚠️ active now — weekly limit hit):** Codex → Grok-Code-Fast-1 → MiniMax-M2.7 → gemma4:26b
6. **Universal emergency fallback:** Every agent must have gemma4:26b as absolute last resort ("limp mode")
7. **Doc/Freud:** gemma4:26b LOCAL ONLY — no exceptions. Health data never leaves the machine
8. **Grok models:** Full lineup available; Grok-3 for contrarian/web research, Grok-Code-Fast-1 for coding, Grok-4.1 Fast for long-context
9. **OpenRouter:** Recommended for multi-provider management — single key for Grok, Mistral, DeepSeek, Kimi, MiniMax, Qwen, GLM
10. **Weekly research update:** MODEL-RESEARCH.md should be refreshed weekly to track new models and pricing changes

---

## Confirmed Model Assignments (by department)

### Executive

| Agent | Role | Primary | Fallback 1 | Fallback 2 (emergency) |
|-------|------|---------|-----------|------------------------|
| Clawdy | CEO | Claude Opus | Claude Sonnet | gemma4:26b |
| Gayan | CTO | Claude Opus | Grok-Code-Fast-1 → MiniMax | gemma4:26b |
| COO | COO | Claude Sonnet | Mistral-large | gemma4:26b |

> **CTO role:** Receives and assesses CEO's instructions/plans, orchestrates work to engineering and design teams, reviews completed work against brief, then reports outcomes back to CEO. Model needs strong reasoning + code-awareness.

### Technology & Engineering

| Agent | Role | Primary | Fallback 1 | Fallback 2 |
|-------|------|---------|-----------|------------|
| Senior Engineer | Engineering | DeepSeek V4 *(1M ctx, 81% SWE)* | Grok-Code-Fast-1 → DeepSeek V3.2 | gemma4:26b |
| Engineer | Engineering | gpt-5.3-codex ⚠️ *quota* | Grok-Code-Fast-1 → MiniMax-M2.7 | gemma4:26b |
| QA Bot | Code review / testing | DeepSeek V4 | Codestral → Claude Haiku | gemma4:26b |
| Designer | UI/UX | Claude Sonnet | Gemini 2.5 Flash | gemma4:26b |

> ⚠️ **Active now:** Codex weekly limit hit. Engineer uses Grok-Code-Fast-1 → MiniMax-M2.7 until quota resets.  
> **Senior Engineer:** DeepSeek V4 (Mar 2026) — $0.30/M, 1M context, 81% SWE-bench. Upgraded from V3. MiniMax-M2.7 now $0.30/M (corrected from $0.80). See MODEL-RESEARCH.md.

### Business Operations

| Agent | Role | Primary | Fallback 1 | Fallback 2 |
|-------|------|---------|-----------|------------|
| Content Lead | Writing / comms | Claude Sonnet | Mistral-large | gemma4:26b |
| Accountant | Finance / bookkeeping | Claude Haiku | DeepSeek | gemma4:26b |
| Spielberg | Video content | Claude Sonnet | Grok-3-mini | gemma4:26b |

### Finance & Investments *(new agent)*

| Agent | Role | Primary | Fallback 1 | Fallback 2 |
|-------|------|---------|-----------|------------|
| Finance | Portfolio / budget | DeepSeek R1 | Kimi K2.5 *(long docs)* | gemma4:26b |

### Family & Health *(local only)*

| Agent | Role | Primary | Fallback | Hard constraint |
|-------|------|---------|---------|-----------------|
| Doc | Health / NDIS / family | gemma4:26b local | **NONE** | LOCAL ONLY — no cloud |
| Freud | Psychiatrist specialist | gemma4:26b local | **NONE** | LOCAL ONLY — no cloud |

### Travel & Lifestyle *(new agent)*

| Agent | Role | Primary | Fallback 1 | Fallback 2 |
|-------|------|---------|-----------|------------|
| Travel Agent | Gypsy years planning | Claude Sonnet | Kimi K2.5 *(long docs, web search)* | gemma4:26b |

### Research

| Agent | Role | Primary | Fallback 1 | Fallback 2 |
|-------|------|---------|-----------|------------|
| Researcher | Cross-dept research | Grok-4.1 *(131K, web search)* | Kimi K2.5 *(web search, analyst)* | gemma4:26b |

---

## Council of Elders (on-demand only — no heartbeat)

Council members renamed from model names to role-based titles.

| New Name | Old Name | Model | Fallback | Role |
|----------|----------|-------|---------|------|
| Yoda | Yoda | Claude Opus | Claude Sonnet → gemma4:26b | Judge — synthesises debate into recommendation |
| Council Contrarian | Skeptic | Grok-3 | Grok-3-mini → gemma4:26b (contrarian prompting) | Devil's advocate — challenges assumptions |
| Council Local | Gemma | gemma4:26b local | *none (always available)* | Local voice — free, grounded, private |
| Council EU | Mistral | Mistral Large 3 | Mistral Small 4 → gemma4:26b | European balanced perspective |
| Council CH | Kimi | Kimi K2.5 | DeepSeek → gemma4:26b | Deep analyst — long-context specialist |
| Council Tech | Codex | gpt-5.3-codex | MiniMax-M2.7 → gemma4:26b | Technical / code perspective |

> **On Gemma as contrarian fallback:** Gemma (gemma4:26b) CAN be prompted in a contrarian/adversarial style via the system prompt. It's less sophisticated than Grok-3 for this but workable as an emergency fallback. The instructions for Council Contrarian should include a contrarian-mode prompt that Gemma can follow if Grok is unavailable.

> **Council Contrarian note:** Renamed from "Skeptic" to "Council Contrarian" for consistency. Agent in Paperclip will be renamed accordingly.

---

## Position Job Descriptions (for SOUL.md writing)

### Clawdy — CEO
Orchestrates the entire Life Admin operation. Receives priorities from Greg, breaks work into actionable tasks, assigns to appropriate agents, monitors progress, and synthesises outcomes. Makes or escalates high-stakes decisions. Primary interface between Greg and the agent team.

### Gayan — CTO
Receives and critiques the CEO's technical instructions. Designs technical architecture, orchestrates engineering and design work, reviews completed deliverables against spec, and reports outcomes to Clawdy. Bridge between business strategy and technical execution.

### COO
Manages day-to-day operational flow. Coordinates Shine wind-down activities, tracks project status, handles communications and scheduling, and ensures nothing falls through the cracks. Reports to Clawdy.

### Senior Engineer
Primary builder. Takes architectural plans from CTO and builds software, writes code, creates scripts. Owns complex implementations. Reports to Gayan.

### Engineer
Second engineer. Handles Codex-specific tasks, supplementary coding, parallel workstreams. Falls back to MiniMax when ChatGPT Plus weekly quota is exhausted. Reports to Gayan.

### QA Bot
Reviews code, writes tests, identifies bugs, checks regressions. Works with both engineers to maintain code quality. Reports to Gayan.

### Designer
UI/UX design thinking for Paperclip and other projects. Produces component specs, colour/type decisions, design system guidance. Reports to Gayan (or Clawdy for non-tech design).

### Content Lead
Business writing: proposals, Shine comms, job ads, social posts, client correspondence. Adapts tone for recruitment/HR contexts. Reports to COO.

### Accountant
Bookkeeping, invoicing, expense tracking, financial reporting for Shine. Reports to COO.

### Spielberg
Video content planning, scripting, shot lists, YouTube strategy, travel content planning. Reports to COO (or Clawdy for personal content).

### Finance *(new)*
Personal finance: share portfolio (ASX/ETFs), superannuation, travel budget, investment research, quarterly summaries. Reports directly to Greg/Clawdy.

### Doc
Family and health coordinator (LOCAL ONLY). Manages NDIS admin, general health tracking, appointment scheduling, wellbeing journaling for Greg, Tegan, Lana, Kobi. Refers complex psychological/psychiatric cases to Freud. Never uses cloud models.

### Freud
Psychiatrist/psychologist specialist (LOCAL ONLY). Receives referrals from Doc. Handles psychological wellbeing support, ADHD/autism specialist guidance, mental health journaling. Never uses cloud models.

### Travel Agent *(new)*
Plans the gypsy years. Accommodation research, visa requirements, route planning, itinerary building, logistics, packing, remote work setup at each destination. Reports directly to Greg/Clawdy.

### Researcher
Cross-department research. Performs market intelligence, topic deep-dives, synthesises long documents, briefs other agents. On-call for any department.

---

## Codex Usage Monitoring (design — implementation pending)

**Goal:** Monitor weekly Codex quota, calculate daily allowed fraction, auto-swap Engineer to MiniMax when limit approached.

**Daily budget formula:** `daily_allowed = weekly_quota × (day_of_week / 7)`  
e.g. Monday (day 1) = 1/7 of weekly quota. Friday (day 5) = 5/7. This prevents front-loading consumption.

**Monitoring approach (researching):**
- The usage page at `https://chatgpt.com/codex/settings/usage` requires ChatGPT login (OAuth cookies)
- Not scrapeable with simple HTTP requests — requires browser session (Playwright/Puppeteer) or cookie-based auth
- OpenAI does NOT expose a public Codex-specific usage API (separate from billing API)
- Possible approach: Python script with saved session cookies → scrapes page → writes quota state to a JSON file → Paperclip reads this file on each Codex agent invocation
- Alternative: manual weekly tracking + `lineups.json` switch command to Greg

**Status:** Pending research agent results. Implementation will be a separate task.

---

## Investigations Completed (2026-04-06)

| Topic | Finding | Decision |
|-------|---------|---------|
| Qwen models | Qwen-Plus ($0.26/M, 1M context), Qwen2.5 72B ($0.23/M), Turbo ($0.05/M). Local Qwen2.5-7B/14B via Ollama free. | Add Qwen-Plus as long-context fallback for Researcher/Travel |
| GLM models | GLM-4.5-Flash and GLM-4.7-Flash FREE. GLM-5 launched Feb 2026 with 30–60% price hike. | Free flash models usable for bulk/simple tasks; GLM-5 too expensive |
| OpenRouter | 167+ models, no markup, BYOK option, built-in fallback chains | ✅ Recommended for multi-provider key management |
| Full model matrix | See MODEL-RESEARCH.md — all providers × all tasks scored | Updated agent recommendations above |
| Ollama Cloud | $20–100/month fixed. NVIDIA-hosted. Same models as local. | Not needed — Greg has RTX 4090. Local is free. |
| Grok full lineup | Grok-3/4 ($3/M, vision), Grok-4.1 ($0.20, 131K, vision, web search), Grok-Code-Fast-1 ($0.20, code), Grok-3-Mini ($0.30) | Grok-Code-Fast-1 for coding fallback; Grok-4.1 for research. Note: 2M context claim was incorrect — confirmed 131K. |
| Codex monitoring | ChatGPT usage page needs Playwright auth scraping. No official API. Design in MODEL-RESEARCH.md. | Implement as separate task: `check_codex_quota.py` |
| OpenAI API key | Completely safe to add — separate from Codex OAuth. GPT-4o, o4-mini, o3 available. | Add after 1 week Codex quota tracking to benchmark value |
| Kimi K2.5 pricing | **CORRECTED:** $0.60/$2.50 per million tokens (was documented as $2.50/$10 — 4x error). Caching reduces to $0.15/M input. | Kimi much more competitive than previously estimated; confirmed for Finance fallback + Council CH |
| MiniMax M2.7 pricing | **CORRECTED:** $0.30/$1.20 per million tokens (was $0.80/$2.40). 205K context, two variants (standard + highspeed). | More competitive as fallback option; keep for Engineer fallback chain |
| DeepSeek V4 | New March 2026. $0.30/$0.50, 1M context, 81% SWE-bench, multimodal gen, hybrid reasoning. Replaces V3. | Upgrade Senior Engineer + QA Bot primary to DeepSeek V4 |
| Gemini 2.0 Flash | **DEPRECATED** — shutting down June 1, 2026. | Removed from matrix. Use Gemini 2.5 Flash instead. |
| Mistral Small 4 | New 2026. $0.15/M. Unifies Magistral (reasoning) + Pixtral (multimodal) + Devstral (agentic coding). | Add as fallback option. Council EU fallback: Mistral Large 3 → Mistral Small 4. |

---

## Next Steps

1. ✅ Council agents renamed in Paperclip (done 2026-04-06)
2. Greg reviews and approves model assignments above (particularly Senior Engineer → DeepSeek V3, Researcher → Grok-4.1 Fast)
3. Decide on OpenRouter — set up single API key to replace multiple provider keys
4. Implement Codex usage monitoring script (`check_codex_quota.py`) — separate task
5. Create Finance and Travel Agent with full instructions
6. Strategic wake-up once matrix is approved
7. Refresh MODEL-RESEARCH.md weekly (run model research agent Monday mornings)
