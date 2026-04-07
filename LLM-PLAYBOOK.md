# LLM Playbook — Life Admin Agent Team

_Maintained by Researcher. Last updated: 2026-04-07._

This document is Clawdy's reference for two things:
1. **Who is running what** — which model is currently active for each agent
2. **How to talk to them** — prompting style per LLM family

---

## How Clawdy Uses This

When composing a prompt that will be sent to another agent (via council-debate, a delegated task, or direct API call), Clawdy should:

1. Read `D:\paperclip\positions\positions.json` → find the agent's `active_model`
2. Look up that model in this playbook → apply the prompting style
3. Adapt the prompt accordingly before sending

This matters most in two scenarios:
- **Council debates** — each council member runs a different LLM; tailored prompts get better arguments
- **API billing mode** — when Max plan ends and every token costs money, efficient prompts reduce costs significantly

---

## Current Agent Roster

_Source: `D:\paperclip\positions\positions.json` — always check for current fallback state_

| Agent | Character | Current Model | Adapter |
|-------|-----------|--------------|---------|
| CEO | Clawdy | claude-opus-4-6 | claude_local |
| CTO | Gayan | claude-opus-4-6 | claude_local |
| COO | — | claude-sonnet-4-6 | claude_local |
| Yoda | Yoda | claude-opus-4-6 | claude_local |
| Senior Engineer | — | deepseek-chat | ollama_local |
| QA Bot | — | deepseek-chat | ollama_local |
| Engineer | — | gpt-5.3-codex | codex_local |
| Council Tech | — | gpt-5.3-codex | codex_local |
| Designer | — | gemini-2.5-flash | gemini_local |
| Finance | — | deepseek-reasoner (R1) | ollama_local |
| Cyber Security (Sentry) | — | deepseek-reasoner | ollama_local |
| Doc | — | gemma4:26b | ollama_local (LOCAL ONLY) |
| Freud | — | gemma4:26b | ollama_local (LOCAL ONLY) |
| Council Local | — | gemma4:26b | ollama_local (LOCAL ONLY) |
| Researcher | — | grok-4.1 | ollama_local |
| Contrarian | — | grok-3 | ollama_local |
| Spielberg | — | grok-3-mini | ollama_local |
| Content Lead | — | mistral-large-latest | ollama_local |
| Council EU | — | mistral-large-latest | ollama_local |
| Council CH | — | kimi-k2.5 | ollama_local |
| Travel Agent | — | kimi-k2.5 | ollama_local |
| Accountant | — | deepseek-chat | ollama_local |

---

## Critical Concept: Reasoning Models vs Standard Models

Two models in the lineup are **reasoning models** — they generate an internal chain of thought before answering:

| Model | Type |
|-------|------|
| DeepSeek R1 (deepseek-reasoner) | Reasoning |
| (future: o1, o3 variants) | Reasoning |

**Reasoning models need different prompting:**
- ❌ Don't say "think step by step" — they already do this internally
- ❌ Don't write long instructional system prompts about how to reason
- ✅ Give them the problem clearly and briefly — let them reason
- ✅ Short, focused system prompts only
- ✅ They'll produce a `<think>` block before the actual answer — this is normal

All other models are **standard instruction-following models** and accept detailed prompts.

---

## Per-Model Prompting Guides

---

### Claude (Anthropic) — Opus 4.6, Sonnet 4.6, Haiku 4.5

**Used by:** CEO, CTO, COO, Yoda

**Core style:**
- XML tags for structured requests work extremely well: `<task>`, `<context>`, `<constraints>`, `<output_format>`
- System prompts are strongly respected — role framing here is very effective
- Explicit output format instructions are followed precisely
- Handles ambiguity well — can make reasonable judgments without over-specifying

**Tier differences:**

| Tier | When to use | Prompting notes |
|------|------------|-----------------|
| Opus 4.6 | Complex reasoning, strategic decisions, nuanced judgment | Give it full context; it can handle 200K tokens; it excels at weighing competing concerns |
| Sonnet 4.6 | Writing-heavy tasks, balanced quality/speed | Best for drafts, structured analysis, content creation |
| Haiku 4.5 | Structured/repetitive tasks, fast turnaround | Keep prompts shorter and directive; it's less reliable on open-ended reasoning |

**Example structure for Opus/Sonnet:**
```
System: You are [role]. [Context about the situation].

<task>
[Specific task description]
</task>

<context>
[Relevant background]
</context>

<output_format>
[Exactly what you want back]
</output_format>
```

---

### Grok (xAI) — Grok-3, Grok-4.1, Grok-3-Mini, Grok Code Fast 1

**Used by:** Researcher (4.1), Contrarian (3), Spielberg (3-Mini)

