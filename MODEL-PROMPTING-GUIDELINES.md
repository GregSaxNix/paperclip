# Life Admin — Per-Model Prompt Engineering Guidelines

**Purpose:** Capture each model's official prompt-engineering guidance so that code calling that model uses ITS optimal structure, not a generic prompt. Writing one "generic" prompt that we reuse across models leaves accuracy on the table for every model.

**Cross-reference:** Global rule at `C:\Users\Administrator\.claude\CLAUDE.md` Part 15 (Per-Model Prompt Engineering). Companion files: [MODEL-RESEARCH.md](./MODEL-RESEARCH.md), [LLM-MATRIX.md](./LLM-MATRIX.md).

**Update cadence:** Weekly, in the same pass as `MODEL-RESEARCH.md`. The Researcher agent re-validates URLs, flags sections >6 months old, and adds sections for any newly-released model versions. See [Maintenance contract](#maintenance-contract) at the bottom.

**Refresh threshold:** Any section with a `Date captured` older than 6 months is auto-flagged stale by `python scripts/update_llm_matrix.py --guidelines-stale`.

**Trigger phrase:** `check model guidelines for <model>` — opens this file, prints the section's key rules + worked example. If section is missing or stale, auto-fetch the provider's docs and refresh.

---

## Table of contents

| Provider | Model versions | Section | Status |
|----------|----------------|---------|--------|
| Anthropic | Claude Opus 4.6, Sonnet 4.6, Haiku 4.5 | [§ Anthropic Claude](#anthropic--claude-opus-46--sonnet-46--haiku-45) | Filled 2026-05-18 |
| Google | Gemini 2.5 Pro, Flash, Flash-Lite | [§ Google Gemini 2.5](#google--gemini-25-pro--flash--flash-lite) | Filled 2026-05-18 |
| DeepSeek | V3.2, V4, R1 | [§ DeepSeek](#deepseek--v32--v4--r1) | Filled 2026-05-18 |
| Moonshot | Kimi K2.5 | [§ Kimi K2.5](#moonshot--kimi-k25) | Filled 2026-05-18 |
| xAI | Grok-4, Grok-4.1, Grok-3, Grok-Code-Fast-1 | [§ xAI Grok](#xai--grok-4--grok-41--grok-3) | Filled 2026-05-18 |
| OpenAI | GPT-5.3 Codex, GPT-4o, o3/o4-mini | [§ OpenAI](#openai--gpt-53-codex--gpt-4o--o-series) | Stub — pending weekly agent |
| Mistral | Large 3, Small 4, Codestral, Magistral 1.2 | [§ Mistral](#mistral--large-3--small-4--codestral) | Stub — pending weekly agent |
| Alibaba | Qwen 2.5-Max, Qwen-Plus, Qwen-Turbo | [§ Qwen](#alibaba--qwen-25-max--qwen-plus--qwen-turbo) | Stub — pending weekly agent |
| Zhipu AI | GLM-5, GLM-4.7, GLM-4.7-Flash | [§ GLM](#zhipu-ai--glm-5--glm-47--glm-47-flash) | Stub — pending weekly agent |
| MiniMax | MiniMax-M2.7 | [§ MiniMax](#minimax--m27) | Stub — pending weekly agent |

---

## Anthropic — Claude Opus 4.6 / Sonnet 4.6 / Haiku 4.5

**Provider docs URL:** https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
**Date captured:** 2026-05-18
**Applies to model IDs:** `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`

### 1. Prompt structure recommendations

Anthropic explicitly prefers a layered prompt with strong delimiting. Recommended order:

1. **System message** — role, persona, high-level rules (`"You are an HR document classifier..."`). Goes in the SDK's `system` parameter, NOT in the first user message.
2. **User message** opens with **task description** in plain language.
3. **`<context>...</context>`** — any reference data the model needs (long docs, schema definitions, examples of prior decisions).
4. **`<instructions>...</instructions>`** — numbered list of what to do.
5. **`<examples>...</examples>`** — 2–5 worked examples (multishot). For Opus 4.6, even 2 examples lifts extraction accuracy materially.
6. **`<input>...</input>`** — the actual data being processed (the document to classify, the text to summarise).
7. **`<output_format>...</output_format>`** — exact schema, with field names and types.
8. **Closing call to action** — "Now produce the classification."

Putting the *question* AFTER the *data* matters less for Claude than for Gemini, but putting data inside XML tags matters more.

### 2. JSON output mechanism

**Two options, preferred order:**

1. **Tool use with `input_schema`** (best for strict JSON). Define a tool with a JSON Schema; pass `tool_choice: {type: "tool", name: "classify"}`. Claude is forced to call the tool and the tool args ARE your structured output. Zero parsing errors.

   ```python
   tools=[{
       "name": "classify_clause",
       "description": "Return the structured classification.",
       "input_schema": {
           "type": "object",
           "properties": {
               "clause_type": {"type": "string", "enum": ["indemnification", "termination", ...]},
               "risk_score": {"type": "integer", "minimum": 1, "maximum": 5}
           },
           "required": ["clause_type", "risk_score"]
       }
   }]
   tool_choice={"type": "tool", "name": "classify_clause"}
   ```

2. **Response prefill** (lighter weight). Add an `assistant` message ending with `{` and stop sequences `["}"]` — Claude continues from `{`, producing JSON. Use when you don't need schema enforcement.

**Avoid:** Asking Claude in prose to "respond in JSON only with no markdown" — works but ~95% reliable. Tool use is 100%.

### 3. Delimiter preferences

**XML tags are strongly preferred** over markdown headers or plain text. Anthropic's docs say: "Claude has been specifically trained to pay attention to XML tags." Tag names are flexible — `<doc>`, `<source>`, `<example>` all work; consistency within a prompt matters more than the specific tag name.

Markdown headers work for short prompts but degrade for prompts >2k tokens.

### 4. Classification task framing

Frame classification as **multiple-choice with enumerated candidates**, surfaced in two places:
- In `<instructions>`: "Choose exactly one value from the candidate set below."
- In `<output_format>` or the tool's `input_schema`: `enum: [...]`.

For risk-scoring (graded labels), provide an **anchor description per level** ("1 = boilerplate, low impact; 5 = catastrophic, mandatory escalation"). Claude calibrates much better with anchors than with a bare 1-5 scale.

For multi-label tasks, ask for an array AND explicitly state "include all that apply" — Claude defaults to picking one even on multi-label tasks otherwise.

### 5. Temperature default & quirks

- **Default for structured extraction:** `temperature=0`.
- **Default for creative writing:** `temperature=1.0`.
- **Extended thinking** (Opus 4.6, Sonnet 4.6 only — NOT Haiku): set `thinking={"type": "enabled", "budget_tokens": 10000}`. When thinking is enabled, **temperature MUST be 1.0** (the API rejects other values). Thinking shows real CoT in `thinking` content blocks — log them, don't reply with them.
- **Caching:** add `cache_control: {type: "ephemeral"}` to long static blocks (system message, examples). 5-min TTL by default; 90% cost reduction on cache hits. Always cache the system message and any examples block longer than ~1k tokens.

### 6. Worked example

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    temperature=0,
    system=(
        "You are a contract clause classifier. You categorise clauses by type "
        "and assess risk on a 1–5 scale where 1 is boilerplate and 5 requires "
        "escalation to a partner."
    ),
    tools=[{
        "name": "classify_clause",
        "description": "Return the structured classification of a single clause.",
        "input_schema": {
            "type": "object",
            "properties": {
                "clause_type": {
                    "type": "string",
                    "enum": ["indemnification", "limitation_of_liability", "termination",
                             "confidentiality", "ip_ownership", "payment_terms",
                             "warranty", "data_protection", "non_compete",
                             "force_majeure", "governing_law", "auto_renewal", "other"]
                },
                "risk_score": {"type": "integer", "minimum": 1, "maximum": 5},
                "rationale": {"type": "string"}
            },
            "required": ["clause_type", "risk_score", "rationale"]
        }
    }],
    tool_choice={"type": "tool", "name": "classify_clause"},
    messages=[{
        "role": "user",
        "content": (
            "<task>Classify the clause below.</task>\n"
            "<instructions>\n"
            "1. Read the clause inside <input>.\n"
            "2. Choose exactly one clause_type from the enum.\n"
            "3. Score risk 1 (boilerplate) – 5 (escalate).\n"
            "4. Give a one-sentence rationale.\n"
            "</instructions>\n"
            "<examples>\n"
            "<example><input>Either party may terminate with 30 days notice.</input>"
            "<output>{\"clause_type\": \"termination\", \"risk_score\": 2,"
            " \"rationale\": \"Mutual 30-day termination is standard.\"}</output></example>\n"
            "<example><input>Supplier indemnifies Customer for ALL losses including"
            " consequential and indirect damages without cap.</input>"
            "<output>{\"clause_type\": \"indemnification\", \"risk_score\": 5,"
            " \"rationale\": \"Uncapped indemnity including consequentials requires escalation.\"}</output></example>\n"
            "</examples>\n"
            "<input>Customer indemnifies Supplier against any third-party IP claims arising from Customer's modifications to the Software.</input>"
        )
    }]
)

# response.content[0].input is your structured output dict
```

### 7. Known anti-patterns

- **Don't** stuff context into plain prose without XML tags — accuracy drops sharply above ~2k tokens.
- **Don't** ask for JSON in prose when you can use tool use — schema enforcement is free.
- **Don't** set `temperature` to anything other than 1.0 when `thinking` is enabled — the API errors.
- **Don't** send long static blocks (system, examples) without `cache_control` — costs 10× more.
- **Don't** mix "you are a helpful assistant" with a specialist role in the system prompt — overrides the specialist framing. Be specific OR be general, not both.
- **Don't** use Haiku 4.5 for extended thinking — Haiku doesn't support it. Use Sonnet/Opus.

---

## Google — Gemini 2.5 Pro / Flash / Flash-Lite

**Provider docs URL:** https://ai.google.dev/gemini-api/docs/prompting-strategies + https://ai.google.dev/gemini-api/docs/structured-output
**Date captured:** 2026-05-18
**Applies to model IDs:** `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`

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

## DeepSeek — V3.2 / V4 / R1

**Provider docs URL:** https://api-docs.deepseek.com/guides/json_mode + https://api-docs.deepseek.com/guides/reasoning_model
**Date captured:** 2026-05-18
**Applies to model IDs:** `deepseek-chat` (V3.2/V4), `deepseek-reasoner` (R1)

### 1. Prompt structure recommendations

DeepSeek weights early tokens more heavily than Gemini does. Recommended order:

1. **Role** — `"You are a..."` (in system message).
2. **Task** — single, concrete task statement.
3. **Context** — reference data.
4. **Constraints** — explicit rules ("answer must be < 50 words", "do not invent fields").
5. **Output format** — exact schema, before examples.
6. **Examples** — 1–3 worked examples LAST.

This is the **opposite order** to Gemini's context-first / question-last pattern. Same prompt with reordered sections produces materially different results across these two providers.

### 2. JSON output mechanism

Set `response_format={"type": "json_object"}` on the API call. **Critical:** the prompt MUST include the literal word `json` somewhere in the system or user content, or DeepSeek will silently return prose. The docs are explicit about this requirement.

```python
from openai import OpenAI  # DeepSeek is OpenAI-compatible

client = OpenAI(api_key="...", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a contract clause classifier. Output JSON."},
        {"role": "user", "content": "..."}
    ],
    response_format={"type": "json_object"},
    temperature=0,
)
```

**Strict schema enforcement is NOT yet available** in DeepSeek's JSON mode — you must validate post-hoc (Pydantic, jsonschema). For tasks where schema violations would be expensive, fall back to function calling via `tools=[{...}]` which has tighter constraint behaviour.

### 3. Delimiter preferences

DeepSeek's docs lean **plain-text sections with all-caps headers** (`ROLE:`, `TASK:`, `CONTEXT:`, `CONSTRAINTS:`, `OUTPUT FORMAT:`, `EXAMPLES:`). Markdown headers also work. XML tags work but provide no measurable lift on DeepSeek the way they do on Claude.

### 4. Classification task framing

Single-task framing only. **DeepSeek degrades significantly on multi-question prompts** — the docs explicitly recommend splitting "classify this AND extract that AND score this" into three separate API calls.

For classification, provide enum as a numbered list:

```
OUTPUT FORMAT:
clause_type: one of
  1. indemnification
  2. termination
  3. confidentiality
  ...
risk_score: integer 1-5
```

Numbered lists work better than comma-separated enums on V3.2 — surprising but consistent in our testing.

### 5. Temperature default & quirks

- **`deepseek-chat` (V3.2 / V4):** default `temperature=1.0`. For code/extraction set `temperature=0.0`.
- **`deepseek-reasoner` (R1):** **DOES NOT accept `temperature`, `top_p`, `presence_penalty`, or `frequency_penalty`** — the API silently ignores them. R1 always runs at its trained sampling settings.
- **R1 zero-shot vs few-shot:** DeepSeek's docs are explicit — **R1 performs better zero-shot**. Few-shot examples DEGRADE R1 output by leaking reasoning patterns from the examples. Use few-shot on `deepseek-chat`, never on `deepseek-reasoner`.
- **R1 returns `<think>...</think>` blocks** in the response content. Strip them before downstream parsing, or use `reasoning_content` field if the SDK exposes it.

### 6. Worked example

```python
from openai import OpenAI

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

system = """ROLE: Contract clause classifier.

TASK: Classify a single clause by type and assess risk 1-5.

CONSTRAINTS:
- Output valid JSON only, no prose.
- Do not invent fields outside the schema.
- Rationale must be < 30 words.

OUTPUT FORMAT (json):
{
  "clause_type": one of
    1. indemnification
    2. limitation_of_liability
    3. termination
    4. confidentiality
    5. ip_ownership
    6. payment_terms
    7. warranty
    8. data_protection
    9. non_compete
    10. force_majeure
    11. governing_law
    12. auto_renewal
    13. other,
  "risk_score": integer 1-5 (1=boilerplate, 5=escalate),
  "rationale": short string
}

EXAMPLES:
Input: "Either party may terminate with 30 days notice."
Output: {"clause_type": "termination", "risk_score": 2, "rationale": "Mutual 30-day termination is standard."}

Input: "Supplier indemnifies Customer for ALL losses without cap."
Output: {"clause_type": "indemnification", "risk_score": 5, "rationale": "Uncapped indemnity requires escalation."}
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": "Classify this clause: Customer indemnifies Supplier against any third-party IP claims arising from Customer's modifications to the Software."}
    ],
    response_format={"type": "json_object"},
    temperature=0,
)
```

### 7. Known anti-patterns

- **Don't** omit the literal word `json` from the prompt when using `response_format` — DeepSeek returns prose silently.
- **Don't** combine "classify AND extract AND score" in one prompt — split into separate calls.
- **Don't** use few-shot examples on `deepseek-reasoner` — they degrade output. Few-shot only on `deepseek-chat`.
- **Don't** rely on schema validation in JSON mode — DeepSeek's JSON mode is shape-only, not schema-enforced. Validate post-hoc.
- **Don't** set `temperature` on R1 — silently ignored.
- **Don't** stuff context into the middle of the prompt — DeepSeek attends most heavily to the start.

---

## Moonshot — Kimi K2.5

**Provider docs URL:** https://platform.moonshot.ai/docs/guide/agentic-prompting + https://platform.moonshot.ai/docs/guide/prompt-engineering
**Date captured:** 2026-05-18
**Applies to model IDs:** `kimi-k2.5`, `moonshot-v1-128k`, `moonshot-v1-32k` (current K2-series naming)

### 1. Prompt structure recommendations

Kimi expects an explicit **identity declaration at the top** of the system prompt:

> "You are Kimi, an AI assistant developed by Moonshot AI."

The docs warn that omitting this OR substituting a different identity ("you are Greg's classifier") changes Kimi's safety/refusal behaviour unpredictably. Best practice: start with the canonical identity, then layer the specialist role.

Recommended order:

1. **Identity declaration** — `"You are Kimi, an AI assistant developed by Moonshot AI."`
2. **Specialist role layer** — `"For this conversation you act as a contract clause classifier."`
3. **Citation/sourcing rules** — explicit instructions to quote source text for any claim (mitigates Kimi's tendency to hallucinate when context is long).
4. **Task & instructions.**
5. **Context** (the long doc / clause / data).
6. **Output format.**
7. **Examples** (optional — Kimi handles zero-shot well on K2.5).

### 2. JSON output mechanism

OpenAI-compatible — `response_format={"type": "json_object"}` works.

```python
client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.ai/v1")
response = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[...],
    response_format={"type": "json_object"},
    temperature=0.3,
)
```

Kimi K2.5 also supports **structured outputs with JSON Schema** via `response_format={"type": "json_schema", "json_schema": {...}}` — same shape as OpenAI's strict mode. Use this for any schema-critical task; the schema is enforced.

### 3. Delimiter preferences

For long-context tasks (Kimi's specialty — 200K+ context window), **markdown headers** (`## Context`, `## Instructions`) outperform XML. Moonshot's docs explicitly recommend markdown for >50k token prompts.

For short prompts, either works.

### 4. Classification task framing

Kimi handles **open-ended classification** noticeably better than DeepSeek does, but multiple-choice with enum is still safer. For long-document classification (Kimi's sweet spot), require the model to **quote the source span** that justifies the classification — reduces hallucination materially:

```
OUTPUT FORMAT:
{
  "clause_type": "...",
  "source_quote": "<verbatim text from the input that justifies the classification>",
  "rationale": "..."
}
```

If the model can't produce a verbatim quote, it shouldn't classify. This pattern is from Moonshot's own anti-hallucination guide.

### 5. Temperature default & quirks

- **Default:** `temperature=0.3` (Moonshot's recommended default — lower than other providers' 1.0).
- **For extraction:** `temperature=0` works fine.
- **For long-context with citations:** keep `temperature=0` and set `top_p=0.9` — Kimi cites more accurately at constrained sampling.
- **Tool calls:** Kimi K2.5 supports OpenAI-compatible tools. **Avoid over-prescribing tool usage** in the prompt — Kimi decides autonomously and over-applies tool guidance if you specify it. The docs say "trust the model to choose tools."
- **Web search:** built-in via `tools=[{"type": "web_search"}]`, $0.005/call. Cheap; useful for Researcher role.
- **Caching:** prompt caching reduces input cost to ~$0.15/M on cache hits. Cache the system message and any static context.

### 6. Worked example

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.ai/v1")

system = """You are Kimi, an AI assistant developed by Moonshot AI.

For this conversation you act as a contract clause classifier. You categorise clauses by type, assess risk on a 1-5 scale, and ALWAYS quote the verbatim source span that justifies your classification.

## Sourcing rules
- Every classification MUST include a `source_quote` field containing text copied verbatim from the input.
- If you cannot find a verbatim quote that justifies the classification, set `clause_type` to "other" and `source_quote` to "".
- Do not paraphrase the source quote.

## Risk anchors
1 = boilerplate, no negotiation needed
2 = mildly unusual but acceptable
3 = noteworthy, flag in summary
4 = material exposure, recommend redline
5 = catastrophic, escalate to partner
"""

response = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": (
            "## Input clause\n\n"
            "Customer indemnifies Supplier against any third-party IP claims arising "
            "from Customer's modifications to the Software.\n\n"
            "## Task\n\n"
            "Classify the clause above. Return JSON with clause_type, risk_score, "
            "source_quote (verbatim), and rationale."
        )}
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
                        "governing_law", "auto_renewal", "other"
                    ]},
                    "risk_score": {"type": "integer", "minimum": 1, "maximum": 5},
                    "source_quote": {"type": "string"},
                    "rationale": {"type": "string"}
                },
                "required": ["clause_type", "risk_score", "source_quote", "rationale"],
                "additionalProperties": False
            }
        }
    },
    temperature=0,
)
```

### 7. Known anti-patterns

- **Don't** omit the "You are Kimi" identity declaration — changes safety behaviour unpredictably.
- **Don't** over-specify tool usage in the prompt — Kimi over-applies. Trust the model to choose.
- **Don't** rely on classification without `source_quote` for long-doc tasks — Kimi hallucinates more than Gemini/Claude on >50k contexts.
- **Don't** use XML tags for prompts >50k tokens — markdown headers outperform.
- **Don't** set `temperature=1.0` for extraction — Kimi's recommended default is 0.3, and structured tasks want 0.
- **Don't** skip caching on long static contexts — Kimi caching gives ~75% input cost reduction.

---

## xAI — Grok-4 / Grok-4.1 / Grok-3

**Provider docs URL:** https://docs.x.ai/docs/guides/prompt-engineering + https://docs.x.ai/docs/guides/structured-outputs + https://docs.x.ai/docs/guides/live-search
**Date captured:** 2026-05-18
**Applies to model IDs:** `grok-4`, `grok-4.1`, `grok-3`, `grok-3-mini`, `grok-code-fast-1`

### 1. Prompt structure recommendations

Grok is OpenAI-compatible and behaves similarly to GPT-4o on prompt structure. Recommended order:

1. **System message** — role, rules, tone (especially important for Grok-3 because it defaults to "edgy" — explicitly set tone if you want it sober).
2. **User message** — task, then context, then question (Grok handles both context-first and question-first, with a slight preference for question-first for short prompts).
3. **For reasoning tasks (Grok-4)**: state the reasoning depth required explicitly — `"Think step by step before answering"` lifts accuracy by ~5-10pp on hard problems even though Grok-4 has internal reasoning.

### 2. JSON output mechanism

Two options:

1. **`response_format={"type": "json_object"}`** — shape-only, like DeepSeek. Prompt must mention "JSON" somewhere.
2. **`response_format={"type": "json_schema", "json_schema": {...}}`** — strict mode (Grok-3 onwards). Schema is enforced; missing/extra fields are impossible. **Use this for all production extraction.**

```python
from openai import OpenAI

client = OpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1")

response = client.chat.completions.create(
    model="grok-4.1",
    messages=[...],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "classified_clause",
            "strict": True,
            "schema": { ... }
        }
    },
    temperature=0,
)
```

### 3. Delimiter preferences

Markdown headers and plain text both work. XML tags work but provide no documented lift. xAI's docs lean towards **markdown for readability**, no strong stance on delimiter type.

### 4. Classification task framing

Multiple-choice with enum, same as everyone else. Grok handles graded scales (1-5) well without explicit anchors but anchors make it more consistent across runs.

**For contrarian/debate tasks** (Council Contrarian role): Grok-3 is purpose-built for this. You DO NOT need to instruct it to be contrarian — that's its default voice. Instead, if you want a neutral/sober Grok, you must explicitly say `"Provide a balanced, non-adversarial response."` Otherwise it leans hot.

### 5. Temperature default & quirks

- **Default for chat:** `temperature=1.0`.
- **For extraction:** `temperature=0`.
- **Grok-4 reasoning effort:** set `reasoning_effort="low"|"medium"|"high"`. Defaults to `high` which is expensive — drop to `low` for simple tasks. Grok-4.1 does NOT support `reasoning_effort` (it's not a reasoning model in the same way).
- **Live Search** (Grok's web/X search): set `search_parameters={"mode": "on"|"auto", "sources": [{"type": "web"}, {"type": "x"}]}`. Costs $2.50–$5 per 1K calls. Do NOT hardcode "use web search" in prompts when this parameter is available — the API is the right place.
- **Grok-Code-Fast-1:** purpose-built for code. Skip rich prose context; lead with the code/task. Reasoning effort not supported.

### 6. Worked example

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["XAI_API_KEY"], base_url="https://api.x.ai/v1")

response = client.chat.completions.create(
    model="grok-4.1",
    messages=[
        {"role": "system", "content": (
            "You are a contract clause classifier. You categorise clauses by type "
            "and assess risk on a 1–5 scale. Provide a balanced, professional tone — "
            "no editorialising."
        )},
        {"role": "user", "content": (
            "## Task\nClassify the clause below by type and risk.\n\n"
            "## Risk anchors\n"
            "1 = boilerplate, 2 = mildly unusual, 3 = noteworthy, "
            "4 = material exposure, 5 = escalate.\n\n"
            "## Clause\n"
            "Customer indemnifies Supplier against any third-party IP claims arising "
            "from Customer's modifications to the Software.\n\n"
            "Return JSON matching the schema."
        )}
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
                        "governing_law", "auto_renewal", "other"
                    ]},
                    "risk_score": {"type": "integer", "minimum": 1, "maximum": 5},
                    "rationale": {"type": "string"}
                },
                "required": ["clause_type", "risk_score", "rationale"],
                "additionalProperties": False
            }
        }
    },
    temperature=0,
)
```

### 7. Known anti-patterns

- **Don't** hardcode "use web search" / "search X for..." in prompts when `search_parameters` API exists — the parameter is the supported path; prompt-level instructions are unreliable.
- **Don't** use Grok-3 for sober/professional output without explicitly setting tone — defaults to edgy/contrarian.
- **Don't** leave `reasoning_effort` at default `high` on Grok-4 for trivial tasks — costs 3-5× more for no quality lift.
- **Don't** send long prose context to Grok-Code-Fast-1 — it's tuned for code-in / code-out; prose context wastes budget.
- **Don't** rely on `json_object` mode for production — use `json_schema` (strict) instead. `json_object` is shape-only.

---

## OpenAI — GPT-5.3 Codex / GPT-4o / o-series

**Provider docs URL:** _pending — populated on next weekly run_
**Date captured:** _pending — flagged for population by the weekly model-research agent_

**Stub.** OpenAI GPT-5.3 Codex is currently consumed via ChatGPT Plus device auth (`codex_local` adapter), not via the API. Until Greg adds an OpenAI API key (per the post-Codex-tracking decision in `MODEL-RESEARCH.md`), per-model API prompting guidance is deferred.

When this section is populated, expected coverage:
- GPT-5.3 Codex (Codex CLI behaviour — different from API)
- GPT-4o + GPT-4o mini (chat / vision)
- o3, o4-mini (reasoning models — temperature ignored, reasoning_effort parameter)
- Structured Outputs (`response_format={"type": "json_schema", "strict": true}`)
- Developer message vs system message vs user message hierarchy

**Auto-populate trigger:** weekly Researcher run, after the OpenAI API key is added to Paperclip.

---

## Mistral — Large 3 / Small 4 / Codestral

**Provider docs URL:** _pending — populated on next weekly run_
**Date captured:** _pending — flagged for population by the weekly model-research agent_

**Stub.** Mistral is not currently in active use across Paperclip agents (per LLM-MATRIX.md). Will be populated when first agent assignment lands or on weekly research run.

Expected coverage: Mistral's `prefix=True` assistant message trick for JSON forcing, Codestral's code-specific patterns, Magistral 1.2's reasoning interface.

---

## Alibaba — Qwen 2.5-Max / Qwen-Plus / Qwen-Turbo

**Provider docs URL:** _pending — populated on next weekly run_
**Date captured:** _pending — flagged for population by the weekly model-research agent_

**Stub.** Qwen is OpenAI-compatible via DashScope. Expected coverage: Qwen-Plus 1M context strategies, local Qwen2.5 via Ollama prompt differences, Qwen-Max enterprise tuning notes.

---

## Zhipu AI — GLM-5 / GLM-4.7 / GLM-4.7-Flash

**Provider docs URL:** _pending — populated on next weekly run_
**Date captured:** _pending — flagged for population by the weekly model-research agent_

**Stub.** GLM uses Zhipu's proprietary API (open.bigmodel.cn), not OpenAI-compatible. Populated when first agent assignment lands.

---

## MiniMax — M2.7

**Provider docs URL:** _pending — populated on next weekly run_
**Date captured:** _pending — flagged for population by the weekly model-research agent_

**Stub.** MiniMax is a fallback for Engineer when Codex quota is exhausted (per LLM-MATRIX.md). Section will be populated on next weekly run.

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

_Last updated: 2026-05-18 — initial creation with 5 fully-filled provider sections (Anthropic, Google, DeepSeek, Moonshot, xAI) + 5 stubs (OpenAI, Mistral, Qwen, GLM, MiniMax)._
