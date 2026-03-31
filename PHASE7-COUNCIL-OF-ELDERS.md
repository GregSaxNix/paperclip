# Phase 7: Council of Elders — Multi-LLM Debate System

Paste everything below this line into the Paperclip Cursor session.

---

## Context

All migration phases (0-6) are complete. Two companies running, 9 agents configured, 51 skills installed and vetted, Telegram working with two-way comms, Microsoft 365 credentials stored. This is the final major feature build.

## What We're Building

A **Council of Elders** — a multi-LLM adversarial debate system where agents powered by different AI providers argue FOR and AGAINST a proposal, then a Judge agent (Yoda) synthesises the best answer.

**Why:** Different LLMs have different strengths, biases, and blind spots. Getting multiple perspectives on important decisions (business strategy, architecture choices, investment analysis) produces better outcomes than asking one model.

## Architecture

```
Greg (Board) creates a "Council Debate" issue
    ↓
Council orchestration triggers all participants:
    ├── Claude perspective (Clawdy or dedicated council agent — claude_local)
    ├── Codex perspective (new agent — codex-local adapter)
    ├── Gemini perspective (new agent — gemini-local adapter)
    └── Ollama perspective (Guardian — local 4090, optional)
    ↓
Each agent posts their perspective as a comment on the issue
    ↓
Yoda (Judge) reads all perspectives and synthesises a final recommendation
    ↓
Greg reviews and makes the final call
```

## Step 1: Set Up Additional Adapters

### Codex (OpenAI)

Greg needs to do ONE thing in his browser first:
1. Go to **https://chatgpt.com** → **Settings** → **Security**
2. Enable **"Device code authorisation for Codex"**
3. Tell the Paperclip session it's done

Then in Paperclip:
- Create a `codex-local` adapter
- When first run, it will show a device code for Greg to authorise
- This uses Greg's existing ChatGPT subscription

### Gemini (Google)