**Core style:**
- More direct than Claude — get to the point faster
- System prompts work but are less powerful than Claude's; compensate with explicit task framing in the user turn
- Better to be explicit about format: "Respond in exactly 3 paragraphs" beats vague instructions
- Less benefit from XML tags; plain markdown headers work fine

**Tier differences:**

| Model | Strengths | Prompting notes |
|-------|-----------|-----------------|
| Grok-4.1 | Deep research, thorough analysis | Give it permission to be thorough: "Research this in depth, prioritise completeness over brevity." |
| Grok-3 | Strong reasoning, adversarial analysis, debates | Excellent for Contrarian role — prime it for the adversarial angle explicitly |
| Grok-3-Mini | Mid-tier tasks, value | Keep prompts concise; good at structured outputs |
| Grok Code Fast 1 | Code-only tasks | Minimal prose context; just code + error + instruction |

**Researcher-specific (Grok-4.1):**
```
You are conducting deep research on [topic]. 
Prioritise completeness and evidence over brevity.
Cover: [angle 1], [angle 2], [angle 3].
Format: executive summary → key findings → evidence → gaps
```

**Contrarian-specific (Grok-3):**
```
You are the devil's advocate in this debate.
Your role is to challenge, stress-test, and find weaknesses in: [position/proposal].
Be specific and evidence-based in your objections.
Don't be contrarian for its own sake — identify genuine risks.
```

---

### Gemma 4 26B (Google Local / Ollama)

**Used by:** Doc, Freud, Council Local  
**CRITICAL: This is the ONLY local model. All health data stays on this model only — never route health queries to cloud.**

**Core style:**
- Runs via Ollama — system + user format, no chat history by default
- Shorter system prompts work better; long system prompts dilute instruction-following
- Direct, concrete task descriptions
- Template-style prompting works well: show the exact format you want
- Role assignment in system prompt is effective

**Config parameters that work well:**
- Temperature: 0.3–0.4 for factual/analysis tasks; 0.6–0.7 for reflective/creative
- num_predict: 2000–3000 for substantive responses
- Context: 128K max

**For Doc (health advisor):**
```
System: You are Doc, a knowledgeable health advisor speaking confidentially with Greg. 
All information is private and handled with care. Provide balanced, evidence-based guidance.
Be direct and practical. Flag when professional in-person advice is needed.

User: [health question or data]
```

**For Freud (reflection/psychology):**
```
System: You are Freud, a reflective advisor helping Greg understand patterns in his thinking and behaviour.
Thoughtful, unhurried tone. Ask clarifying questions. Do not rush to conclusions.
All conversations are private.

User: [reflection prompt]
```

---

### DeepSeek (DeepSeek AI) — V4 (chat) and R1 (reasoner)

**Used by:** Senior Engineer, QA Bot, Accountant (V4) | Finance, Cyber Security (R1)

#### DeepSeek V4 (deepseek-chat)

Standard instruction-following model. Code-optimised.

- System + user message format; system prompt is respected
- For code: include language, framework, existing style examples, full error messages
- Excellent at following structured output templates (JSON, markdown tables, numbered lists)
- Provide context file by file when reviewing code
- Similar prompting to GPT-4o style

**For code tasks:**
```
System: You are a [role]. You work in [language/framework].
Code style: [relevant conventions — e.g. TypeScript strict mode, async/await preferred]

User: [file context or error]
Task: [specific instruction]
Expected output: [code block / explanation / both]
```

#### DeepSeek R1 (deepseek-reasoner) ⚠️ REASONING MODEL

**DO NOT** instruct it on how to reason. Give it the problem; let it think.

- Short system prompt only — set role and constraints
- User turn should be clear and complete but not prescriptive about method
- Expect a `<think>...</think>` block in output before the answer — this is the reasoning trace
- Exceptional at: financial analysis, structured logical problems, multi-factor risk assessment

**For Finance:**
```
System: You are a financial analyst. Be precise. Show your workings.

User: [financial data / scenario]
Question: [the specific question]
```

**For Cyber Security:**
```
System: You are a senior cybersecurity analyst. Prioritise accuracy over speed.

User: [threat scenario / code / logs]
Question: [what are the risks / attack vectors / recommended mitigations]
```

---

### Mistral (Mistral AI) — Large 3, Small 4, Codestral

**Used by:** Content Lead, Council EU (Large 3)

**Core style:**
- Clear, task-focused prompts; system prompts are reliably followed
- Natively multilingual — can prompt in French or German if diversity of perspective is needed
- Good at structured analysis and formal writing
- Handles long documents reliably

**For Council EU (Mistral Large 3):**
```
System: You represent a European regulatory and values perspective in this debate.
Consider: GDPR, EU AI Act, proportionality, human rights frameworks, institutional trust.
Be specific, cite regulatory context where relevant.

User: [debate topic or question]
```

