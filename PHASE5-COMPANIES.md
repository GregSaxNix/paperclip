# Phase 5: Company Structure & Agent Configuration

Paste everything below this line into the Paperclip Cursor session after Phase 4 (Security & Hardening) is complete.

---

## Context

The migration phases 0-4 are done. Now we need to set up the two-company structure and configure agents for each. This replaces the original Phase 5 (Council of Elders) — that moves to Phase 7 since it needs multiple adapters working first.

## Two Companies to Create

### Company 1: Shine Operations

**Purpose:** All business and work — recruitment, client projects, coding projects, business admin.

**Projects to create within this company:**
- TalentMap (existing app at `D:\TalentMap\shine-talentmap-app\`)
- Website (check `D:\` and `D:\VS Code Projects\` for exact path)
- Waybook clone (check `D:\` and `D:\VS Code Projects\`)
- MS 365 clone (not started yet — only desktop chat history exists, no repo)
- Whisper Transcribe (check `D:\` and `D:\VS Code Projects\`)
- VoiceClone (check `D:\` and `D:\VS Code Projects\`)
- Digital Twin (check `D:\` and `D:\VS Code Projects\`)
- Client Recruitment (general recruitment work)
- Business Admin (invoicing, operations, etc.)

**Agents:**
- **Clawdy** — primary agent, `claude_local` adapter (Max plan). Professional tone. Migrate the existing SOUL.md and MEMORY.md from the Phase 1 setup into this company.
- Additional agents as needed per project.

### Company 2: Life Admin

**Purpose:** All personal and family — health management, personal projects, hobbies, family scheduling.

**Projects to create within this company:**
- Health Management (Lana — developmental delays/autism, Kobi — ADHD. SENSITIVE DATA — must use local agent once available)
- Family Scheduling
- Personal Finances
- YouTube Second Brain
- Music Generator (check `D:\` and `D:\VS Code Projects\`)
- TravelPlanner (check `D:\` and `D:\VS Code Projects\`)
- Tech-Stocks (check `D:\` and `D:\VS Code Projects\`)
- Textbook Scrape (check `D:\` and `D:\VS Code Projects\`)

**Agents:**
- A personal-tone agent using `claude_local` adapter (Max plan). More casual than Clawdy — this is personal/family stuff, not business.
- Health-related tasks will later use a local Ollama/4090 agent (Phase 6) so sensitive data never leaves the machine. For now, use the Claude agent but flag health projects as "future local processing."

## Agent Configuration Process

For each agent, Greg will describe what he wants in plain language. Claude configures:
1. **SOUL.md** — personality, tone, boundaries, behaviours
2. **Memory files** — MEMORY.md for long-term context, daily journals
3. **Skills** — which skills the agent has access to
4. **Adapter** — which AI provider (claude_local for Max plan agents)
5. **Routines** — any scheduled tasks (daily check-ins, monitoring, etc.)

Ask Greg questions to shape each agent's personality rather than guessing. For example:
- "Should this agent be formal or casual?"
- "What should it never do?"
- "What's the most important thing it needs to be good at?"

## Cross-Company Notes

- Code projects live on the filesystem, not inside Paperclip. Any agent from either company can be pointed at any directory.
- Company isolation is about task tracking, budgets, and audit trails — not filesystem access.
- Skills and plugins work across both companies.
- Greg accesses both companies from the same dashboard.

## Critical Reminders

- Australian English everywhere (colour, organisation, normalise)
- All Claude agents use `claude_local` adapter — NEVER set ANTHROPIC_API_KEY
- Dark slate theme should already be applied from Phase 1
- Greg is a vibe coder — explain things in plain language, give click-by-click navigation paths
- When asking Greg to test something, include the navigation path (e.g., "Go to **Shine Operations > Agents > Clawdy** and click **Details**")

## Revised Phase Order

- Phase 5: Two companies + projects + agent personalities (THIS PHASE)
- Phase 6: Ollama/4090 private agent for Life Admin health data
- Phase 7: Council of Elders plugin (multi-LLM debate — needs multiple adapters)
- Phase 8: Validation & cutover

## What to Do First

1. Scan `D:\` and `D:\VS Code Projects\` to find exact paths for all the projects listed above
2. Create the Shine Operations company with its projects
3. Move/configure Clawdy into Shine Operations
4. Create the Life Admin company with its projects
5. Ask Greg about the Life Admin agent personality
6. Configure routines for both companies
