# Life Admin — Per-Model Prompt Engineering Guidelines

**Purpose:** Capture each model's official prompt-engineering guidance so that code calling that model uses ITS optimal structure, not a generic prompt. Writing one "generic" prompt that we reuse across models leaves accuracy on the table for every model.

**Cross-reference:** Global rule at `C:\Users\Administrator\.claude\CLAUDE.md` Part 15 (Per-Model Prompt Engineering). Companion files: [MODEL-RESEARCH.md](./MODEL-RESEARCH.md), [LLM-MATRIX.md](./LLM-MATRIX.md).

**Update cadence:** Weekly, in the same Monday pass as `MODEL-RESEARCH.md`. Task Scheduler `Model Lineup Monitor` (Monday 9:00 AM) posts the Researcher issue that starts the pass. The Researcher re-validates URLs, flags sections >6 months old, and adds sections for any newly-released model versions. See [Maintenance contract](#maintenance-contract) at the bottom.

**Refresh threshold:** Any section with a `Date captured` older than 6 months is auto-flagged stale by `python scripts/update_llm_matrix.py --guidelines-stale`.

**Trigger phrase:** `check model guidelines for <model>` — opens this file, prints the section's key rules + worked example. If section is missing or stale, auto-fetch the provider's docs and refresh.

---

## Table of contents

| Provider | Model versions | Section | Status |
|----------|----------------|---------|--------|
| Anthropic | Claude Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.2 (legacy notes for 4.6 / 4.5) | [§ Anthropic Claude](#anthropic--claude-opus-55--sonnet-55--haiku-55--fable-52) | Filled 2026-11-10 |
| Google | Gemini 4 Argon, 3.8 Flash, 3.6 Flash, 3.5 Flash-Lite | [§ Google Gemini 4 / 3.8 / 3.6](#google--gemini-4-argon--38-flash--36-flash--35-flash-lite) | Filled 2026-11-10 |
| Google | Gemini 3.5 Flash (now routes to 3.6), 3.1 Flash-Lite, 3.1 Pro (preview) | [§ Google Gemini 3.x](#google--gemini-35-flash--31-flash-lite--31-pro-preview) | Filled 2026-05-20; status note 2026-11-10 |
| Google | Gemini 2.5 Pro, Flash, Flash-Lite (deprecated / legacy) | [§ Google Gemini 2.5](#google--gemini-25-pro--flash--flash-lite) | Filled 2026-05-18; status note 2026-11-10 |
| Google | Gemma 4 12B / 26B (local via Ollama) | [§ Google Gemma 4](#google--gemma-4-12b--26b-local-via-ollama) | Filled 2026-06-07 |
| DeepSeek | V4.1 Flash (`deepseek-flash`), V4 Pro | [§ DeepSeek](#deepseek--v41-flash--v4-pro) | Filled 2026-11-10 |
| Moonshot | Kimi K3.1 Pro, K3 (K2 series retiring) | [§ Kimi](#moonshot--kimi-k31-pro--k3) | Filled 2026-11-10 |
| xAI | Grok 4.7, 4.6, 4.5, 4.3, Build 0.1 | [§ xAI Grok](#xai--grok-47--46--45--43--build-01) | Filled 2026-11-10 |
| OpenAI | GPT-6 Astra, 6.1 Sol, 6.1 Terra, 6 Luna (API and Codex) | [§ OpenAI](#openai--gpt-6-astra--61-sol--61-terra--6-luna-api-and-codex) | Filled 2026-11-10 |
| Mistral | Large 4, Small 4, Ministral 3, Codestral | [§ Mistral](#mistral--large-4--small-4--ministral-3--codestral) | Filled 2026-11-10 |
| Alibaba | Qwen3.8-Max, Qwen3.7-Plus, Qwen3.8-Flash | [§ Qwen](#alibaba--qwen38-max--qwen37-plus--qwen38-flash) | Filled 2026-11-10 |
| Zhipu AI | GLM-5.3, GLM-5.3-Flash, GLM-4.7 | [§ GLM](#zhipu-ai--glm-53--glm-53-flash--glm-47) | Filled 2026-11-10 |
| MiniMax | MiniMax-M3.1-Flash, M3 | [§ MiniMax](#minimax--m31-flash--m3) | Filled 2026-11-10 |
---

## Anthropic — Claude Opus 5.5 / Sonnet 5.5 / Haiku 5.5 / Fable 5.2

**Provider docs URL:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices + https://platform.claude.com/docs/en/build-with-claude/structured-outputs + https://platform.claude.com/docs/en/build-with-claude/effort
**Date captured:** 2026-11-10
**Applies to model IDs:** `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-fable-5-2`. Legacy notes cover `claude-opus-4-6`, `claude-sonnet-4-6` and `claude-haiku-4-5-20251001`.

Each current model also has its own prompting page, which lists where it differs from the general guide: [Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5), [Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5), [Haiku 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5), [Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2). Read the one for your model first.

**What changed since the 18 May 2026 capture:** prefill is gone (400 error from Claude 4.6 onwards), `temperature`, `top_p` and `top_k` were removed in API version `2026-10-21`, `budget_tokens` thinking returns a 400 error from Claude 4.7 onwards, and JSON now has a GA structured-outputs parameter. The old advice to set `temperature=0` and to prefill `{` no longer works.

### 1. Prompt structure recommendations

1. **System prompt:** the role. Anthropic: "Setting a role in the system prompt focuses Claude's behavior and tone for your use case. Even a single sentence makes a difference."
2. **Long data first.** For inputs of 20K+ tokens, put documents "near the top of your prompt, above your query, instructions, and examples". Anthropic reports "Queries at the end can improve response quality by up to 30 percent in tests". Wrap each document in `<document>` with `<source>` and `<document_content>` subtags inside `<documents>`.
3. **`<instructions>`:** numbered steps when order or completeness matters. Explain why a rule exists; "Claude can generalize from the explanation."
4. **`<examples>`:** "Include 3–5 examples for best results", each in its own `<example>` tag, relevant and varied.
5. **`<input>`:** the item to process.
6. **The ask, last.**

Other current rules:
- "Tell Claude what to do instead of what not to do."
- Set the system prompt once per conversation. On the 5.5 models and Fable 5.2, editing earlier messages or rebuilding `system` or `tools` between requests invalidates later thinking blocks, and resending them can return a 400 error. Put new instructions in the newest turn or a mid-conversation system message, and keep history append-only.
- Opus 5.5: mark text the user pasted from elsewhere with `<pasted_content id="...">` tags plus the system-prompt note Anthropic gives on the Opus 5.5 page, so instructions inside pasted text are not followed.
- Give a search-enabled model today's date ("The current date is {{current_date}}.").

### 2. JSON output mechanism

1. **Structured outputs (preferred):** `output_config.format` with `type: "json_schema"`. GA, no beta header. Supported on all current models, Opus 4.5 to 4.8, Sonnet 4.5 and 4.6, and Haiku 4.5. The old `output_format` parameter is deprecated and needs the `structured-outputs-2025-11-13` beta header.
   - Not supported (400 error): numeric constraints (`minimum`, `maximum`), string length constraints, recursive schemas, and `additionalProperties` other than `false`. Use `enum` for bounded values.
   - Check `stop_reason`: `"max_tokens"` can give truncated JSON and `"refusal"` can give non-matching output. Treat both as failures and retry.
   - Enum values may differ only in letter case, so compare case-insensitively.
   - The first request with a new schema is slower (compiled grammars are cached for 24 hours). Changing the schema invalidates the prompt cache.
2. **A tool with an enum field:** Anthropic's prefill migration note says "For classification tasks, use either tools with an enum field containing your valid labels or structured outputs." Add `strict: true` on the tool to validate its inputs.
3. **No prefill.** "Starting with Claude 4.6 models ... prefilled responses ... on the last assistant turn are no longer supported. Requests with prefilled assistant messages to these models return a 400 error."

Model quirks:
- **Haiku 5.5, thinking off, plus JSON output:** it may skip a tool call it needs. Keep adaptive thinking, remove `output_config.format` when a tool must be called, or force the call with `tool_choice`.
- **Sonnet 5.5, JSON answers that need working out (totals, rules, ranking):** with adaptive thinking, end the system prompt with "Think the problem through before you answer." Do not use `between_tools` for these requests.

### 3. Delimiter preferences

**XML tags.** "Wrapping each type of content in its own tag (for example, `<instructions>`, `<context>`, `<input>`) reduces misinterpretation." Use consistent, descriptive names and nest when content has a hierarchy.

### 4. Classification task framing

- Put the allowed labels in a schema `enum` (structured outputs) or a strict tool's enum. Anthropic positions Haiku 5.5 "For high-volume, latency-sensitive tasks such as classification, extraction, and routing."
- Describe each label and each score level in the system prompt. (Anchor descriptions per level carried over from the May 2026 capture; not re-verified this pass.)
- For multi-label tasks, use an array of enum values and say "include all that apply" (carried over from the May 2026 capture).

### 5. Temperature default & quirks

- **No sampling parameters.** `temperature`, `top_p` and `top_k` were removed in API version `2026-10-21` and return a 400 error. Earlier API versions return a 400 when they are set to non-default values on Claude 4.7 and later. Steer with the prompt and with effort.
- **Effort is the main control:** `output_config.effort` with `low`, `medium`, `high`, `xhigh` or `max`. Defaults: Fable 5.2 `high`, Opus 5.5 `medium`, Sonnet 5.5 `high`, Haiku 5.5 `medium`. Anthropic says lowering effort reduces thinking "more reliably than prompt instructions do".
- **Thinking is adaptive.** Opus 5.5 and Fable 5.2: always on (`thinking: {type: "disabled"}` returns 400 on Opus 5.5). Sonnet 5.5: the lowest setting is `thinking: {type: "between_tools"}`, accepted at `high` effort or below. Haiku 5.5: can be turned off at `low`, `medium` and `high` only.
- **`max_tokens` must leave room for thinking**, which counts toward it even when not shown. For agentic coding Anthropic suggests 128,000 with streaming.
- Changing top-level effort between requests invalidates the prompt cache; a per-message effort change (beta) keeps it.
- Pass thinking blocks back unchanged in multi-turn and tool use. Read responses by block type; the first block may be `thinking`.
- **Refusals:** safety classifiers return `stop_reason: "refusal"` with `stop_details.category`. Do not ask the model to write out its reasoning in the reply; that invites `reasoning_extraction` refusals. Use `display: "summarized"` thinking instead.
- **Caching:** cache hits cost 5% of base input on Opus 5.5 and Sonnet 5.5, 10% on Haiku 5.5.
- **Legacy:** `budget_tokens` still works on Opus 4.6 and Sonnet 4.6 but is deprecated. Haiku 4.5 predates effort levels.

### 6. Worked example

```python
import json
import anthropic

client = anthropic.Anthropic()

CLAUSE_TYPES = ["indemnification", "limitation_of_liability", "termination",
                "confidentiality", "ip_ownership", "payment_terms", "warranty",
                "data_protection", "non_compete", "force_majeure",
                "governing_law", "auto_renewal", "other"]

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=4096,                      # thinking counts toward this; leave room
    system=(
        "You are a contract clause classifier for a legal review team. "
        "Risk levels: 1 = boilerplate, 2 = mildly unusual, 3 = noteworthy, "
        "4 = material exposure, 5 = escalate to a partner."
    ),
    output_config={
        "effort": "low",                  # high-volume classification
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "clause_type": {"type": "string", "enum": CLAUSE_TYPES},
                    "risk_score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                    "rationale": {"type": "string"},
                },
                "required": ["clause_type", "risk_score", "rationale"],
                "additionalProperties": False,
            },
        },
    },
    messages=[{
        "role": "user",
        "content": (
            "<instructions>\n"
            "1. Read the clause inside <input>.\n"
            "2. Choose exactly one clause_type.\n"
            "3. Score risk using the levels in your instructions.\n"
            "4. Give a one-sentence rationale.\n"
            "</instructions>\n"
            "<examples>\n"
            "<example><input>Either party may terminate with 30 days notice.</input>"
            "<output>{\"clause_type\": \"termination\", \"risk_score\": 2, "
            "\"rationale\": \"Mutual 30-day termination is standard.\"}</output></example>\n"
            "<example><input>Supplier indemnifies Customer for ALL losses including "
            "consequential and indirect damages without cap.</input>"
            "<output>{\"clause_type\": \"indemnification\", \"risk_score\": 5, "
            "\"rationale\": \"Uncapped indemnity including consequentials needs escalation.\"}</output></example>\n"
            "</examples>\n"
            "<input>Customer indemnifies Supplier against any third-party IP claims "
            "arising from Customer's modifications to the Software.</input>\n"
            "Classify the clause in <input>."
        ),
    }],
)

if response.stop_reason in ("max_tokens", "refusal"):
    raise RuntimeError(f"Classification failed: {response.stop_reason}")
text = next(block.text for block in response.content if block.type == "text")
result = json.loads(text)
```

### 7. Known anti-patterns

- **Don't** send `temperature`, `top_p` or `top_k`: 400 error on API version `2026-10-21`.
- **Don't** prefill the assistant turn: 400 error from Claude 4.6 onwards.
- **Don't** use `thinking.budget_tokens` on Claude 4.7 or later (400), or `thinking: disabled` on Opus 5.5 (400), or `between_tools` at `xhigh`/`max` on Sonnet 5.5 (400).
- **Don't** size `max_tokens` as if there were no thinking; replies get cut off.
- **Don't** try to cut thinking with "answer directly" instructions; lower effort instead.
- **Don't** ask for the reasoning in the reply text; it can trigger `reasoning_extraction` refusals.
- **Don't** edit earlier turns, or rebuild `system` or `tools`, partway through a conversation.
- **Don't** put `minimum`/`maximum` or `minLength`/`maxLength` in a structured-outputs schema (400).
- **Don't** put user text inside a `tool_result` block; the 5.5 models may treat it as a prompt injection.
- **Don't** leave long documents untagged or after the question.

---

## Google — Gemini 4 Argon / 3.8 Flash / 3.6 Flash / 3.5 Flash-Lite

**Provider docs URL:** https://aistudio.google.com/docs/prompting-strategies + https://aistudio.google.com/docs/structured-output + https://aistudio.google.com/docs/thinking
**Date captured:** 2026-11-10
**Applies to model IDs:** `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.6-flash`, `gemini-3.5-flash-lite`. Also `gemini-3.1-pro-preview` and `gemini-3.1-flash-lite` where noted.

Google's Gemini docs moved from ai.google.dev to aistudio.google.com (old links redirect). Gemini 2.5 Pro and 2.5 Flash route to 3.8 Flash and 3.5 Flash-Lite on 1 December 2026, so prompts written for 2.5 will start running on these models whether or not the code changes.

### 1. Prompt structure recommendations

- **Long inputs: context first, question last.** Google: "supply all the context first. Place your specific instructions or questions at the very *end* of the prompt."
- Put essential constraints, persona and output format at the start of the system instruction or user prompt.
- After a large context block, use a transition phrase that links it to the question (for example "Based on the information above, ...").
- **Few-shot:** "We recommend to always include few-shot examples in your prompts." Use a few varied examples with identical structure (same tags, whitespace and newlines). Too many examples can make the model overfit. If the examples are clear, drop instructions they make redundant.
- Avoid "unnecessary or overly persuasive language".

### 2. JSON output mechanism

**`generateContent` (the `google-genai` SDK):** `config={"response_mime_type": "application/json", "response_json_schema": Model.model_json_schema()}`. In REST the same settings sit under `generationConfig.responseFormat.text` (`mimeType`, `schema`). The current page does not mention `response_schema`; treat it as the older name.

**Interactions API:** `response_format={"type": "text", "mime_type": "application/json", "schema": Model.model_json_schema()}`, read from `interaction.output_text`.

Limits:
- `minLength`, `maxLength`, `minProperties`, `maxProperties`, `uniqueItems`, `contains`, `minContains` and `maxContains` are silently stripped, not enforced. `minItems` and `maxItems` are enforced. Validate in code (for example Pydantic `model_validate_json`).
- Large or deeply nested schemas can be rejected with `400 INVALID_ARGUMENT`.
- Structured outputs plus built-in tools is a preview feature on Gemini 3 series models only.

### 3. Delimiter preferences

"XML-style tags (e.g., `<context>`, `<task>`) or Markdown headings are effective." Pick one style and keep it consistent within a prompt.

### 4. Classification task framing

- Put the allowed labels in the schema as an `enum` (via a Pydantic `Literal`); `enum` is not on the list of stripped keywords.
- Use few-shot examples to fix the format, phrasing and scope of the label; Google says examples are most useful for exactly that.

### 5. Temperature default & quirks

- **Gemini 4 and Gemini 3.6+ ignore `temperature`, `top_p` and `top_k`.** Remove them from requests; Google says sending them will return 400 errors in a future release.
- Gemini 3 models below 3.6 (by version number: 3.1 Pro preview, 3.1 Flash-Lite, 3 Flash preview, 3.5 Flash-Lite): keep these at their defaults "to avoid degraded reasoning performance".
- **Thinking is set with `thinking_level`.** Defaults and allowed values: Argon and 3.8 Flash on at `medium` (low, medium, high); 3.6 Flash on at `medium` (minimal to high); 3.5 Flash-Lite on at `minimal` (minimal to high); 3.1 Pro preview on at `high` (low, medium, high). The current Thinking page does not document `thinking_budget`.
- Do not ask for explicit reasoning steps by default; the model already reasons internally. For hard problems a cue such as "Think very hard before answering" adds thinking tokens.
- Leave head-room in `max_output_tokens` for thinking. (TalentMap finding from 20 May 2026 on 3.5 Flash: 800 tokens truncated 5 to 10% of JSON replies, 8000 fixed it. In-house result, not Google guidance.)
- **Price changes are scheduled:** Argon doubles on 1 December 2026; 3.8 Flash and 3.6 Flash double on 1 January 2027. See MODEL-RESEARCH.md.

### 6. Worked example

```python
from typing import Literal
from google import genai
from pydantic import BaseModel

class ClauseClassification(BaseModel):
    clause_type: Literal["indemnification", "limitation_of_liability", "termination",
                         "confidentiality", "ip_ownership", "payment_terms", "warranty",
                         "data_protection", "non_compete", "force_majeure",
                         "governing_law", "auto_renewal", "other"]
    risk_score: Literal[1, 2, 3, 4, 5]
    rationale: str

client = genai.Client()

prompt = """<examples>
<example>
<clause>Either party may terminate with 30 days notice.</clause>
<answer>{"clause_type": "termination", "risk_score": 2, "rationale": "Mutual 30-day termination is standard."}</answer>
</example>
<example>
<clause>Supplier indemnifies Customer for ALL losses without cap.</clause>
<answer>{"clause_type": "indemnification", "risk_score": 5, "rationale": "Uncapped indemnity needs escalation."}</answer>
</example>
</examples>

<clause>
Customer indemnifies Supplier against any third-party IP claims arising from
Customer's modifications to the Software.
</clause>

Based on the clause above, choose one clause_type, score its risk, and give a one-sentence rationale."""

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
    config={
        "system_instruction": (
            "You are a contract clause classifier. Risk: 1 = boilerplate, "
            "2 = mildly unusual, 3 = noteworthy, 4 = material exposure, 5 = escalate."
        ),
        "response_mime_type": "application/json",
        "response_json_schema": ClauseClassification.model_json_schema(),
        "max_output_tokens": 8000,       # head-room for thinking
    },
)
result = ClauseClassification.model_validate_json(response.text)
```

### 7. Known anti-patterns

- **Don't** send `temperature`, `top_p` or `top_k` to Gemini 4 or 3.6+ models; they are ignored now and will error later.
- **Don't** change sampling settings on earlier Gemini 3 models; keep the defaults.
- **Don't** mix XML and Markdown delimiters in one prompt, or format few-shot examples inconsistently.
- **Don't** pile on examples; too many cause overfitting.
- **Don't** rely on `minLength`, `maxLength` or similar schema keywords; they are stripped without an error.
- **Don't** use stop sequences that could appear in normal output.
- **Don't** repeat a failed tool call with the same arguments in an agent; change strategy after a non-transient error.
- **Don't** assume code pinned to `gemini-2.5-flash` or `gemini-2.5-pro` behaves the same after 1 December 2026; re-test on the routing targets.

---

## Google — Gemini 3.5 Flash / 3.1 Flash-Lite / 3.1 Pro (preview)

**Provider docs URL:** https://ai.google.dev/gemini-api/docs/prompting-strategies (Gemini 3 section) + https://ai.google.dev/gemini-api/docs/structured-output
**Date captured:** 2026-05-20
**Applies to model IDs:** `gemini-3.5-flash` (stable), `gemini-3.1-flash-lite` (stable), `gemini-3.1-pro-preview` (preview), `gemini-3-flash-preview` (preview)

**Status, 10 November 2026 (section not refreshed):** `gemini-3.5-flash` now routes automatically to `gemini-3.6-flash`. `gemini-3.1-flash-lite` shuts down on 7 May 2027. The temperature rule in section 5 does not apply to Gemini 3.6 and later, which ignore `temperature`, `top_p` and `top_k`. The prices in section 6 are from 20 May 2026. For new work use [§ Google Gemini 4 / 3.8 / 3.6 / 3.5 Flash-Lite](#google--gemini-4-argon--38-flash--36-flash--35-flash-lite). The TalentMap findings below are kept as history.

### 1. Prompt structure — same as 2.5 (context-first, question-last) but stricter

Same context-first / question-last pattern as Gemini 2.5. The transition phrase ("Based on the information above, answer the following:") is even more important on 3.x — anecdotal observation 2026-05-20 is that 3.5 Flash without the transition phrase is more prone to ignoring late-prompt overrides.

### 2. JSON output — `response_schema` works the same BUT budget for thinking

`response_schema` and `response_mime_type='application/json'` work identically to 2.5. The new operational gotcha:

**`max_output_tokens` must be ≥8000 for 3.x classification.** 3.5 Flash burns tokens on internal reasoning even when `thinking_budget` is not explicitly set. Observed at 800 tokens: ~5–10% of responses are JSON-truncated mid-value. At 8000, errors drop to zero. Real-world example from TalentMap classifier 2026-05-20 on 150-row sample: 3.5 Flash output ~500 tokens on average per call vs ~150 tokens for 2.5 Flash.

For reliable JSON on 3.x:
```python
config=types.GenerateContentConfig(
    temperature=1.0,                  # see §5 — non-optional for 3.x
    max_output_tokens=8000,           # not 800 — leave head-room for reasoning
    response_mime_type='application/json',
    response_schema=YourPydanticModel,
)
```

### 3. Delimiter preferences

Same as 2.5: XML for long contexts, markdown for short. No change.

### 4. Classification task framing

Same multiple-choice / enumerated-set advice as 2.5. 3.5 Flash returns slightly higher 6-digit rate (98.7%) vs the 4-digit honest-partial fallback that the prompt allows; this MAY be a regression in "stop when evidence is thin" behaviour vs 2.5 Flash (which returned 100% 6-digit on the same sample). Watch this on graded-confidence tasks.

### 5. Temperature default & quirks (the non-optional rule)

**3.x family MUST run at `temperature=1.0`.** Google's Gemini 3 prompting doc states this explicitly — any other value degrades output. This is the OPPOSITE of 2.5 (where 0 was best for structured extraction) and the OPPOSITE of every other provider.

Consequence: 3.x classification is non-deterministic by design. Two runs on the same input will not necessarily produce the same code. For audit-style use cases run N times and take majority vote.

3.x **does** support `thinking_config=types.ThinkingConfig(thinking_budget=N)` like 2.5 — but the "burn-on-reasoning" behaviour seen at 800 max_output_tokens happens even when thinking is not explicitly enabled. Setting `thinking_budget=0` may help reduce output cost but was not verified as of 2026-05-20.

### 6. Pricing (per 1M tokens, captured 2026-05-20)

| Model | Input | Output | Status |
|---|---:|---:|---|
| `gemini-3.5-flash` | $1.50 | $9.00 | stable |
| `gemini-3.1-flash-lite` | $0.25 | $1.50 | stable |
| `gemini-3.1-pro-preview` | $2.00 (≤200k) / $4.00 (>200k) | $12.00 / $18.00 | preview |
| `gemini-3-flash-preview` | $0.50 | $3.00 | preview |

For comparison: 2.5 Flash is $0.30/$2.50, 2.5 Flash-Lite is $0.10/$0.40. **3.5 Flash is 5x input / 3.6x output more expensive than 2.5 Flash.** Real-world per-call cost with classification prompt (3.5k input, ~500 output) is ~$0.010 for 3.5 Flash vs ~$0.0014 for 2.5 Flash — a 7x multiplier.

### 7. TalentMap empirical findings (2026-05-20, 150-row rich-context sample)

| Model | vs Claude @6 | vs 2.5 Flash @6 | 6-digit rate | Cost / 72k rows |
|---|---:|---:|---:|---:|
| 2.5 Flash-Lite | 17.5% | — | 100% | $30 |
| 2.5 Flash | 19.2% | (self) | 100% | $104 |
| 3.1 Flash-Lite | 15.8% | 46.0% | 86.7% | $118 |
| 3.5 Flash | **24.1%** | 64.2% | 98.7% | $709 |

3.5 Flash: +5pp absolute Claude-agreement vs 2.5 Flash at 6.8x cost. Worth it for audit / re-classification; **not** worth it for production polling.

3.1 Flash-Lite: **regression** — lower Claude-agreement than 2.5 Flash-Lite AND 4x more expensive. Avoid.

### 8. Known anti-patterns

- **Don't** run 3.x at temperature 0 — output degrades materially per Google's docs.
- **Don't** set `max_output_tokens=800` for 3.x classification — JSON gets truncated mid-string.
- **Don't** assume 3.x is a drop-in replacement for 2.x prompts — 36% of rows change at 6-digit level when swapping 2.5 → 3.5 Flash. Re-validate every downstream consumer of the classifier output.

---

## Google — Gemini 2.5 Pro / Flash / Flash-Lite

**Provider docs URL:** https://ai.google.dev/gemini-api/docs/prompting-strategies + https://ai.google.dev/gemini-api/docs/structured-output
**Date captured:** 2026-05-18
**Applies to model IDs:** `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`

**Status, 10 November 2026 (section not refreshed):** `gemini-2.5-pro` and `gemini-2.5-flash` are deprecated; on 1 December 2026 their requests route to `gemini-3.8-flash` and `gemini-3.5-flash-lite`. `gemini-2.5-flash-lite` is served only to existing users. Google's current structured-output page names the schema field `response_json_schema`; the `response_schema` used below is the older name. For new work use [§ Google Gemini 4 / 3.8 / 3.6 / 3.5 Flash-Lite](#google--gemini-4-argon--38-flash--36-flash--35-flash-lite).

### 1. Prompt structure recommendations

Gemini's official guide is **context-first, question-last**. The model attends most heavily to tokens near the end of the context window for generation, so:

1. **`system_instruction`** parameter — role + invariant rules. Separate from `contents`; don't bury role in the first user turn.
2. **Context block first** — reference docs, schema, examples, prior decisions. Use XML or markdown headers.
3. **Few-shot examples** if applicable.
4. **Transition phrase** — `"Based on the information above, answer the following:"`. The Google docs explicitly recommend this exact phrasing; it materially improves long-context recall.
5. **Question / instruction last.**
6. **Output format spec** is delivered via the `response_schema` API parameter, NOT inside the prompt text (see §2).

For long-context tasks (>50k tokens), put the **question both before AND after** the context. Gemini's "needle-in-haystack" performance is best with question framing twice.

### 2. JSON output mechanism

**Use the `response_schema` API parameter — do NOT format JSON via prose instructions.**

```python
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Literal

class ClassifiedClause(BaseModel):
    clause_type: Literal["indemnification", "termination", "confidentiality", "other"]
    risk_score: int = Field(ge=1, le=5)
    rationale: str

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="...",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ClassifiedClause,
        temperature=0,
    )
)
parsed: ClassifiedClause = response.parsed   # already a Pydantic instance
```

The `response_schema` can be a Pydantic class, a `genai.types.Schema` proto, or a raw JSON Schema dict. Pydantic is the cleanest in Python.

**Enum constraints** are honoured: `Literal["a","b","c"]` becomes a JSON enum that Gemini cannot violate.

For Gemini 2.5 Pro/Flash, you can also use **function calling** (`tools=[...]`) which works identically to Claude's tool use — pick one or the other, not both in the same call.

### 3. Delimiter preferences

Either XML tags OR markdown headers — both work for Gemini. The official guide leans **XML for long contexts** (>10k tokens), **markdown for short**.

Naming convention from the docs: `<role>`, `<context>`, `<example>`, `<question>`, `<output_format>`.

### 4. Classification task framing

Frame as **multiple-choice** wherever possible. Gemini calibrates strongly to enumerated candidate sets — Google's docs recommend this explicitly over open-ended classification.

For graded scoring, provide anchor descriptions per level (same as Claude — Gemini benefits identically).

**Important Gemini quirk:** if you specify the enum in BOTH the prompt text AND the `response_schema`, occasionally Gemini will return a value from the prompt that isn't in the schema (causing a validation error). Specify enums **only in `response_schema`** and leave the prompt high-level.

### 5. Temperature default & quirks

- **Default for structured extraction:** `temperature=0`.
- **Default for creative writing:** `temperature=1.0`.
- **Thinking mode** (Flash and Pro): set `thinking_config=types.ThinkingConfig(thinking_budget=N)` where N is token budget. `thinking_budget=0` disables thinking on Flash; `-1` lets the model decide. Flash-Lite does NOT support thinking.
- **Gemini 3.0 forward-compat note:** Google's Gemini 3 docs state the model "MUST run at temperature 1.0" — any other value degrades output. If/when 3.0 lands in `MODEL-RESEARCH.md`, this section gets split.

### 6. Worked example

```python
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Literal

class ClassifiedClause(BaseModel):
    clause_type: Literal[
        "indemnification", "limitation_of_liability", "termination",
        "confidentiality", "ip_ownership", "payment_terms", "warranty",
        "data_protection", "non_compete", "force_majeure", "governing_law",
        "auto_renewal", "other"
    ]
    risk_score: int = Field(ge=1, le=5, description="1=boilerplate, 5=escalate")
    rationale: str

client = genai.Client()

prompt = """<role>You are a contract clause classifier.</role>

<context>
Risk scale anchors:
1 = boilerplate, no negotiation needed
2 = mildly unusual but acceptable
3 = noteworthy, flag in summary
4 = material exposure, recommend redline
5 = catastrophic, escalate to partner
</context>

<examples>
<example>
<input>Either party may terminate with 30 days notice.</input>
<output>termination, score 2 — mutual 30-day termination is standard.</output>
</example>
<example>
<input>Supplier indemnifies Customer for ALL losses including consequential and indirect damages without cap.</input>
<output>indemnification, score 5 — uncapped indemnity including consequentials.</output>
</example>
</examples>

<input>Customer indemnifies Supplier against any third-party IP claims arising from Customer's modifications to the Software.</input>

Based on the information above, classify the clause inside <input> and return the structured result.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=(
            "You categorise contract clauses by type and assess risk on a 1–5 scale. "
            "Always return a single best-fit clause_type from the enum and a rationale "
            "shorter than 30 words."
        ),
        response_mime_type="application/json",
        response_schema=ClassifiedClause,
        temperature=0,
    )
)

result: ClassifiedClause = response.parsed
```

### 7. Known anti-patterns

- **Don't** put the question FIRST then dump 50k tokens of context — positional weighting hurts recall. Context first, question last.
- **Don't** ask for JSON in prose when `response_schema` exists — Gemini sometimes wraps JSON in ```json fences when prompted in prose.
- **Don't** specify enums in BOTH the prompt text and the schema — schema-only is more reliable.
- **Don't** use Flash-Lite for thinking-mode tasks — it doesn't support it. Use Flash or Pro.
- **Don't** put role/persona in the first user message — use `system_instruction`. Persona inside user content is occasionally ignored or merged with the question.
- **Don't** use markdown headers for prompts >10k tokens — switch to XML.

---

## Google — Gemma 4 12B / 26B (local via Ollama)

**Provider docs URL:** https://ai.google.dev/gemma/docs/core/prompt-structure + https://ollama.com/blog/structured-outputs
**Date captured:** 2026-06-07
**Applies to model IDs:** `gemma4:12b`, `gemma4:26b` (Ollama, `ollama_local` adapter — free, on-device on the RTX 4090)

> **Gemma ≠ Gemini.** Gemma is the open-weights family we run locally; its prompt conventions differ from the Gemini API sections above. Two big differences: (1) **no system role** — Gemma has only `user` and `model` turns; (2) JSON is enforced by **Ollama's `format` parameter** (a JSON Schema object), not Gemini's `response_schema`.

### 1. Prompt structure recommendations

Gemma's chat template uses exactly two roles — `user` and `model` — wrapped in `<start_of_turn>` / `<end_of_turn>` control tokens. **Ollama applies this template for you** from the model's Modelfile, so you send normal role messages and never hand-write the turn tokens.

1. **No system role.** Gemma folds system-level instructions into the *first user turn*. With Ollama you may still pass a `system` field (or a `{"role":"system"}` message) — Ollama's Gemma template prepends it to the first user turn automatically. Put role + invariant rules there.
2. **Order:** persona/rules → context block → few-shot examples → the actual instruction/question **last**. Like Gemini, Gemma weights late tokens most for generation.
3. **Multimodal** (text + image + audio, 256K context): pass images as base64 in a message's `images` array (`/api/chat`). The vision encoder is bundled in the `gemma4:*` tags.

### 2. JSON output mechanism

**Use Ollama's `format` parameter with a full JSON Schema object** — constrained decoding, so the model literally cannot emit non-conforming tokens. Do NOT ask for JSON in prose.

```python
import ollama
from pydantic import BaseModel, Field
from typing import Literal

class ClassifiedClause(BaseModel):
    clause_type: Literal["indemnification", "termination", "confidentiality", "other"]
    risk_score: int = Field(ge=1, le=5)
    rationale: str

resp = ollama.chat(
    model="gemma4:12b",
    messages=[{"role": "user", "content": "..."}],
    format=ClassifiedClause.model_json_schema(),   # <-- the JSON enforcement mechanism
    options={"temperature": 0},
)
parsed = ClassifiedClause.model_validate_json(resp["message"]["content"])
```

Raw HTTP equivalent: POST `/api/chat` (or `/api/generate`) with `"format": { ...json schema... }` and `"stream": false`. The bare string `"format": "json"` also works but only guarantees *valid* JSON, not *your shape* — always pass the schema object when you have one.

### 3. Delimiter preferences

Markdown headers or XML tags both work. Gemma was trained heavily on markdown, so **markdown (`## Context`, `## Task`) is the safe default**; reserve XML tags for fencing verbatim input you don't want interpreted (e.g. `<document>…</document>`).

### 4. Classification task framing

Frame as **multiple-choice** with an explicit enum, same as Gemini. Put the allowed values in the `format` schema (`Literal[...]` → JSON enum) and keep the prompt high-level — the schema enum is hard-enforced, so the model cannot return an out-of-set label. For graded scores, give per-level anchor descriptions in the prompt text.

### 5. Temperature default & quirks

- **Gemma's partner-recommended sampling is `temperature=1.0, top_p=0.95, top_k=64`** — the default for general / creative / coding use (Gemma 4 notably performs well at high temperature *even for coding*).
- **For deterministic extraction / classification, override to `temperature=0`** (greedy). Use this whenever you pass a `format` schema.
- Set via Ollama's `options` object: `options={"temperature": 0, "top_p": 0.95, "top_k": 64}`.
- **No dedicated "thinking mode"** (unlike Gemini Flash or DeepSeek R1) — Gemma 4 reasons inline. There is no separate thinking-budget knob.

### 6. Worked example

```python
import ollama
from pydantic import BaseModel, Field
from typing import Literal

class ClassifiedClause(BaseModel):
    clause_type: Literal[
        "indemnification", "limitation_of_liability", "termination",
        "confidentiality", "ip_ownership", "payment_terms", "warranty",
        "data_protection", "non_compete", "force_majeure", "governing_law",
        "auto_renewal", "other"
    ]
    risk_score: int = Field(ge=1, le=5, description="1=boilerplate, 5=escalate")
    rationale: str

# Gemma has NO system role — fold role + rules into the first user turn.
# (Ollama also accepts a `system=` arg and prepends it to the first user turn for you.)
user_prompt = """You are a contract clause classifier. You categorise clauses by type
and assess risk on a 1-5 scale, returning a single best-fit clause_type and a
rationale under 30 words.

## Risk scale anchors
1 = boilerplate, no negotiation needed
2 = mildly unusual but acceptable
3 = noteworthy, flag in summary
4 = material exposure, recommend redline
5 = catastrophic, escalate to partner

## Examples
- "Either party may terminate with 30 days notice." -> termination, score 2 (mutual, standard).
- "Supplier indemnifies Customer for ALL losses incl. consequential damages, no cap." -> indemnification, score 5 (uncapped).

## Clause to classify
<document>
Customer indemnifies Supplier against any third-party IP claims arising from
Customer's modifications to the Software.
</document>

Classify the clause inside <document> and return the structured result."""

resp = ollama.chat(
    model="gemma4:12b",
    messages=[{"role": "user", "content": user_prompt}],
    format=ClassifiedClause.model_json_schema(),
    options={"temperature": 0},
)
result = ClassifiedClause.model_validate_json(resp["message"]["content"])
```

### 7. Known anti-patterns

- **Don't** send a `{"role":"system"}` turn expecting a Gemini/Claude-style separate system channel — Gemma has none; it gets merged into the first user turn. Write the prompt knowing that.
- **Don't** hand-write `<start_of_turn>` / `<end_of_turn>` tokens when calling via Ollama — the Modelfile template adds them; doubling them corrupts the prompt.
- **Don't** rely on prose "respond in JSON" — pass the schema to `format`. Prose-only JSON from Gemma sometimes arrives wrapped in ```json fences.
- **Don't** run extraction at the default `temperature=1.0` — drop to `0` for structured / classification work; keep `1.0` only for creative / coding generation.
- **Don't** assume `gemma4:12b` and `gemma4:26b` need different prompts — same family, same template; the 26B is just stronger. Prompt identically; pick the size by task difficulty / VRAM headroom.

---

## DeepSeek — V4.1 Flash / V4 Pro

**Provider docs URL:** https://api-docs.deepseek.com/guides/thinking_mode + https://api-docs.deepseek.com/guides/json_mode + https://api-docs.deepseek.com/quick_start/pricing
**Date captured:** 2026-11-10
**Applies to model IDs:** `deepseek-flash` (served by DeepSeek-V4.1-Flash-1017), `deepseek-v4-pro` (DeepSeek-V4-Pro-0813)

**What changed since the 18 May 2026 capture:** DeepSeek's API docs now list only `deepseek-flash` and `deepseek-v4-pro`. The `deepseek-v4-flash` names are retired but still accepted (served by V4.1 Flash). `deepseek-chat` and `deepseek-reasoner` are no longer mentioned (third-party reports say they were retired on 24 July 2026). Thinking is now a switch on both models rather than a separate R1 model. The May 2026 rules about R1, `<think>` tags, all-caps section headers, numbered enum lists and "early tokens weigh more" are not in DeepSeek's current docs and have been dropped.

### 1. Prompt structure recommendations

DeepSeek does not publish a prompt-structure guide. Its JSON Output example shows the shape to follow: a system prompt that states the task and then gives a sample input and the exact JSON it expects ("EXAMPLE INPUT:" then "EXAMPLE JSON OUTPUT:"), with the real item in the user message.

### 2. JSON output mechanism

- Set `response_format={"type": "json_object"}`. This is the only documented JSON option; there is no `json_schema` mode, so validate in code.
- The prompt must include the word "json" and an example of the JSON structure you want.
- Set `max_tokens` high enough that the JSON is not cut off.
- If the output is not valid JSON, the API returns spaces instead, so `content` can look empty even with `finish_reason` `stop`. Check for blank content and retry.
- Parse `content`, not `reasoning_content`.

### 3. Delimiter preferences

Not documented. The official example uses plain labelled lines (`EXAMPLE INPUT:`, `EXAMPLE JSON OUTPUT:`).

### 4. Classification task framing

List the allowed labels in the system prompt next to the JSON example, then check the returned label against the allowed set in code, because JSON mode does not enforce a schema.

### 5. Temperature default & quirks

- **Thinking is on by default.** OpenAI format: `extra_body={"thinking": {"type": "enabled"}}` or `"disabled"`. Anthropic and Responses formats: `reasoning.effort`, where `none` turns thinking off.
- **Effort:** `reasoning_effort` `low`, `high` or `max`; default `high`. Other names are mapped (`minimal` to `low`; `medium` and `xhigh` to `high`; `ultra` to `max`).
- `temperature`, `presence_penalty` and `frequency_penalty` are accepted in thinking mode but have no effect. `top_p` has model-specific floors (for `deepseek-flash`, 0.95 to 1.0 in thinking mode, fixed at 1.0 without thinking).
- The chain of thought comes back in `reasoning_content`. Without tools, earlier turns' `reasoning_content` is ignored. **With tools, you must pass back the `reasoning_content` of all previous turns, or the API returns 400.**
- Context 1M tokens; maximum output 384K. Vision on `deepseek-flash` only.
- **Off-peak prices are half of peak.** Peak is 01:00 to 04:00 and 06:00 to 10:00 UTC on weekdays (11:00 am to 2:00 pm and 4:00 pm to 8:00 pm Brisbane). Schedule batch jobs outside those hours.
- OpenAI-compatible base URL `https://api.deepseek.com`; Anthropic-compatible `https://api.deepseek.com/anthropic`.

### 6. Worked example

```python
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

ALLOWED = {"indemnification", "limitation_of_liability", "termination", "confidentiality",
           "ip_ownership", "payment_terms", "warranty", "data_protection", "non_compete",
           "force_majeure", "governing_law", "auto_renewal", "other"}

system = """You classify one contract clause and reply in json.
clause_type must be one of: indemnification, limitation_of_liability, termination,
confidentiality, ip_ownership, payment_terms, warranty, data_protection, non_compete,
force_majeure, governing_law, auto_renewal, other.
risk_score is an integer from 1 (boilerplate) to 5 (escalate to a partner).

EXAMPLE INPUT: Either party may terminate with 30 days notice.
EXAMPLE JSON OUTPUT:
{"clause_type": "termination", "risk_score": 2, "rationale": "Mutual 30-day termination is standard."}"""

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": "Customer indemnifies Supplier against any third-party "
                                    "IP claims arising from Customer's modifications to the Software."},
    ],
    response_format={"type": "json_object"},
    max_tokens=1024,
    extra_body={"thinking": {"type": "disabled"}},   # simple classification; enable for harder tasks
)

content = response.choices[0].message.content
if not content or not content.strip():
    raise RuntimeError("Blank JSON reply; retry")
result = json.loads(content)
if result.get("clause_type") not in ALLOWED or result.get("risk_score") not in range(1, 6):
    raise ValueError(f"Out-of-schema reply: {result}")
```

### 7. Known anti-patterns

- **Don't** use `deepseek-chat`, `deepseek-reasoner` or `deepseek-v4-flash` in new code; use `deepseek-flash` or `deepseek-v4-pro`.
- **Don't** leave the word "json" and a JSON example out of the prompt when using JSON mode.
- **Don't** trust JSON mode to enforce a schema; validate.
- **Don't** treat a blank or all-spaces `content` as success.
- **Don't** drop `reasoning_content` from history in tool-calling conversations (400 error).
- **Don't** tune `temperature` in thinking mode; it has no effect.
- **Don't** run large batch jobs in Brisbane peak hours if cost matters.

---

## Moonshot — Kimi K3.1 Pro / K3

**Provider docs URL:** https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart + https://platform.kimi.ai/docs/pricing/chat
**Date captured:** 2026-11-10
**Applies to model IDs:** `kimi-k3.1-pro`, `kimi-k3.1-pro-highspeed`, `kimi-k3`. The K2 series (`kimi-k2.7-code`, `kimi-k2.6`) retires by the end of December 2026; `kimi-k2.5` is no longer on the price list.

**What changed since the 18 May 2026 capture:** Moonshot's developer site moved to platform.kimi.ai. The old agentic-prompting and prompt-engineering links now open quick-start pages with no prompting guide. The May 2026 rules (identity warning, Markdown beats XML above 50K tokens, `temperature=0.3`, `source_quote` anti-hallucination pattern) are no longer in Moonshot's docs and are dropped. Sampling is now fixed, so the old temperature advice cannot be applied.

### 1. Prompt structure recommendations

Moonshot publishes no structure guide for K3. Its examples use a `system` message that opens "You are Kimi, an AI assistant provided by Moonshot AI." followed by the task in a `user` message. Keeping that opening and adding the specialist role after it matches the official examples.

### 2. JSON output mechanism

- `response_format={"type": "json_schema", "json_schema": {...}, "strict": True}` style structured output (OpenAI-compatible).
- **Parse only `message.content`, never `reasoning_content`.**

### 3. Delimiter preferences

Not documented.

### 4. Classification task framing

Labels in a schema `enum`. Lower the reasoning effort for simple, high-volume labels.

### 5. Temperature default & quirks

- **Sampling is fixed:** `temperature=1.0`, `top_p=0.95`, `n=1`, `presence_penalty=0`, `frequency_penalty=0`. Leave them out of requests.
- **Thinking is always on** for K3.1 Pro and cannot be turned off. Set top-level `reasoning_effort` to `low`, `high` or `max`; the default is `max`. Moonshot suggests `low` if responses are too slow.
- `max_completion_tokens` defaults to 131,072 and can go to 1,048,576.
- Keep the **full assistant message** in history in multi-turn and tool flows, not just `content`.
- Tools: `tool_choice="required"` forces a call on the first turn. Dynamically added tools must be resent each request (the server does not store them). Moonshot says its web search is not recommended for production.
- **Caching is automatic** (5-minute TTL by default, 1 hour via `prompt_cache_options.ttl`); cache writes carry a one-time charge. Batch inference costs 60% of standard.
- Vision: `content` must be an array; public image URLs are not supported (use base64 or `ms://<file-id>`).
- Base URL `https://api.moonshot.ai/v1` with the OpenAI SDK.

### 6. Worked example

```python
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.ai/v1")

response = client.chat.completions.create(
    model="kimi-k3.1-pro",
    reasoning_effort="low",               # default is max; no sampling parameters
    messages=[
        {"role": "system", "content": (
            "You are Kimi, an AI assistant provided by Moonshot AI. "
            "For this task you classify contract clauses. Risk: 1 = boilerplate, "
            "2 = mildly unusual, 3 = noteworthy, 4 = material exposure, 5 = escalate."
        )},
        {"role": "user", "content": (
            "Classify this clause: Customer indemnifies Supplier against any third-party "
            "IP claims arising from Customer's modifications to the Software."
        )},
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "classified_clause",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "clause_type": {"type": "string", "enum": [
                        "indemnification", "limitation_of_liability", "termination",
                        "confidentiality", "ip_ownership", "payment_terms", "warranty",
                        "data_protection", "non_compete", "force_majeure",
                        "governing_law", "auto_renewal", "other"]},
                    "risk_score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                    "rationale": {"type": "string"},
                },
                "required": ["clause_type", "risk_score", "rationale"],
                "additionalProperties": False,
            },
        },
    },
)
result = json.loads(response.choices[0].message.content)   # never reasoning_content
```

### 7. Known anti-patterns

- **Don't** set `temperature`, `top_p`, `n` or the penalties; they are fixed.
- **Don't** strip the assistant message down to `content` in multi-turn or tool flows.
- **Don't** parse `reasoning_content` for structured output.
- **Don't** assume dynamically loaded tools persist on the server.
- **Don't** rely on Kimi web search in production.
- **Don't** send public image URLs or a serialised string as vision `content`.
- **Don't** start new work on K2 models; they retire by the end of December 2026.

---

## xAI — Grok 4.7 / 4.6 / 4.5 / 4.3 / Build 0.1

**Provider docs URL:** https://docs.x.ai/developers/model-capabilities/text/best-practices + https://docs.x.ai/docs/guides/structured-outputs + https://docs.x.ai/developers/model-capabilities/text/reasoning
**Date captured:** 2026-11-10
**Applies to model IDs:** `grok-4.7`, `grok-4.6`, `grok-4.5`, `grok-4.3`, `grok-build-0.1`

**URL change:** the old `https://docs.x.ai/docs/guides/prompt-engineering` page returns 404 (checked 10 November 2026). xAI's guidance now lives on the best-practices and reasoning pages above. Grok-4, Grok-4.1 Fast, Grok-3 and Grok-Code-Fast-1 were retired on 15 May 2026; their slugs redirect to Grok 4.3 or Build 0.1 and are billed at those prices. xAI publishes no prompt guide for Build 0.1.

### 1. Prompt structure recommendations

- "Grok reasoning models reason before they answer, so state the task, constraints, and output format directly."
- **Static content first:** "System prompts, few-shot examples, and reference documents at the start of the input form a stable prefix" that the cache can reuse. Put the variable item last.
- "Only append to the conversation." Editing, removing or reordering earlier items breaks the cached prefix.
- For model-as-judge prompts: "give it a specific rubric with examples of each score".

### 2. JSON output mechanism

- **Chat Completions:** `response_format={"type": "json_schema", "json_schema": {"name": "...", "schema": {...}, "strict": True}}`.
- **Responses API:** `text={"format": {"type": "json_schema", "name": "...", "schema": {...}, "strict": True}}`.
- **xAI SDK:** `client.chat.create(model="grok-4.7", response_format=PydanticModel)`, then `chat.parse(Model)` for a parsed object.
- `json_object` (any well-formed JSON) also exists; prefer `json_schema`.
- Schema rules: `additionalProperties` defaults to `false`; fields not in `required` are optional; nullable fields need a type array or `anyOf` with `null`. Enforced string formats: `date`, `time`, `date-time`, `email`, `uuid`, `ipv4`, `ipv6`, `uri`. Guaranteed limits: `minLength`/`maxLength` up to 2,048, `minItems`/`maxItems` up to 256. `not`, `if`/`then`/`else` and multi-part `allOf` are best-effort only.

### 3. Delimiter preferences

Not covered by xAI's current pages. Keep one consistent style.

### 4. Classification task framing

Put the labels in a schema `enum`. For graded scores, give a rubric with an example of each score (xAI's advice for judge prompts).

### 5. Temperature default & quirks

- **Sampling:** "Set `temperature` to 0.7 and `top_p` to 0.95, and don't deviate far from these values." "Grok models don't respond well to other sampling settings, and quality usually drops when you change them." This replaces the May 2026 advice to use `temperature=0` for extraction.
- **Reasoning effort:** "Set the effort explicitly on every request so a default never decides your result," and log it with each result. `grok-4.7` and `grok-4.6`: `low`, `medium`, `high`, `xhigh`, default `high`, cannot be turned off. `grok-4.5`: `low` to `high` (`xhigh` treated as `high`). `grok-4.3`: defaults to `low` and also accepts `none`.
- `presencePenalty`, `frequencyPenalty` and `stop` cannot be used with reasoning models (error).
- **Caching:** give each conversation its own `prompt_cache_key` and reuse it every turn.
- **Multi-turn and tools:** send encrypted reasoning back unchanged. Use the Responses API for multi-turn or tool-calling work; Chat Completions has no field for encrypted reasoning.
- **Web search:** the `web_search` tool runs through the Responses API (`https://api.x.ai/v1/responses`), with `allowed_domains` / `excluded_domains` filters (up to 5 each).

### 6. Worked example

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1")

SYSTEM = (
    "You are a contract clause classifier. State one clause_type and a risk score.\n"
    "Risk rubric with examples:\n"
    "1 = boilerplate (e.g. standard governing-law clause)\n"
    "2 = mildly unusual (e.g. mutual 30-day termination)\n"
    "3 = noteworthy (e.g. one-sided auto-renewal)\n"
    "4 = material exposure (e.g. liability cap below fees paid)\n"
    "5 = escalate (e.g. uncapped indemnity including consequential loss)"
)

response = client.chat.completions.create(
    model="grok-4.3",
    reasoning_effort="low",               # set explicitly every time
    temperature=0.7,
    top_p=0.95,
    messages=[
        {"role": "system", "content": SYSTEM},          # static prefix first
        {"role": "user", "content": (
            "Clause: Customer indemnifies Supplier against any third-party IP claims "
            "arising from Customer's modifications to the Software."
        )},
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "classified_clause",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "clause_type": {"type": "string", "enum": [
                        "indemnification", "limitation_of_liability", "termination",
                        "confidentiality", "ip_ownership", "payment_terms", "warranty",
                        "data_protection", "non_compete", "force_majeure",
                        "governing_law", "auto_renewal", "other"]},
                    "risk_score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                    "rationale": {"type": "string"},
                },
                "required": ["clause_type", "risk_score", "rationale"],
            },
        },
    },
)
```

### 7. Known anti-patterns

- **Don't** keep retired slugs (`grok-4-0709`, `grok-4-1-fast-*`, `grok-3`, `grok-code-fast-1`) pinned; they still answer but run a different model at Grok 4.3 or Build 0.1 prices.
- **Don't** move `temperature` or `top_p` far from 0.7 and 0.95.
- **Don't** leave reasoning effort to the default; `grok-4.7` defaults to `high`.
- **Don't** send `presencePenalty`, `frequencyPenalty` or `stop` to reasoning models.
- **Don't** edit, reorder or filter output items before sending them back, or rebuild the conversation in a different format between turns.
- **Don't** extract `output_text` and append it as a plain assistant message; that drops the reasoning and function-call items.
- **Don't** use Chat Completions for multi-turn or tool-calling work.

---

## OpenAI — GPT-6 Astra / 6.1 Sol / 6.1 Terra / 6 Luna (API and Codex)

**Provider docs URL:** [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model) · [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) · [Codex models](https://learn.chatgpt.com/docs/models) · [Codex best practices](https://developers.openai.com/codex/learn/best-practices) · [AGENTS.md for Codex](https://developers.openai.com/codex/guides/agents-md) · [Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)
**Date captured:** 2026-11-10
**Applies to model IDs:** `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna` (API and Codex). `gpt-5.3-codex` is deprecated: already in Codex when signed in with ChatGPT, and on the API from 1 April 2027.

**Scope note:** Two distinct surfaces. **(A) Codex** is the agentic coding and review tool (CLI, IDE, GitHub), driven by natural-language tasks and the repo's `AGENTS.md`, not by JSON API calls. This is what Greg uses for code review, signed in with ChatGPT Plus. **(B) the OpenAI API** for programmatic calls. Codex now offers `gpt-6-astra` (most demanding work), `gpt-6.1-sol` (lower cost for repeated, long-running work), `gpt-6.1-terra` (writing and visual tasks; needs Codex CLI 0.159.0 or later) and `gpt-6-luna` (focused, high-volume tasks). Codex's config example sets `model = "gpt-6.1-sol"`. Update any script, config file or `codex exec --model` call that still names `gpt-5.3-codex` or `gpt-5.2`.

The Codex review-gate guidance in sections 1, 3, 4 and the first worked example is from the 13 June 2026 capture. Those Codex pages were still live on 10 November 2026 but were not re-read this pass.

### 1. Prompt structure recommendations

**Codex (13 June 2026 capture):** four elements, in order: **Goal, Context, Constraints, Done-when.**
- **Goal:** one line, what to do.
- **Context:** the specific files, directories and docs, with the acceptance criteria and the spec to conform to.
- **Constraints:** standards, what not to touch, review-only or edit, safety.
- **Done-when:** completion and verification criteria.
- Codex is autonomous and persistent by default. Do not ask for an upfront plan or preamble (it causes premature stopping). For review, say **review-only, do not modify code**.
- Durable rules belong in `AGENTS.md` (nearest file wins), with a `CODE_REVIEW.md` referenced from it; keep each task prompt short.

**GPT-6 family (10 November 2026, "Using GPT-6"):**
- "Prompt the model to ask for approval only after preparing a concrete, reviewable result." Do the authorised work first so approval is the last step.
- The model should "persist until the user's intended goal is complete" unless an action is destructive or irreversible.
- "If explicit user instructions conflict with a skill's instructions, prioritize the user's instructions." Audit skills and `AGENTS.md` for conflicting or silent guidance; it can make Astra pause.
- State each "ask first" rule once; repeated approval rules cause approval requests for safe actions.
- For prose: "Default to using clear, concise paragraphs, each developing one main idea." Use lists only for parallel or sequential content. Astra tends toward detailed, formatted answers.

### 2. JSON output mechanism

- **Responses API (recommended):** `text: {format: {type: "json_schema", name: "...", schema: {...}, strict: true}}`. In the Python SDK, `client.responses.parse(..., text_format=Model)` returns `response.output_parsed`.
- **Chat Completions:** `response_format: {type: "json_schema", ...}`.
- The examples list every property in `required` and set `"additionalProperties": false`.
- Astra, Sol and Terra accept Chat Completions, but **tool calling with reasoning needs the Responses API**.
- Codex (the tool) is not a JSON surface. For machine-readable review output, set an output contract in the prompt (for example a final line `VERDICT: PASS|CONDITIONAL|FAIL`).

### 3. Delimiter & formatting preferences

The GPT-6 page gives no delimiter rule; its GPT-5.6 example uses an XML-tagged block. Codex conventions (13 June 2026 capture): light Markdown, bullets ordered by importance, backticks for paths and commands, fenced code blocks, file references as `path/to/file.ts:42`.

### 4. Classification and code-review framing

- **API classification:** put labels in the schema (`Literal` or `enum`) and use Structured Outputs.
- **Codex review (13 June 2026 capture):** when the task says "review", Codex puts findings first, ordered by severity, with `file:line` references, and says explicitly when it finds nothing. Tell it to run the tests and checks and paste the output.
- GPT-6: "Do not write tests for reversible, low-impact changes that mirror the implementation."

### 5. reasoning.effort and parameters

| Model | `reasoning.effort` values | Default |
|---|---|---|
| `gpt-6-astra` | no `none` (use `low`) | not stated |
| `gpt-6.1-sol` | `low`, `medium`, `high`, `xhigh`, `max` | `medium` |
| `gpt-6.1-terra` | `none`, `low`, `medium`, `high`, `xhigh`, `max` | `medium` |
| `gpt-6-luna` | supports `none` | not stated |

- "When reasoning effort is not `none`, remove `temperature`, `top_p`, and `top_logprobs`." Sampling settings only apply at `none`.
- If old code used `minimal`, start with `low` and compare.
- **Pro mode:** `reasoning.mode: "pro"` on the same model (no separate slug). No need to ask for "think harder" or several candidate answers in the prompt.
- **Verbosity:** `text.verbosity` (`low`, `medium`, `high`) sets the default detail (documented in the GPT-5.6 section of the same page); give task-specific length in the prompt.
- **Caching:** from GPT-5.5 or earlier, replace `prompt_cache_retention` with `prompt_cache_options.ttl` set to `"30m"`. To change effort mid-conversation, send a `configuration_update` input item and keep request-level `reasoning.effort` unchanged so the prefix stays cacheable.
- Message roles: put durable instructions in the `developer` message (13 June 2026 capture).

### 6. Worked examples

**Codex review gate:**

```text
Goal: Independently review Slice 2 (DB schema, RLS, audit) of the Shine CRM. Review only; do NOT modify code.

Context:
- Standards: ./CODE_REVIEW.md (durable review rules; auto-loaded via AGENTS.md)
- Slice scope + acceptance criteria: docs/implementation/00-master-plan.md (Slice 2)
- Specs it must conform to: docs/architecture/04-security-model.md, 02-schema-design.md
- Code: db/migrations/, src/lib/supabase/

Constraints:
- Read-only review. Do not edit files or run destructive git.
- Use high reasoning effort. Run the test suite + the RLS catalog test yourself; paste real output.
- Findings first, severity-ordered, each with file:line. No upfront plan/preamble.

Done when: you output numbered findings (sev-ordered) + a final line `VERDICT: PASS | CONDITIONAL (with must-fix list) | FAIL`, with pasted test output as evidence. PASS only if every crm table has RLS + grants in-migration, policies match the role matrix, and tests are green.
```

**API classification:**

```python
from typing import Literal
from openai import OpenAI
from pydantic import BaseModel

class ClauseClassification(BaseModel):
    clause_type: Literal["indemnification", "limitation_of_liability", "termination",
                         "confidentiality", "ip_ownership", "payment_terms", "warranty",
                         "data_protection", "non_compete", "force_majeure",
                         "governing_law", "auto_renewal", "other"]
    risk_score: Literal[1, 2, 3, 4, 5]
    rationale: str

client = OpenAI()

response = client.responses.parse(
    model="gpt-6-luna",
    reasoning={"effort": "low"},          # no temperature when effort is not "none"
    input=[
        {"role": "developer", "content": (
            "You classify one contract clause. Risk: 1 = boilerplate, "
            "2 = mildly unusual, 3 = noteworthy, 4 = material exposure, 5 = escalate. "
            "Give a one-sentence rationale."
        )},
        {"role": "user", "content": (
            "Customer indemnifies Supplier against any third-party IP claims arising "
            "from Customer's modifications to the Software."
        )},
    ],
    text_format=ClauseClassification,
)
result = response.output_parsed
```

### 7. Known anti-patterns

- **Don't** keep `gpt-5.3-codex` in Codex config or scripts; it is deprecated in Codex already.
- **Don't** send `temperature`, `top_p` or `top_logprobs` when reasoning effort is not `none`.
- **Don't** send `none` to Astra or 6.1 Sol; use `low`.
- **Don't** repeat "ask first" or "wait for approval" rules; state each once.
- **Don't** write broad "be concise" rules; say what a short answer must still include.
- **Don't** add unsolicited warnings, disclaimers or approval flows for hypothetical risks, or stock phrases such as "delve" and "leverage".
- **Don't** give vague tool routing ("use Programmatic Tool Calling efficiently"); name the stage, tools and output schema.
- Codex (13 June 2026 capture): don't overload the prompt with durable rules (move them to `AGENTS.md`), don't ask for an upfront plan, don't forget "review-only", and start a fresh task per review gate rather than one long thread.

---

## Mistral — Large 4 / Small 4 / Ministral 3 / Codestral

**Provider docs URL:** https://docs.mistral.ai/studio-api/conversations/chat-completion/prompting + https://docs.mistral.ai/inference/conversations/structured-output/custom + https://docs.mistral.ai/studio-api/conversations/reasoning
**Date captured:** 2026-11-10
**Applies to model IDs:** `mistral-large-4-0` (Large 4), `mistral-small-2603` (Small 4), Ministral 3 (`ministral-8b-latest` in Mistral's example), Codestral

Not yet used by any Paperclip agent. Filled from the stub on 10 November 2026 because the lineup changed (Large 4 and Ministral 3 are new; Large 3 and Medium 3.5 are deprecated; Magistral and Nemo are retired).

### 1. Prompt structure recommendations

- "The **`system` prompt** is provided at the beginning of the conversation" and is normally developer-managed. If you cannot control it, put the context and instructions in the `user` prompt.
- Open with a role and a task: "You are a <role>, your task is to <task>."
- "The prompt should be clear and complete." Write as if the reader has no prior context.
- Few-shot examples can go in the prompt or as artificial user and assistant turns in the history.

### 2. JSON output mechanism

- **Custom structured output (recommended by Mistral as more reliable):** `client.chat.parse(model=..., messages=..., response_format=PydanticModel)`.
- **JSON mode:** enforces JSON only. You must also tell the model in the prompt to output JSON and give the format.

### 3. Delimiter preferences

"**Markdown** and/or **XML-style tags** are ideal" (readable, parsable, familiar to the models).

### 4. Classification task framing

- Either ask for the label alone ("a single word or string"; fast, cheap, less flexible) or ask for a JSON object ("more reliable and flexible").
- **Rating scales:** "use a worded scale for better performance" rather than a numeric one.
- Avoid vague quantities ("too long", "many"); give objective measures. Use decision trees for conditional logic, because long system prompts drift into contradictions.

### 5. Temperature default & quirks

- **Reasoning effort:** Large 4 accepts `low`, `medium` and `high` (not `none`, `minimal`, `xhigh` or `max`); Mistral recommends starting with `high`. Small 4 accepts `high` or `none`. No default is documented.
- With reasoning on, `message.content` is a list of chunks: a `ThinkChunk` (`type: "thinking"`) and a `TextChunk` with the answer. With `none` it is a plain string. Append the full assistant message, including the `ThinkChunk`, in multi-turn conversations.
- Temperature: the prompting page gives no rule; Mistral's structured-output example uses `temperature=0`.
- "Models are faster at ingesting tokens than generating them," so ask only for the output you need.
- Re-test prompts when models or versions change.

### 6. Worked example

```python
import os
from typing import Literal
from mistralai.client import Mistral
from pydantic import BaseModel

class ClauseClassification(BaseModel):
    clause_type: Literal["indemnification", "limitation_of_liability", "termination",
                         "confidentiality", "ip_ownership", "payment_terms", "warranty",
                         "data_protection", "non_compete", "force_majeure",
                         "governing_law", "auto_renewal", "other"]
    risk: Literal["boilerplate", "mildly_unusual", "noteworthy",
                  "material_exposure", "escalate"]          # worded scale, per Mistral
    rationale: str

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

response = client.chat.parse(
    model="mistral-small-2603",
    messages=[
        {"role": "system", "content": (
            "You are a contract clause classifier, your task is to label one clause.\n"
            "## Risk levels\n"
            "- boilerplate: standard wording, no action\n"
            "- mildly_unusual: acceptable but not standard\n"
            "- noteworthy: flag in the summary\n"
            "- material_exposure: recommend a redline\n"
            "- escalate: send to a partner"
        )},
        {"role": "user", "content": (
            "Customer indemnifies Supplier against any third-party IP claims arising "
            "from Customer's modifications to the Software."
        )},
    ],
    response_format=ClauseClassification,
    temperature=0,
)
```

### 7. Known anti-patterns

- **Don't** use blurry quantities or let a long system prompt contradict itself.
- **Don't** ask the model to count words; pass counts in as input.
- **Don't** request more output than you need.
- **Don't** use numeric rating scales where a worded one fits.
- **Don't** strip the `ThinkChunk` from history.
- **Don't** send `none` or `xhigh` to Large 4.
- **Don't** start new work on Mistral Large 3 or Medium 3.5; both retire 30 April 2027.

---

## Alibaba — Qwen3.8-Max / Qwen3.7-Plus / Qwen3.8-Flash

**Provider docs URL:** https://www.alibabacloud.com/help/en/model-studio/prompt-engineering-guide + https://www.alibabacloud.com/help/en/model-studio/qwen-structured-output + https://www.alibabacloud.com/help/en/model-studio/deep-thinking
**Date captured:** 2026-11-10
**Applies to model IDs:** `qwen3.8-max`, `qwen3.7-plus`, `qwen3.8-flash` (cloud, International region). The local `qwen3.8:27b` on Ollama is a different deployment; this section covers the cloud API.

Not yet used by any Paperclip agent in the cloud. Filled from the stub on 10 November 2026 because the lineup moved to Qwen3.7 and 3.8.

### 1. Prompt structure recommendations

Model Studio's text prompt guide gives a framework of six elements, in this order: **Context, Objective, Style, Tone, Audience, Response.** Add or remove elements to fit the task. For multi-step work, give explicit steps, or split the task across several calls (prompt chaining, which the guide says "performs better and has higher accuracy" but is harder to build).

### 2. JSON output mechanism

- **JSON Object mode:** `response_format={"type": "json_object"}`. The system or user message **must contain the word "JSON"** or the API returns an error. Supported on most Qwen models, including the 3.8-Max, 3.7-Plus and 3.8-Flash series.
- **JSON Schema mode:** `response_format={"type": "json_schema", "json_schema": {..., "strict": True}}` on the Qwen3.7-Plus, 3.7-Flash, 3.7-Max, 3.8-Max and 3.8-Flash series. **But the page says Singapore region models do not yet support JSON Schema mode**, so on the International endpoint use JSON Object mode and validate.
- The Responses API uses `text.format` with the same values.
- The guide calls a format template plus sample data "the most effective optimization approach" for structured output.

### 3. Delimiter preferences

Separators that are "rare in natural language text", such as `###`, `===` or `>>>`, around each block of content.

### 4. Classification task framing

Give an explicit output format with a template and a filled-in sample. Avoid ambiguous terms (the guide's example replaces "language" with "language type").

### 5. Temperature default & quirks

- All three models are hybrid thinking models with **thinking on by default**. Turn it off with `enable_thinking: False` (in the OpenAI Python SDK, inside `extra_body`). `thinking_budget` caps reasoning tokens. Reasoning arrives in `reasoning_content`.
- Thinking tokens are billed as output. On Qwen3.7-Plus they can be over 60% of output tokens, so turning thinking off for simple tasks cuts cost and time.
- `preserve_thinking` controls whether earlier `reasoning_content` is read in later turns (listed for 3.8-Max and 3.7, not 3.8-Flash).
- Temperature and `top_p` guidance was not on the pages read; leave them at their defaults.
- International base URL: `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`, key in `DASHSCOPE_API_KEY`.

### 6. Worked example

```python
import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",  # replace {WorkspaceId}
)

system = """### Context
You label contract clauses for a legal review team.
### Objective
Choose one clause_type and one risk_score for the clause you are given.
clause_type is one of: indemnification, limitation_of_liability, termination,
confidentiality, ip_ownership, payment_terms, warranty, data_protection, non_compete,
force_majeure, governing_law, auto_renewal, other.
risk_score is 1 (boilerplate) to 5 (escalate to a partner).
### Response
Return JSON only, in this template:
{"clause_type": "<value>", "risk_score": <1-5>, "rationale": "<one sentence>"}
Sample:
{"clause_type": "termination", "risk_score": 2, "rationale": "Mutual 30-day termination is standard."}"""

response = client.chat.completions.create(
    model="qwen3.8-flash",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": "### Clause\nCustomer indemnifies Supplier against any "
                                    "third-party IP claims arising from Customer's "
                                    "modifications to the Software.\n###"},
    ],
    response_format={"type": "json_object"},       # "JSON" appears in the system prompt
    extra_body={"enable_thinking": False},          # simple task; saves output tokens
)
result = json.loads(response.choices[0].message.content)
```

### 7. Known anti-patterns

- **Don't** send JSON Object mode without the word "JSON" in the messages; the API rejects it.
- **Don't** assume JSON Schema mode works on the Singapore (International) endpoint yet.
- **Don't** leave thinking on for simple, high-volume calls; it is billed as output.
- **Don't** send one-line, vague requests or long unlabelled blocks of text.
- **Don't** leave the output format open when another system will read the result.

---

## Zhipu AI — GLM-5.3 / GLM-5.3-Flash / GLM-4.7

**Provider docs URL:** https://docs.z.ai/guides/llm/glm-5.3 + https://docs.z.ai/guides/capabilities/struct-output
**Date captured:** 2026-11-10
**Applies to model IDs:** `glm-5.3`, GLM-5.3-Flash, `glm-5`, `glm-4.7`, `glm-4.6`; free `GLM-4.7-Flash` and `GLM-4.5-Flash`

Not yet used by any Paperclip agent. Filled from the stub on 10 November 2026. **Correction to the stub:** Z.ai's international API is OpenAI-compatible (`https://api.z.ai/api/paas/v4/`) and also has an Anthropic-compatible endpoint (`https://api.z.ai/api/anthropic`).

### 1. Prompt structure recommendations

Z.ai's model pages publish no prompt-structure guide. Their examples use a `system` message that sets the role, then the request in a `user` message. For JSON, Z.ai says to describe the expected JSON structure and field rules in the system message and put the user's request in the user message.

### 2. JSON output mechanism

- `response_format={"type": "json_object"}`. Documented for `glm-5`, `glm-4.7` and `glm-4.6` "etc."; a `json_schema` type is not documented, so validate in code.
- Z.ai's own SDK is `zai-sdk` (`from zai import ZaiClient`); the OpenAI SDK also works with the base URL above.

### 3. Delimiter preferences

Not documented.

### 4. Classification task framing

Put the allowed values and field rules in the system message next to the JSON shape, then check the reply against the allowed set in code.

### 5. Temperature default & quirks

- **GLM-5.3 always reasons.** `thinking.type` accepts only `enabled` (the default); `disabled` is not supported. When moving older code to `glm-5.3`, change `"disabled"` to `"enabled"` and set `reasoning_effort` to `low`, or the request fails.
- `reasoning_effort`: `low`, `high` or `max`; default `max`. "For complex tasks such as coding, we recommend using `max`." Use `low` for simple classification.
- GLM-5.3: 1M context, 128K maximum output, text input only.
- Temperature: Z.ai's examples set `temperature=1.0` but do not state a default.
- Through Mistral's API, GLM 5.3 is `zai-glm-5-3` (effort `low`, `high`, `max`; no `none`) and always returns content as a chunk list.

### 6. Worked example

```python
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["ZAI_API_KEY"], base_url="https://api.z.ai/api/paas/v4/")

ALLOWED = {"indemnification", "limitation_of_liability", "termination", "confidentiality",
           "ip_ownership", "payment_terms", "warranty", "data_protection", "non_compete",
           "force_majeure", "governing_law", "auto_renewal", "other"}

system = """You are a contract clause classifier. Reply only with JSON in this shape:
{
  "clause_type": "one of: indemnification | limitation_of_liability | termination | confidentiality | ip_ownership | payment_terms | warranty | data_protection | non_compete | force_majeure | governing_law | auto_renewal | other",
  "risk_score": "integer 1 (boilerplate) to 5 (escalate)",
  "rationale": "one sentence"
}"""

response = client.chat.completions.create(
    model="glm-4.7",                      # JSON mode documented for this model
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": "Classify: Customer indemnifies Supplier against any "
                                    "third-party IP claims arising from Customer's "
                                    "modifications to the Software."},
    ],
    response_format={"type": "json_object"},
)
result = json.loads(response.choices[0].message.content)
if result.get("clause_type") not in ALLOWED:
    raise ValueError(f"Out-of-schema reply: {result}")
```

### 7. Known anti-patterns

- **Don't** send `thinking: {"type": "disabled"}` to `glm-5.3`; it fails.
- **Don't** leave `reasoning_effort` at its `max` default for simple, high-volume work.
- **Don't** assume schema enforcement; JSON mode guarantees JSON only.
- **Don't** rely on the old note that GLM is not OpenAI-compatible; that referred to the open.bigmodel.cn API.

---

## MiniMax — M3.1-Flash / M3

**Provider docs URL:** https://platform.minimax.io/docs/guides/text-generation + https://platform.minimax.io/docs/api-reference/text-anthropic-api
**Date captured:** 2026-11-10
**Applies to model IDs:** `MiniMax-M3.1-Flash`, `MiniMax-M3`

Filled from the stub on 10 November 2026. LLM-MATRIX.md still names `MiniMax-M2.7` as the Engineer fallback, but M2.7 is no longer on MiniMax's price list; this section covers the current models.

### 1. Prompt structure recommendations

MiniMax publishes no prompt-structure guide on the pages read. It recommends its **Anthropic-compatible endpoint** (`https://api.minimax.io/anthropic`), so prompts go in the usual Anthropic shape: role and rules in `system`, the task in the user message. An OpenAI-compatible endpoint is at `https://api.minimax.io/v1`.

### 2. JSON output mechanism

- **No structured-output parameter is documented.** The Anthropic-compatible reference lists only `output_config.effort`, not `output_config.format`.
- `tool_choice` supports only `auto`, so a tool call cannot be forced.
- So: describe the JSON shape in the system prompt, parse the final text block, and validate in code. (A third-party framework, Agno, also says MiniMax has no native `json_schema` mode; not confirmed by MiniMax.)

### 3. Delimiter preferences

Not documented.

### 4. Classification task framing

List the allowed labels and the JSON shape in the system prompt; validate the label in code.

### 5. Temperature default & quirks

- **`temperature` is ignored** (always 1) and **`top_p` is ignored** (always 0.95). `stop_sequences` are ignored too.
- **Thinking is always on** and "cannot be turned off". Sending `thinking: {"type": "disabled"}` or effort `none` returns a 400 error. Lower `effort` instead: `low`, `medium`, `high`, `xhigh` or `max` (default `max` on M3.1-Flash). Anthropic-compatible: `output_config.effort`; OpenAI-compatible: `reasoning_effort` (thinking in `reasoning_content`); OpenAI Responses: `reasoning.effort`.
- **Thinking counts toward `max_tokens`.** A small value can end with `stop_reason: "max_tokens"` and no text.
- Both models have a 1M context window and accept text, image and video.
- MiniMax-M3 has a Priority tier at 1.5 times the price (`service_tier: "priority"`).

### 6. Worked example

```python
import json
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["MINIMAX_API_KEY"],
                             base_url="https://api.minimax.io/anthropic")

ALLOWED = {"indemnification", "limitation_of_liability", "termination", "confidentiality",
           "ip_ownership", "payment_terms", "warranty", "data_protection", "non_compete",
           "force_majeure", "governing_law", "auto_renewal", "other"}

response = client.messages.create(
    model="MiniMax-M3.1-Flash",
    max_tokens=4096,                      # leave room for thinking
    output_config={"effort": "low"},      # thinking cannot be disabled; lower effort instead
    system=(
        "You are a contract clause classifier. Reply with one JSON object only: "
        '{"clause_type": <one of indemnification, limitation_of_liability, termination, '
        "confidentiality, ip_ownership, payment_terms, warranty, data_protection, "
        "non_compete, force_majeure, governing_law, auto_renewal, other>, "
        '"risk_score": <integer 1 (boilerplate) to 5 (escalate)>, '
        '"rationale": <one sentence>}'
    ),
    messages=[{"role": "user", "content": (
        "Customer indemnifies Supplier against any third-party IP claims arising "
        "from Customer's modifications to the Software."
    )}],
)

if response.stop_reason == "max_tokens":
    raise RuntimeError("Ran out of tokens while thinking; raise max_tokens")
text = [block.text for block in response.content if block.type == "text"][-1]
result = json.loads(text)
if result.get("clause_type") not in ALLOWED:
    raise ValueError(f"Out-of-schema reply: {result}")
```

### 7. Known anti-patterns

- **Don't** send `thinking: disabled` or effort `none` (400 error).
- **Don't** tune `temperature`, `top_p` or `stop_sequences`; they are ignored.
- **Don't** set a small `max_tokens`; thinking can use it all and leave no answer.
- **Don't** expect `tool_choice` to force a tool; only `auto` works.
- **Don't** keep `MiniMax-M2.7` as a fallback without checking it still answers; it is off the price list.

---

## Maintenance contract

This file is owned by the **Researcher agent** ([positions/research/researcher/SOUL.md](./positions/research/researcher/SOUL.md)). On every weekly model-research run, Researcher MUST:

1. **For each filled section:**
   - Re-validate the `Provider docs URL` is still live (HTTP 200 / not 404). If broken, mark the section header with `⚠️ URL stale — needs refresh` and search for the new URL.
   - Check `Date captured` is < 6 months old. If older, fetch the latest provider docs and update the section.

2. **For each stub section:**
   - Check if the corresponding provider has been activated in `LLM-MATRIX.md` (any agent now using it). If yes, fetch the provider's prompting docs and convert the stub to a full section with all 9 components.

3. **For any new model in `MODEL-RESEARCH.md` since last week:**
   - Add a section here. Same nine-component template.

4. **Log to the weekly summary** sent to Greg:
   - Sections added (new models)
   - Sections refreshed (date > 6 months or URL was stale)
   - Sections still stub (provider not yet in use)
   - Sections that failed validation (provider docs returned 404 and no replacement URL found)

5. **CLI helpers** (in `scripts/update_llm_matrix.py`):
   - `python update_llm_matrix.py --guidelines-stale` — list sections > 6 months old or with broken URLs.
   - `python update_llm_matrix.py --guidelines <model>` — print the section's key rules + worked example for a given model name. This is the trigger phrase `check model guidelines for <model>` wired up.

6. **Trigger phrase contract:** when Greg (or any agent in the team) says `check model guidelines for <X>`, the relevant agent SHOULD:
   - Open this file, find the section for `<X>`.
   - Print: section header, the 7 key rules, and the worked example.
   - If section is missing OR `Date captured` > 6 months: auto-fetch the provider's prompting docs (WebFetch) and refresh the section before printing.

7. **Section template** for new entries:

   ```markdown
   ## <Provider> — <Model versions>

   **Provider docs URL:** <official prompt-engineering page>
   **Date captured:** YYYY-MM-DD
   **Applies to model IDs:** `<id-1>`, `<id-2>`

   ### 1. Prompt structure recommendations
   ### 2. JSON output mechanism
   ### 3. Delimiter preferences
   ### 4. Classification task framing
   ### 5. Temperature default & quirks
   ### 6. Worked example
   ### 7. Known anti-patterns
   ```

---

_Last updated: 2026-11-10. Weekly pass: refreshed Anthropic (Claude 5 family), OpenAI (GPT-6 family and Codex), xAI (old prompt-engineering URL now 404), DeepSeek (V4.1 Flash, V4 Pro) and Kimi (K3.1 Pro, K3); added a section for Gemini 4 Argon, 3.8 Flash, 3.6 Flash and 3.5 Flash-Lite; filled the Mistral, Qwen, GLM and MiniMax stubs; added status notes to the Gemini 3.x and 2.5 sections. Gemma 4 unchanged (quarterly local review). Previous update 2026-06-13._