Greg needs to get a free API key:
1. Go to **https://aistudio.google.com/apikey** in his browser
2. Sign in with Google account
3. Click **"Create API key"**
4. Copy the key
5. **Add it directly in the Paperclip web UI** — walk Greg through the exact navigation path (e.g., **Instance Settings → Secrets** or the agent's configuration page). NEVER ask him to paste it in chat.

Then in Paperclip:
- Create a `gemini-local` adapter referencing the stored secret

### Ollama (Local — Already Running)
- Guardian agent already uses the local Ollama adapter on the 4090
- Can participate in councils for the private/local perspective
- Optional — not every debate needs a local model

## Step 2: Create Council Agents

### Yoda — Council Judge (Both Companies)

**Create in Shine Operations AND Life Admin** (same name, same role per the naming mandate).

- **Name:** Yoda
- **Role:** Council Elder / Judge — synthesises multiple perspectives into a clear recommendation
- **Adapter:** claude_local (Max plan) — the judge should be the strongest reasoner
- **SOUL.md personality:**
  - Wise, measured, cuts through noise to the essential truth
  - Synthesises multiple perspectives fairly — doesn't favour any single source
  - Speaks plainly (NOT in Yoda syntax — Greg wants clear communication)
  - Identifies where perspectives agree (consensus) and where they disagree (tension points)
  - Always presents: the recommendation, the reasoning, the key risk, and what was left unresolved
  - Australian English
  - Never makes the final decision — always defers to the Board (Greg)

### Council Participants

These are the agents that provide perspectives. They can be existing agents in new roles, or new dedicated agents:

**Option A (Recommended — Simpler):** Use existing agents (Clawdy, Sheldon, Brains) as Claude participants, and create new agents only for Codex and Gemini adapters.

**Option B:** Create dedicated "Council" agents for each provider.

Go with Option A unless Greg says otherwise.

**New agents needed:**

**Codex Elder (Shine Operations + Life Admin)**
- **Name:** Ask Greg — could be a pop culture name like the others (suggest: **Neo** — from The Matrix, different way of seeing the world)
- **Adapter:** codex-local
- **SOUL.md:** Provides the OpenAI/Codex perspective. Direct, pragmatic, focuses on execution feasibility. Australian English.
- **Budget:** $20/month (Codex uses OpenAI credits)
- **maxTurnsPerRun:** 15

**Gemini Elder (Shine Operations + Life Admin)**
- **Name:** Ask Greg — suggest: **Oracle** (The Matrix — sees all possibilities)
- **Adapter:** gemini-local
- **SOUL.md:** Provides the Google/Gemini perspective. Analytical, data-driven, considers scale and search implications. Australian English.
- **Budget:** $15/month (Gemini free tier may suffice)
- **maxTurnsPerRun:** 15

## Step 3: Build the Council Debate Workflow

This can be implemented as either:
- **A Paperclip plugin** (more complex but better UX)
- **A skill + routine** (simpler, uses existing infrastructure)

### Recommended: Skill + Routine Approach

Create a **council-debate** skill that defines the workflow:

1. **Trigger:** Greg creates an issue with a `[COUNCIL]` tag in the title (or a dedicated "Council Debates" project)
2. **Step 1 — Distribute:** Clawdy (or a routine) creates sub-issues assigned to each council member:
   - "Provide Claude perspective on: [original question]" → assigned to Clawdy
   - "Provide Codex perspective on: [original question]" → assigned to Codex Elder
   - "Provide Gemini perspective on: [original question]" → assigned to Gemini Elder
   - (Optional) "Provide local/private perspective on: [original question]" → assigned to Guardian
3. **Step 2 — Deliberate:** Each agent responds in their sub-issue thread with their perspective
4. **Step 3 — Synthesise:** Once all perspectives are in, Yoda's routine picks up the parent issue, reads all sub-issue responses, and posts the synthesis as a comment
5. **Step 4 — Decide:** Greg reads Yoda's synthesis and makes the final call

### Perspective Prompt Template

Each council member should be prompted with:

```
You are participating in a Council of Elders debate on the following question:

[QUESTION]

Your role: Provide your honest, independent perspective. Consider:
- Arguments FOR the proposal
- Arguments AGAINST the proposal
- Risks and blind spots
- What information is missing
- Your recommendation and confidence level (high/medium/low)

Be direct and specific. Disagree with other perspectives if you genuinely see it differently.
Do not hedge or give a non-answer. Take a position.

Format your response as:
## Position: [FOR / AGAINST / CONDITIONAL]
## Key Arguments
[bullet points]
## Risks
[bullet points]
## Recommendation
[1-2 sentences]
## Confidence: [HIGH / MEDIUM / LOW]
```

### Yoda's Synthesis Prompt Template

```
You are Yoda, the Council Judge. Read all perspectives below and synthesise them.

[PERSPECTIVE 1: Claude]
[PERSPECTIVE 2: Codex]
[PERSPECTIVE 3: Gemini]
[PERSPECTIVE 4: Local (if provided)]

Provide your synthesis:
## Consensus Points
[Where do the perspectives agree?]

## Tension Points
[Where do they disagree? Who has the stronger argument and why?]

## Blind Spots
[What did none of them consider?]

## Recommendation
[Your synthesised recommendation for the Board]

## Key Risk
[The single biggest risk of following this recommendation]

## Unresolved
[What needs more information before a final decision]
```

## Step 4: Create a Council Debates Project

In **both companies**, create a project called "Council Debates" where all debate issues live. This keeps them organised separately from regular work.

## Step 5: Test It

Create a test debate issue:

**Title:** `[COUNCIL] Should we prioritise TalentMap features or new client acquisition this quarter?`

**Body:** Context about the business decision, any constraints, relevant data.

Run the full workflow:
1. Verify each council member receives their sub-issue
2. Verify each provides a substantive perspective
3. Verify Yoda synthesises all perspectives
4. Verify the audit trail captures everything

## Important Notes

- **Council debates are NOT for every decision** — they're for important, non-obvious choices where multiple perspectives add value
- **The Board (Greg) always makes the final call** — Yoda recommends, Greg decides
- **Budget awareness** — each debate costs tokens across multiple providers. Use for decisions that matter.
- **Privacy consideration** — if a debate involves sensitive health/family data, exclude cloud providers and use only Claude (Max plan) + Guardian (local Ollama). Yoda can still judge.
- **Australian English** in all agent responses

## API Keys Needed

**SECURITY: NEVER ask Greg to paste API keys into chat. Guide him to the Paperclip web UI instead.**

### Codex (OpenAI)
1. Greg needs to go to **chatgpt.com → Settings → Security** in his browser and enable **"Device code authorisation for Codex"**
2. When the Codex adapter first runs, it will show a device code in the agent's run output
3. Greg authorises it at the URL shown — this is a one-time flow
4. No API key to manually enter — the device auth handles it

### Gemini (Google)
1. Greg needs to get a free API key at **https://aistudio.google.com/apikey** in his browser
2. Greg adds it **directly in the Paperclip web UI**: navigate to the Gemini agent's **Configuration → API Keys** page or the instance secrets settings
3. Walk Greg through the exact navigation path — do NOT ask him to paste it in chat

### Claude and Ollama
Already configured — no additional keys needed.

## What to Do First

1. Create Yoda in both companies
2. Ask Greg for council agent names (suggested: Neo for Codex, Oracle for Gemini — both from The Matrix)
3. Create Codex and Gemini elder agents in both companies
4. Set up codex-local adapter — walk Greg through the device auth flow when it triggers (tell him exactly what to click and where)
5. Set up gemini-local adapter — walk Greg through adding the API key via the Paperclip web UI (give exact navigation path: **Instance Settings → Secrets** or **Agents → [Agent] → Configuration**)
6. Build the council-debate skill with the workflow and prompt templates
7. Create "Council Debates" project in both companies
8. Run the test debate
