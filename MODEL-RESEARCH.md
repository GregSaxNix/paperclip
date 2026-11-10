# Life Admin — Model Research Database

**Purpose:** Comprehensive matrix of all available AI models × all agent task types. Used to inform and update LLM-MATRIX.md.  
**Update cadence:** Weekly provider and pricing pass, every Monday 9:00 AM AEST, via Task Scheduler task `Model Lineup Monitor` (`scripts/check_model_lineups.py`). That run posts an issue to the Researcher. Local weights on this PC are reviewed quarterly, on the first Monday of January, April, July, and October (next: January 2027).  
**Last updated:** 2026-11-10 (full provider and pricing pass from official provider pages; gemma4:12b/26b local entries added 2026-06-07; schedule corrected 2026-10-06)

### Changes in the 10 November 2026 pass

Every price below was read from the provider's own pricing or models page on 10 November 2026, unless a row says otherwise. The previous full pass was 6 April 2026, so most lineups had moved on.

- **Anthropic:** Claude 5 family added (Fable 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5). Haiku 4.5 price corrected to $1/$5 (was $0.80/$4). Sonnet 4.6 context corrected to 1M. The Messages API removed `temperature`, `top_p` and `top_k` in API version `2026-10-21`.
- **OpenAI:** GPT-6 family added. `gpt-5.3-codex` is deprecated (API shutdown 1 April 2027; already deprecated in Codex when signed in with ChatGPT). `o4-mini` retired 23 October 2026. `o3` shuts down 11 December 2026. `gpt-4o` and `gpt-4o-mini` snapshots shut down 14 January 2027.
- **Google:** Gemini 4 Argon, 3.8 Flash, 3.6 Flash and 3.5 Flash-Lite added. Gemini 2.5 Pro and 2.5 Flash are deprecated and route to newer models on 1 December 2026. 2.5 Flash and Flash-Lite prices corrected. Gemini 2.0 Flash shut down 1 June 2026.
- **xAI:** Grok 4.7, 4.6, 4.5, 4.3, 4.20 and Build 0.1 added. Grok-4 (`grok-4-0709`), Grok-4.1 Fast, Grok-3 and Grok-Code-Fast-1 retired 15 May 2026 (their slugs still answer, redirected and billed at Grok 4.3 prices).
- **Mistral:** Large 4 and Ministral 3 added; prices now published. Large 3 deprecated; Medium 3, Magistral 1.2 and Nemo retired.
- **DeepSeek:** API now offers `deepseek-flash` (V4.1 Flash) and `deepseek-v4-pro` only, with peak and off-peak prices.
- **Moonshot:** Kimi K3.1 Pro and K3 added. The whole K2 series retires by the end of December 2026; K2.5 is no longer on the price list.
- **MiniMax:** M3 and M3.1-Flash added. M2.7 is no longer on the price list.
- **Qwen:** Qwen3.8-Max, Qwen3.7-Plus and Qwen3.8-Flash added (International region, USD).
- **GLM:** GLM-5.3, 5.3-Flash, 5.3-FlashX, 5.2, 5.1 and 5 prices added; GLM-4.x prices corrected. Z.ai's API is OpenAI-compatible.
- **Agents affected (for Greg's review in LLM-MATRIX.md, not changed here):** the Engineer chain (`gpt-5.3-codex`, Grok-Code-Fast-1, MiniMax-M2.7), the Researcher (Grok-4.1), the Council Contrarian (Grok-3) and Council CH (Kimi K2.5) all point at models that are retired, deprecated or off the price list.

**Companion files:**
- [LLM-MATRIX.md](./LLM-MATRIX.md) — position assignments and fallback chains
- [MODEL-PROMPTING-GUIDELINES.md](./MODEL-PROMPTING-GUIDELINES.md) — per-model prompt-engineering rules (URL, JSON mechanism, delimiters, temperature, worked example, anti-patterns). **Refreshed in the same weekly pass as this file.**

---

## All Available Models (API access, last 6 months)

### Anthropic — Claude

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Claude Fable 5.2 (`claude-fable-5-2`) | 1M | $8.00 | $40.00 | Yes | Yes (adaptive, always on) | Via claude_local | **New.** For demanding reasoning and long-horizon agentic work. Default effort `high`. Max output 128K. Retirement not sooner than 9 November 2027. |
| Claude Opus 5.5 (`claude-opus-5-5`) | 1M | $4.00 | $20.00 | Yes | Yes (adaptive, always on) | Via claude_local | **New.** Anthropic's recommended starting model. Default effort `medium`. Max output 128K. |
| Claude Sonnet 5.5 (`claude-sonnet-5-5`) | 1M | $2.00 | $10.00 | Yes | Yes (adaptive) | Via claude_local | **New.** Speed and intelligence balance. Default effort `high`. Max output 128K. |
| Claude Haiku 5.5 (`claude-haiku-5-5`) | 1M | $0.10 (prompts up to 100K) / $0.50 (over 100K) | $0.50 / $2.50 | Yes | Yes (adaptive, can be disabled at low to high effort) | Via claude_local | **New.** For classification, extraction and routing. Default effort `medium`. Price depends on prompt length. |
| Claude Opus 4.6 | 1M | $5.00 | $25.00 | Yes | Yes | Via claude_local | Legacy (still active). Retirement not sooner than 5 February 2027. |
| Claude Sonnet 4.6 | 1M | $3.00 | $15.00 | Yes | Yes | Via claude_local | Legacy (still active). Context corrected from 200K to 1M. Retirement not sooner than 17 February 2027. |
| Claude Haiku 4.5 | 200K | $1.00 | $5.00 | Yes | No | Via claude_local | Legacy (still active). **Price corrected** (was $0.80/$4.00). |
| ~~Claude Sonnet 4.5~~ | n/a | $3.00 | $15.00 | n/a | n/a | n/a | **Deprecated. Retires 30 November 2026.** Replacement: `claude-sonnet-5-5`. |

> All Claude models are FREE via Greg's Anthropic Max plan. No API key needed; use the claude_local adapter. API prices are listed for comparison. Also active but not listed: Fable 5.1, Fable 5, Opus 5, Opus 4.8, Opus 4.7, Sonnet 5, Opus 4.5, and the limited-access Mythos models. Source: [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [Pricing](https://platform.claude.com/docs/en/about-claude/pricing), [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

---

### OpenAI — GPT / Codex

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| GPT-6 Astra (`gpt-6-astra`) | 1.05M | $10.00 | $50.00 | Yes | Yes (low to max; no `none`) | Yes | **New.** OpenAI flagship for complex reasoning and coding. Cached input $1.00. Max output 128K. Also in Codex. |
| GPT-6.1 Sol (`gpt-6.1-sol`) | 1.05M | $2.00 | $10.00 | Yes | Yes (low to max; default medium) | Yes | **New.** Balance of intelligence and cost. Cached input $0.10. Codex config example uses this model. |
| GPT-6.1 Terra (`gpt-6.1-terra`) | 1.05M | $1.00 | $5.00 | Yes | Yes (none to max; default medium) | Yes | **New.** Fast and efficient. Cached input $0.05. Needs Codex CLI 0.159.0 or later. |
| GPT-6 Luna (`gpt-6-luna`) | 1.05M | $0.10 | $0.50 | Yes | Yes (supports `none`) | Yes | **New.** Cost-sensitive, high-volume work. Cached input $0.01. Replacement for GPT-4o and GPT-4o mini. |
| GPT-6 Sol (`gpt-6-sol`) | Not checked | $2.00 | $10.00 | Not checked | Yes | Yes | Earlier GPT-6 Sol; still on the price list. Cached input $0.20. Named as the replacement for `gpt-5.3-codex`. |
| GPT-5.6 Sol / Terra / Luna | Not checked | $4.00 / $2.00 / $0.20 | $20.00 / $12.00 / $1.20 | Not checked | Yes | Yes | Previous generation; still on the price list. |
| gpt-5.3-codex | N/A | **Weekly quota** (API $1.75) | **Weekly quota** (API $14.00) | No | Yes | codex_local | **Deprecated.** API shutdown 1 April 2027 (replacement `gpt-6-sol`). Already deprecated in Codex when signed in with ChatGPT; update `codex exec --model` and config files. |
| GPT-4o | 128K | $2.50 | $10.00 | Yes | No | Yes | **Deprecated.** Snapshots `gpt-4o-2024-08-06` and `-11-20` shut down 14 January 2027 (replacement `gpt-6-luna`). `gpt-4o-2024-05-13` shut down 23 October 2026. |
| GPT-4o mini | 128K | $0.15 | $0.60 | Yes | No | Yes | **Deprecated.** Shuts down 14 January 2027 (replacement `gpt-6-luna`). |
| ~~o4-mini~~ | n/a | n/a | n/a | n/a | n/a | n/a | **Retired 23 October 2026.** Replacement was `gpt-5.6-terra`. |
| o3 | 200K | $2.00 | $8.00 | Yes | Yes | Yes | **Deprecated.** Shuts down 11 December 2026 (replacement `gpt-5.6-sol`). Price corrected (was $10/$40). |

> OpenAI API key is SEPARATE from ChatGPT Plus Codex OAuth; safe to add. Codex now offers `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra` and `gpt-6-luna`. Source: [Models](https://developers.openai.com/api/docs/models), [Pricing](https://developers.openai.com/api/docs/pricing), [Deprecations](https://developers.openai.com/api/docs/deprecations), [Codex models](https://learn.chatgpt.com/docs/models).

---

### Google — Gemini

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Gemini 4 Argon (`gemini-4-argon`) | 1M | $2.00 to 30 Nov 2026; **$4.00 from 1 Dec 2026** | $10.00; **$20.00 from 1 Dec 2026** | Yes | Yes (low, medium, high; default medium) | Via gemini_local | **New.** Flagship reasoning model. Not on the free tier. |
| Gemini 3.8 Flash (`gemini-3.8-flash`) | Not stated | $0.75 to 31 Dec 2026; **$1.50 from 1 Jan 2027** | $3.75; **$7.50 from 1 Jan 2027** | Yes | Yes (low, medium, high; default medium) | Via gemini_local | **New.** Most capable Flash. Gemini 2.5 Pro traffic routes here on 1 December 2026. `gemini-3.7-flash` already routes here. |
| Gemini 3.6 Flash (`gemini-3.6-flash`) | Not stated | $0.75 to 31 Dec 2026; **$1.50 from 1 Jan 2027** | $3.75; **$7.50 from 1 Jan 2027** | Yes | Yes (minimal to high; default medium) | Via gemini_local | **New.** Previous-generation Flash, stable. `gemini-3.5-flash` now routes here. |
| Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`) | Not stated | $0.30 | $2.50 | Yes | Yes (minimal to high; default minimal) | Via gemini_local | **New.** Cheapest current 3.x text model. Gemini 2.5 Flash traffic routes here on 1 December 2026. |
| Gemini 3.1 Flash-Lite (`gemini-3.1-flash-lite`) | Not stated | $0.25 | $1.50 | Yes | Yes | Via gemini_local | Stable. **Shuts down 7 May 2027** (replacement 3.5 Flash-Lite). |
| Gemini 3.1 Pro preview (`gemini-3.1-pro-preview`) | Not stated | $2.00 (up to 200K) / $4.00 | $12.00 / $18.00 | Yes | Yes (low, medium, high; default high) | Via gemini_local | Preview. No shutdown date announced. |
| ~~Gemini 3.5 Flash~~ (`gemini-3.5-flash`) | n/a | n/a | n/a | n/a | n/a | n/a | **Superseded.** Endpoint routes automatically to `gemini-3.6-flash`. |
| Gemini 2.5 Pro | 1M | $1.25 | $10.00 | Yes | Yes | Via gemini_local | **Deprecated.** Requests route to `gemini-3.8-flash` on 1 December 2026 (and get 3.8 Flash pricing). |
| Gemini 2.5 Flash | 1M | $0.30 | $2.50 | Yes | Yes | Via gemini_local | **Deprecated.** Requests route to `gemini-3.5-flash-lite` on 1 December 2026. **Price corrected** (was $0.15/$0.60). |
| Gemini 2.5 Flash-Lite | 1M | $0.10 | $0.40 | Yes | Off by default | Via gemini_local | Legacy: served only to existing users; no shutdown date. **Price corrected** (was $0.075/$0.30). |
| ~~Gemini 2.0 Flash~~ | n/a | n/a | n/a | n/a | n/a | n/a | **Retired. Shut down 1 June 2026.** |

> Greg's global default for user apps (Gemini 2.5 Flash-Lite, then 2.5 Flash, then 2.5 Pro) is affected: 2.5 Flash and 2.5 Pro silently switch model and price on 1 December 2026. Source: [Pricing](https://aistudio.google.com/docs/pricing), [Models](https://aistudio.google.com/docs/models), [Deprecations](https://aistudio.google.com/docs/deprecations), [Thinking](https://aistudio.google.com/docs/thinking).

---

### Google — Gemma (open-weights, local via Ollama)

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| gemma4:12b (local) | 256K | FREE | FREE | Yes | No | Via ollama_local | **New — released 2026-06-03.** Multimodal (text/image/audio); ~8GB VRAM at Q4_K_M; tool calling; Apache 2.0. Faster/lighter than 26b. |
| gemma4:26b (local) | 256K | FREE | FREE | Yes | No | Via ollama_local | Stronger local Gemma (MoE); ~17GB VRAM. Doc/Freud LOCAL-ONLY model. Emergency fallback for everyone else is gemma4:12b. |

> Both run free on the RTX 4090 via the `ollama_local` adapter — private, on-device, always available. Prompt rules: see [MODEL-PROMPTING-GUIDELINES.md § Google — Gemma 4](./MODEL-PROMPTING-GUIDELINES.md). Gemma has **no system role** and enforces JSON via Ollama's `format` schema param (not Gemini's `response_schema`).

---

### xAI — Grok

| Model | Context | Input /M | Output /M | Vision | Web Search | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|------------|---------------|-------|
| Grok 4.7 (`grok-4.7`) | 500K | $2.00 (under 200K) / $4.00 | $6.00 / $12.00 | Not checked | `web_search` via Responses API | Yes (api.x.ai/v1) | **New.** Newest Grok. Reasoning always on (low, medium, high, xhigh; default high). |
| Grok 4.6 (`grok-4.6`) | 500K | $2.00 / $4.00 | $6.00 / $12.00 | Not checked | Via Responses API | Yes | **New.** Same reasoning options as 4.7. |
| Grok 4.5 (`grok-4.5`) | 500K | $2.00 / $4.00 | $6.00 / $12.00 | Not checked | Via Responses API | Yes | **New.** Reasoning low, medium, high (xhigh treated as high). |
| Grok 4.3 (`grok-4.3`) | 1M | $1.25 / $2.50 | $2.50 / $5.00 | Not checked | Via Responses API | Yes | **New.** Cheapest current Grok. Redirect target for most retired Grok slugs. |
| Grok 4.20 (`grok-4.20-0309-reasoning`, `-non-reasoning`, `grok-4.20-multi-agent-0309`) | 1M | $1.25 / $2.50 | $2.50 / $5.00 | Not checked | Via Responses API | Yes | **New.** Multi-agent variant uses reasoning effort to set agent count. |
| Grok Build 0.1 (`grok-build-0.1`) | 256K | $1.00 / $2.00 | $2.00 / $4.00 | Not checked | Not checked | Yes | **New.** Agentic coding model; replacement for Grok-Code-Fast-1. |
| ~~Grok-4~~ (`grok-4-0709`) | n/a | n/a | n/a | n/a | n/a | n/a | **Retired 15 May 2026.** Redirects to Grok 4.3 (low effort), billed at Grok 4.3 prices. |
| ~~Grok-4.1 Fast~~ (`grok-4-1-fast-reasoning`, `-non-reasoning`) | n/a | n/a | n/a | n/a | n/a | n/a | **Retired 15 May 2026.** Redirects to Grok 4.3. |
| ~~Grok-3~~ | n/a | n/a | n/a | n/a | n/a | n/a | **Retired 15 May 2026.** Redirects to Grok 4.3 (no reasoning). |
| ~~Grok-Code-Fast-1~~ | n/a | n/a | n/a | n/a | n/a | n/a | **Retired 15 May 2026.** Redirects to `grok-build-0.1`. |
| Grok-3 Mini, Grok-3-fast | n/a | n/a | n/a | n/a | n/a | n/a | Not on xAI's models page (10 November 2026) and not in its retirement notice. Status not confirmed; do not rely on them. |

> Prices switch to the higher figure for the whole request once the prompt reaches 200K tokens. Retired slugs still answer without errors, so check bills: they are charged at Grok 4.3 rates ($1.25/$2.50). The old tool-call pricing note ($2.50 to $5 per 1,000 search calls) was not re-checked this pass. Source: [Models](https://docs.x.ai/docs/models), [15 May retirement](https://docs.x.ai/developers/migration/may-15-retirement), [Reasoning](https://docs.x.ai/developers/model-capabilities/text/reasoning).

---

### Mistral

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Mistral Large 4 (`mistral-large-4-0`, v26.10) | Not stated | $0.70 | $2.10 | Not checked | Yes (low, medium, high) | No (own SDK) | **New.** Flagship. Cached input $0.07. Third-party sites quote other prices; the figure here is Mistral's own page. |
| Mistral Small 4 (`mistral-small-2603`, v26.03) | Not stated | $0.15 | $0.60 | Yes | Yes (high or none) | No | Output price now published. Cached input $0.015. |
| Ministral 3 14B / 8B / 3B (v25.12) | Not stated | $0.20 / $0.15 / $0.10 | $0.20 / $0.15 / $0.10 | Not checked | Not checked | No | **New.** Small open models. |
| Codestral (v25.08) | 256K (not re-checked) | $0.30 | $0.90 | No | No | No | Code specialist. Cached input $0.03. |
| Mistral Large 3 (`mistral-large-2512`) | n/a | n/a | n/a | n/a | n/a | n/a | **Deprecated 31 October 2026. Retires 30 April 2027.** Replacement Large 4. No longer on the price list. |
| Mistral Medium 3.5 (`mistral-medium-3-5`) | n/a | n/a | n/a | n/a | Yes | n/a | **Deprecated 31 October 2026. Retires 30 April 2027.** Replacement Large 4. |
| ~~Mistral Medium 3~~ | n/a | n/a | n/a | n/a | n/a | n/a | **Retired 31 August 2026.** |
| ~~Magistral Medium 1.2 / Small 1.2~~ | n/a | n/a | n/a | n/a | n/a | n/a | **Retired 31 July 2026.** |
| ~~Mistral Nemo~~ | n/a | n/a | n/a | n/a | n/a | n/a | **Retired 31 July 2026.** Replacement Ministral 3 8B. |

> Mistral now also resells Z.ai GLM 5.3 ($1.40/$4.40) and GLM 5.3 Flash ($0.15/$0.50), and DeepSeek V4.1 Flash ($0.30/$1.20). Source: [API pricing](https://mistral.ai/pricing/api), [Models and deprecations](https://docs.mistral.ai/getting-started/models/models_overview/), [Reasoning](https://docs.mistral.ai/studio-api/conversations/reasoning).

---

### DeepSeek

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| DeepSeek V4.1 Flash (`deepseek-flash`, serves DeepSeek-V4.1-Flash-1017) | 1M | $0.30 peak / $0.15 off-peak | $1.20 peak / $0.60 off-peak | Yes | Yes (thinking on by default; low, high, max) | Yes | **New.** Cache-hit input $0.006 peak / $0.003 off-peak. Max output 384K. |
| DeepSeek V4 Pro (`deepseek-v4-pro`, serves DeepSeek-V4-Pro-0813) | 1M | $1.32 peak / $0.66 off-peak | $3.96 peak / $1.98 off-peak | No | Yes | Yes | **New.** Cache-hit input $0.044 peak / $0.022 off-peak. |
| ~~DeepSeek V4 Flash~~ (`deepseek-v4-flash`, `deepseek-v4-flash-vision-exp`) | n/a | n/a | n/a | n/a | n/a | n/a | **Retired.** Names still accepted; served by V4.1 Flash at Flash prices. |
| DeepSeek V3.2 (`deepseek-chat`), R1 (`deepseek-reasoner`) | n/a | n/a | n/a | n/a | n/a | n/a | **Not on DeepSeek's API docs any more.** Third-party reports say both names were retired 24 July 2026; not confirmed on DeepSeek's own site. Treat as unavailable. |

> Off-peak prices (half of peak) apply outside 01:00 to 04:00 and 06:00 to 10:00 UTC on weekdays, and all weekend and Chinese public holidays. In Brisbane time, peak is 11:00 am to 2:00 pm and 4:00 pm to 8:00 pm, Monday to Friday. DeepSeek also offers an Anthropic-compatible endpoint at `https://api.deepseek.com/anthropic`. Source: [Models and pricing](https://api-docs.deepseek.com/quick_start/pricing), [Quick start](https://api-docs.deepseek.com/).

---

### Moonshot — Kimi

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Kimi K3.1 Pro (`kimi-k3.1-pro`) | 1M | $2.00 | $10.00 | Yes (text, image, video) | Yes (always on; low, high, max; default max) | Yes | **New.** Moonshot's flagship. Cached input $0.20. Batch is 60% of standard price. |
| Kimi K3.1 Pro Highspeed (`kimi-k3.1-pro-highspeed`) | 1M | $4.00 | $20.00 | Yes | Yes | Yes | **New.** 2 to 3 times faster. Cached input $0.20. |
| Kimi K3 (`kimi-k3`) | 1M | $3.00 | $15.00 | Yes | Yes | Yes | **New.** Cached input $0.30. |
| Kimi K2.7 Code (`kimi-k2.7-code`) | 262K | $0.95 | $4.00 | Yes | Not checked | Yes | K2 series: **retires by end of December 2026**; closed to new sign-ups from 31 October 2026. Highspeed variant $1.90/$8.00. |
| Kimi K2.6 (`kimi-k2.6`) | 262K | $0.95 | $4.00 | Yes | Not checked | Yes | K2 series: **retires by end of December 2026**. Cached input $0.16. |
| Kimi K2.5 | n/a | n/a | n/a | n/a | n/a | n/a | **No longer on Kimi's price list** (10 November 2026). Part of the K2 series being retired. |

> Moonshot's developer site moved to platform.kimi.ai; the API base URL is still `https://api.moonshot.ai/v1`. Source: [Pricing](https://platform.kimi.ai/docs/pricing/chat), [K3.1 Pro quick start](https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart).

---

### MiniMax

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| MiniMax-M3.1-Flash | 1M | $0.15 | $0.60 | Yes (text, image, video) | Yes (always on; low to max; default max) | Yes (also Anthropic-compatible, recommended) | **New.** Latest M-series model. Cache read $0.015. |
| MiniMax-M3 | 1M | $0.30 (up to 512K) / $0.60 | $1.20 / $2.40 | Yes | Yes (always on) | Yes | **New.** Shown at a permanent 50% off. Priority tier costs 1.5 times (`service_tier: priority`). Cache read $0.06. |
| MiniMax-M2.7 | n/a | n/a | n/a | n/a | n/a | n/a | **No longer on MiniMax's price list** (10 November 2026); no deprecation notice found. Status not confirmed. |

> Base URLs: `https://api.minimax.io/anthropic` (Anthropic-compatible, recommended) or `https://api.minimax.io/v1` (OpenAI-compatible). The old "OpenAI-compat: No" entry was wrong. Source: [Pricing](https://platform.minimax.io/docs/guides/pricing), [Text generation](https://platform.minimax.io/docs/guides/text-generation).

---

### Alibaba — Qwen

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| Qwen3.8-Max (`qwen3.8-max`) | Up to 1M (pricing tier) | $2.00 | $6.00 | Not checked | Yes (hybrid; on by default) | Yes | **New.** Top Qwen for complex reasoning and coding. International (Singapore) price. |
| Qwen3.7-Max (`qwen3.7-max`) | Up to 1M | $2.50 | $7.50 | Not checked | Yes | Yes | **New.** Previous Max. |
| Qwen3.7-Plus (`qwen3.7-plus`) | Up to 1M | $0.40 (up to 256K) / $1.20 | $1.60 / $4.80 | Not checked | Yes (hybrid; on by default) | Yes | **New.** List price; limited-time 20% off at time of check. |
| Qwen3.8-Flash (`qwen3.8-flash`) | Up to 1M | $0.15 | $0.47 | Not checked | Yes (hybrid; on by default) | Yes | **New.** Fast, low cost. |
| Qwen3.7-Flash (`qwen3.7-flash`) | Up to 1M | $0.03 (up to 32K) / $0.10 / $0.20 | $0.13 / $0.40 / $0.80 | Not checked | Not checked | Yes | **New.** Cheapest current Qwen; three prompt-length tiers. |
| Qwen 2.5-Max, Qwen-Turbo | n/a | n/a | n/a | n/a | n/a | n/a | **Not in the International price tables** (10 November 2026). Status not confirmed; use the Qwen3.7 or 3.8 models instead. |
| Qwen-Plus, Qwen2.5 72B | Not re-checked | Not re-checked | Not re-checked | No | No | Yes | Old prices from April 2026, not re-checked this pass. Qwen-Plus is still listed but its International USD row was not read. |
| qwen3.8:27b (local via Ollama) | 256K | FREE | FREE | Yes | Yes | Yes | Coding/agent local model on the RTX 4090. Replaces Qwen2.5 and Qwen3 32B. |

> `qwen3.8:27b` is the local Qwen on this machine: free, private, about 18 GB. Run it on its own.  
> Cloud Qwen uses the OpenAI-compatible endpoint `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` for the International (Singapore) region. Source: [Model pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing), [Models](https://www.alibabacloud.com/help/en/model-studio/models).

---

### Zhipu AI — GLM

| Model | Context | Input /M | Output /M | Vision | Reasoning | OpenAI-compat | Notes |
|-------|---------|---------|---------|--------|-----------|---------------|-------|
| GLM-5.3 (`glm-5.3`) | 1M | $1.40 | $4.40 | No (text only) | Yes (always on; low, high, max; default max) | Yes | **New.** Max output 128K. Cached input $0.26. |
| GLM-5.3-Flash | 1M (per Mistral's listing) | $0.15 | $0.50 | Not checked | Yes | Yes | **New.** Cached input $0.03. |
| GLM-5.3-FlashX | Not stated | $0.37 | $1.25 | Not checked | Not checked | Yes | **New.** A `-Legal` variant has the same price. |
| GLM-5.2 / GLM-5.1 | Not stated | $1.40 | $4.40 | Not checked | Yes | Yes | **New.** Mistral retired its resold GLM 5.2 on 31 October 2026; Z.ai still lists it. |
| GLM-5 | Not stated | $1.00 | $3.20 | Yes | Yes | Yes | Prices now published. |
| GLM-4.7 | 200K (not re-checked) | $0.60 | $2.20 | No | No | Yes | **Price corrected** (was $0.39/$1.75). |
| GLM-4.7-FlashX | Not stated | $0.07 | $0.40 | Not checked | Not checked | Yes | **New.** |
| GLM-4.7-Flash | 200K (not re-checked) | **FREE** | **FREE** | Yes | No | Yes | **Free.** Good for bulk/simple tasks |
| GLM-4.5 | Not stated | $0.60 | $2.20 | Yes | No | Yes | Unchanged. |
| GLM-4.5-Air / AirX | Not stated | $0.20 / $1.10 | $1.10 / $4.50 | Not checked | Not checked | Yes | **New** to this file. |
| GLM-4.5-Flash | Not stated | **FREE** | **FREE** | Yes | No | Yes | **Free.** Flash variant |
| GLM-4.5-X | Not stated | $2.20 | $8.90 | Yes | Yes | Yes | Input price now published. |

> GLM-4.5-Flash and GLM-4.7-Flash are FREE: useful for high-volume simple tasks.  
> **Correction:** Z.ai's international API is OpenAI-compatible (`https://api.z.ai/api/paas/v4/`) and also offers an Anthropic-compatible endpoint (`https://api.z.ai/api/anthropic`). The earlier "not OpenAI-compatible" note referred to the old open.bigmodel.cn API. Source: [Pricing](https://docs.z.ai/guides/overview/pricing), [GLM-5.3](https://docs.z.ai/guides/llm/glm-5.3).

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

> **Status, 10 November 2026:** these scores were set on 6 April 2026 and have not been re-scored; no new model has scores yet. Rows marked *(retired)* or *(deprecated)* point at models that are gone or going (see the provider tables above). Re-scoring needs evals, not guesses, so it is left for a separate task.

| Model | Cost rank | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | T10 |
|-------|-----------|----|----|----|----|----|----|----|----|----|----|
| **Claude Opus 4.6** | 1 (free) | **5** | 5 | 5 | 4 | **5** | 4 | 5 | 4 | 0 | 0 |
| **Claude Sonnet 4.6** | 1 (free) | 4 | 4 | 4 | 4 | **5** | 4 | **5** | 3 | 0 | 0 |
| **Claude Haiku 4.5** | 1 (free) | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 2 | 0 | 0 |
| **gemma4:26b (local)** | 1 (free) | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 0 | **5** |
| **GLM-4.7-Flash** | 1 (free) | 2 | 3 | 3 | 4 | 3 | 3 | 2 | 1 | 0 | 0 |
| **Gemini 2.5 Flash** *(deprecated)* | 2 ($0.15) | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 2 | 0 | 0 |
| **Mistral Small 4** | 2 ($0.15) | 3 | 4 | 4 | 3 | 4 | 3 | 3 | 2 | 0 | 0 |
| **Grok-4.1** *(retired)* | 2 ($0.20) | 4 | 4 | 4 | 4 | 3 | 3 | 3 | 4 | 4 | 0 |
| **Grok-Code-Fast-1** *(retired)* | 2 ($0.20) | 2 | **5** | **5** | 2 | 2 | 2 | 1 | 1 | 0 | 0 |
| **Qwen2.5 72B** | 2 ($0.23) | 3 | 4 | 4 | 4 | 3 | 3 | 3 | 2 | 0 | 0 |
| **DeepSeek V3.2** *(retired, unconfirmed)* | 2 ($0.26) | 4 | **5** | **5** | 3 | 3 | 4 | 2 | 2 | 0 | 0 |
| **Qwen-Plus** | 2 ($0.26) | 3 | 4 | 4 | **5** | 4 | 3 | 3 | 2 | 0 | 0 |
| **Codestral** | 2 ($0.30) | 1 | **5** | **5** | 2 | 1 | 1 | 1 | 1 | 0 | 0 |
| **DeepSeek V4** *(V4 Flash retired; V4 Pro active)* | 2 ($0.30) | 4 | **5** | **5** | 4 | 3 | 4 | 2 | 2 | 0 | 0 |
| **MiniMax-M2.7** *(off price list)* | 2 ($0.30) | 3 | 4 | 4 | 3 | 3 | 3 | 3 | 2 | 0 | 0 |
| **Grok-3 Mini** *(status unconfirmed)* | 2 ($0.30) | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 4 | 4 | 0 |
| **GLM-4.7** | 3 ($0.39) | 3 | 4 | 4 | 4 | 4 | 3 | 3 | 2 | 0 | 0 |
| **DeepSeek R1** *(retired, unconfirmed)* | 3 ($0.55) | **5** | 4 | 4 | 3 | 3 | 4 | 2 | 3 | 0 | 0 |
| **Kimi K2.5** *(off price list; K2 retiring)* | 3 ($0.60) | 4 | 3 | 3 | **5** | 3 | 4 | 3 | 3 | 3 | 0 |
| **Gemini 2.5 Pro** *(deprecated)* | 4 ($1.25) | 5 | 4 | 5 | 5 | 4 | 4 | 4 | 3 | 0 | 0 |
| **Mistral Large 3** *(deprecated)* | 4 ($2.00) | 4 | 3 | 4 | 3 | 4 | 3 | 3 | 3 | 0 | 0 |
| **Qwen-Max** | 4 ($2.00) | 4 | 4 | 4 | 3 | 4 | 4 | 3 | 2 | 0 | 0 |
| **Grok-3** *(retired)* | 4 ($3.00) | 4 | 4 | 4 | 3 | 3 | 3 | 4 | **5** | **5** | 0 |
| **Grok-4** *(retired)* | 4 ($3.00) | **5** | 5 | 5 | 4 | 4 | 4 | 4 | 5 | **5** | 0 |
| **gpt-5.3-codex** *(deprecated)* | 5 (finite) | 4 | **5** | **5** | 3 | 3 | 3 | 3 | 3 | 0 | 0 |
| **Claude Opus API** | 5 ($5.00) | **5** | 5 | 5 | 4 | **5** | 4 | 5 | 4 | 0 | 0 |

### Top Performers by Task (cost-adjusted)

> **Status, 10 November 2026:** set on 6 April 2026 and not re-scored. Many picks below are now retired or deprecated (Grok-Code-Fast-1, Grok-3, Grok-4, Grok-4.1, DeepSeek R1 and V3.2, gpt-5.3-codex, Gemini 2.5 Pro). Check the provider tables before acting on them.

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
| T10 Local / private | gemma4:12b (free, local) | gemma4:26b (Doc/Freud) |

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

> These are recommendations to consider; final decisions belong in LLM-MATRIX.md after Greg's review.  
> **Status, 10 November 2026:** most "Updated" picks in this table now point at a retired, deprecated or delisted model (DeepSeek R1, Grok-Code-Fast-1, Grok-4.1, Grok-3, Kimi K2.5, MiniMax-M2.7, gpt-5.3-codex). "DeepSeek V4" now means V4 Pro or V4.1 Flash; Codestral is still active; Grok-3 Mini is unconfirmed. This table needs Greg's review against the current provider tables; it has not been rewritten here.

---

## Update Schedule

`Model Lineup Monitor` runs every Monday at 9:00 AM and posts the weekly research issue to the Researcher. The task used to be every four weeks, so this file stopped being refreshed. Refresh this file in that Monday pass, alongside [MODEL-PROMPTING-GUIDELINES.md](./MODEL-PROMPTING-GUIDELINES.md). The issue prompt is:
> "Research all major AI providers (Anthropic, OpenAI, Google, xAI, Mistral, DeepSeek, Moonshot, MiniMax, Qwen, GLM) for new models and pricing changes in the past 7 days. Update MODEL-RESEARCH.md AND MODEL-PROMPTING-GUIDELINES.md."

Track: new model releases, pricing changes, free tier changes, context window updates, new capabilities.

The first Monday of January, April, July, and October adds the quarterly local-model review (RTX 4090, 24 GB). That review checks whether a newly released open model should replace `gemma4:12b`, `gemma4:26b`, `qwen3.8:27b`, `gpt-oss:20b`, or `llama3.2`. Leave `nomic-embed-text` installed.

**For every new model added here, the same weekly run MUST add a section to MODEL-PROMPTING-GUIDELINES.md** (provider docs URL, JSON mechanism, delimiter prefs, temperature, worked example, anti-patterns). Use `python scripts/update_llm_matrix.py --guidelines-stale` to verify nothing is missed.