**For Content Lead (Mistral Large 3):**
```
System: You are a content strategist. [Target audience]. [Brand voice — professional/casual/etc.]
Output format: [blog post / social copy / structured brief / etc.]

User: [content brief]
```

**Codestral:** Code-only. Treat like Grok Code Fast 1 — minimal prose, just code context + task.

---

### Kimi K2.5 (Moonshot AI)

**Used by:** Travel Agent, Council CH

**Core style:**
- Research-oriented; give it sources or data to work from when available
- Excellent at multi-factor analysis (e.g. comparing travel options across price/time/quality)
- Clear research scope boundaries: "Focus on X, not Y" prevents drift
- JSON and structured markdown output works well
- Natively bilingual (Chinese/English) — for Council CH, can prime for Chinese-market perspective

**For Council CH:**
```
System: You represent a Chinese market and technology perspective in this debate.
Consider: scale, pragmatism, speed of adoption, alternative ecosystems (WeChat, Alibaba, Huawei).
Be direct and evidence-based. Challenge Western assumptions where relevant.

User: [debate topic]
```

**For Travel Agent:**
```
System: You are a travel research specialist. Prioritise: [budget / experience / safety / practicality — pick relevant ones].

User: [destination + dates + constraints + preferences]
Task: Research and compare [specific options]. Return a structured comparison.
```

---

### Gemini 2.5 Flash (Google)

**Used by:** Designer (Fallback 1)

**Core style:**
- 1 MILLION token context window — use it liberally; don't compress context unnecessarily
- Very reliable at following multi-constraint instructions
- JSON output mode is very accurate when requested
- Can be verbose — add explicit length constraints: "in under 400 words" or "5 bullet points max"
- Natively multimodal — can accept image descriptions or image data if the adapter supports it
- Google system instructions format works well

**For Designer:**
```
System: You are a UI/UX designer for [project]. 
Brand: [colours, fonts, tone — reference BRAND.md if Shine work].
Accessibility: WCAG AA minimum.

User: [design task — describe existing component + what change is needed + why]
```

---

### GPT-5.3 Codex (OpenAI)

**Used by:** Engineer, Council Tech  
**Note:** Task-limited Codex plan — save for coding work only

**Core style:**
- Best coding model in the lineup — but only use it for code
- Standard OpenAI system + user format
- Include: codebase context, existing style, the specific task, expected output
- Agentic coding loop: plan → implement → test; prompt each step separately
- For debugging: include full stack trace, relevant file contents, steps to reproduce

**For Engineer:**
```
System: You are a senior [language] engineer. 
Stack: [tech stack].
Style: [TypeScript strict / async/await / component patterns — relevant conventions]

User: [task description]
Relevant code:
[paste relevant files/functions]

Task: [implement X / fix Y / refactor Z]
Output: complete, runnable code with any necessary tests
```

---

### MiniMax M2.7 (MiniMax)

**Used by:** Various fallback slots  
Standard capable model. Treat as a reliable general-purpose fallback.

- Standard system + user format
- Clear, direct task descriptions
- Works well with structured output templates
- No special prompting quirks; standard best practices apply

---

### Qwen Plus (Alibaba)

**Used by:** Various fallback slots

- Solid all-rounder, good multilingual capability (Chinese + English)
- Can reason from Chinese market context if prompted
- Standard instruction-following; clear system prompts work well
- Useful when geographic or market diversity in perspective is valuable

---

## Quick Cheatsheet

| Model family | Key prompt pattern | Avoid |
|---|---|---|
| Claude | XML tags + detailed system prompt | Vague instructions |
| Grok-4.1 | "Research this in depth, prioritise completeness" | Brevity constraints |
| Grok-3 | Explicit adversarial framing | Generic "be helpful" |
| Grok-3-Mini | Short, direct | Long preamble |
| Gemma 4 26B | Short system prompt + concrete template | Long system prompts |
| DeepSeek V4 | Code context + style examples | Over-explaining the task |
| DeepSeek R1 ⚠️ | Problem only — let it reason | "Think step by step" |
| Mistral Large | Clear task focus, formal if needed | Casual/vague framing |
| Kimi K2.5 | Explicit scope + structured output | Open-ended drift |
| Gemini 2.5 Flash | Use the full context window freely | Forgetting length constraints |
| GPT-5.3 Codex | Full code context + task | Using it for prose |

---

## Maintenance — Researcher's Responsibility

The Researcher agent maintains this document. Update when:
- A model is added, removed, or falls back (check positions.json weekly)
- New pricing or benchmarks are published (update llm-matrix-data.json first)
- Prompting best practices are discovered through use (add to per-model section)
- A new model family is onboarded to the team

**Update protocol:**
1. Check `positions.json` for current active models → update the Roster table
2. Check provider pages for updated pricing → update `llm-matrix-data.json`
3. Update this playbook with any new prompting insights
4. Update `last_updated` date at top of this file
