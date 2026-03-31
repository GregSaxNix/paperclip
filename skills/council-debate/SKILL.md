---
name: council-debate
description: Multi-LLM adversarial debate system. Distributes a question to multiple AI providers, collects perspectives, and synthesises a recommendation via the Council Judge (Yoda).
---

# Council of Elders — Multi-LLM Debate

Use this skill when you need multiple AI perspectives on an important decision. The Council of Elders is an adversarial debate system where agents powered by different AI providers argue FOR and AGAINST a proposal, then the Judge (Yoda) synthesises the best answer.

## When to Use

- Business strategy decisions (e.g. "Should we prioritise TalentMap features or new client acquisition?")
- Architecture or technology choices
- Investment analysis
- Any non-obvious decision where multiple perspectives add value

**Do NOT use for:**
- Routine tasks or simple questions
- Decisions where speed matters more than thoroughness
- Low-stakes choices

## How It Works

1. **Trigger:** An issue is created with `[COUNCIL]` in the title, in the "Council Debates" project
2. **Distribute:** The orchestrator (CEO agent) creates sub-issues assigned to each council member:
   - Claude perspective → assigned to Clawdy (Shine) or Skippy (Life Admin)
   - Codex perspective → assigned to Codex agent
   - Gemini perspective → assigned to Gemini agent
   - Local perspective (optional) → assigned to Guardian (Ollama, for privacy-sensitive debates)
3. **Deliberate:** Each agent responds with their perspective using the format below
4. **Synthesise:** Yoda reads all perspectives and posts a synthesis on the parent issue
5. **Decide:** Greg (Board) reads Yoda's synthesis and makes the final call

## Privacy Rule

If a debate involves sensitive health or family data:
- **Exclude cloud providers** (Codex, Gemini)
- Use only **Claude** (Max plan, not API-billed) and **Guardian** (local Ollama)
- Yoda can still judge

## Perspective Prompt Template

When assigned a council debate sub-issue, respond using this format:

```
You are participating in a Council of Elders debate on the following question:

[QUESTION FROM PARENT ISSUE]

Your role: Provide your honest, independent perspective. Consider:
- Arguments FOR the proposal
- Arguments AGAINST the proposal
- Risks and blind spots
- What information is missing
- Your recommendation and confidence level (high/medium/low)

Be direct and specific. Disagree with other perspectives if you genuinely see it differently.
Do not hedge or give a non-answer. Take a position.
```

### Response Format

```
## Position: [FOR / AGAINST / CONDITIONAL]

## Key Arguments
- [bullet points]

## Risks
- [bullet points]

## Recommendation
[1-2 sentences]

## Confidence: [HIGH / MEDIUM / LOW]
```

## Yoda's Synthesis Format

When Yoda reads all perspectives, respond using this format:

```
## Consensus Points
[Where do the perspectives agree?]

## Tension Points
[Where do they disagree? Who has the stronger argument and why?]

## Blind Spots
[What did none of them consider?]

## Recommendation
[Synthesised recommendation for the Board]

## Key Risk
[The single biggest risk of following this recommendation]

## Unresolved
[What needs more information before a final decision]
```

## Creating a Council Debate

To start a debate, create an issue in the "Council Debates" project:

**Title:** `[COUNCIL] Your question here`

**Description:** Context about the decision, constraints, relevant data, and which council members should participate.

Then create sub-issues for each participant:
- `[COUNCIL-PERSPECTIVE] Claude: [question]` → assign to Clawdy/Skippy
- `[COUNCIL-PERSPECTIVE] Codex: [question]` → assign to Codex agent
- `[COUNCIL-PERSPECTIVE] Gemini: [question]` → assign to Gemini agent
- `[COUNCIL-PERSPECTIVE] Local: [question]` → assign to Guardian (optional)
- `[COUNCIL-SYNTHESIS] [question]` → assign to Yoda (runs after all perspectives are in)

Each sub-issue should reference the parent issue ID so Yoda can find all perspectives.

## Budget Awareness

Each debate costs tokens across multiple providers. The Council is for decisions that matter — not routine questions.

## Notes

- The Board (Greg) always makes the final call — Yoda recommends, Greg decides
- Australian English in all responses
- All perspectives should be genuinely independent — don't read other perspectives before posting yours
