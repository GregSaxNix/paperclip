# Memory System Finalisation

Paste everything below this line into the Paperclip Cursor session.

---

## Context

The Memory Engine plugin was already built during migration (at packages/plugins/plugin-memory-engine/) but may not be activated. The para-memory-files skill is installed. The qmd search tool is NOT installed. This phase finalises the memory system.

## Step 1: Check Memory Engine Plugin Status

Check if the Memory Engine plugin is installed and active:
1. Look in the Paperclip UI under plugin management
2. Or check the database for plugin status
3. If not active, build and activate it:
   ```bash
   cd /d/paperclip/packages/plugins/plugin-memory-engine
   pnpm build
   ```
4. Install/register the plugin with Paperclip
5. Verify the dashboard widget appears and the "Memory Facts" tab shows on issue detail pages
6. Verify the daily consolidation job is scheduled (11pm nightly)

## Step 2: Install qmd Search Tool

The para-memory-files skill references `qmd` for semantic memory search but it's not installed.

Research and install qmd:
1. Check what qmd is — it may be a pip package, npm package, or standalone binary
2. Search: `pip install qmd`, `npm install -g qmd`, or check GitHub for `qmd` memory search tool
3. If qmd is not a real/findable tool, implement an alternative:
   - Option A: Use ripgrep (`rg`) for basic text search across memory files (already available)
   - Option B: Build a simple search script that indexes MEMORY.md + daily notes with full-text search
   - Option C: Use the Memory Engine plugin's built-in Memory Search tool instead (it already does full-text search)
4. If qmd doesn't exist as a standalone tool, update the para-memory-files skill to reference the Memory Engine plugin's search tool instead of qmd

## Step 3: Verify Memory System End-to-End

Test the full memory lifecycle:
1. Have an agent (Clawdy) complete a simple issue
2. Run the "Extract Facts from Issue" tool on that completed issue
3. Verify facts appear in the agent's knowledge graph (life/ directory)
4. Run "Memory Search" to find those facts
5. Check that daily notes exist in the agent's memory/ directory
6. Run "Flush to MEMORY.md" and verify entries are promoted
7. Check "Memory Stats" shows correct counts

## Step 4: Configure for All Agents

Ensure the Memory Engine plugin works for all 9 agents across both companies:
- Shine: Clawdy, Sheldon, Sherlock, Nicky, Spielberg, Banksy
- Life Admin: Skippy, Brains, Guardian

Each agent should have:
- A `memory/` directory for daily notes
- A `life/` directory for knowledge graph (PARA structure)
- A `MEMORY.md` for tacit knowledge
- Access to the Memory Search tool

## Step 5: Q&A — How Greg Should Ask Questions

Greg wants to know: should there be a dedicated Q&A agent, or should he just ask the CEO?

**Recommendation: Just ask the CEO (Clawdy or Skippy depending on the company).**

Reasons:
- CEOs already have access to all memory and can delegate if needed
- A separate Q&A agent adds management overhead with little benefit
- If Greg asks Clawdy "What do we know about candidate X?", Clawdy can search memory and respond in the issue thread
- If the question needs research, Clawdy delegates to Brains or the relevant specialist

**How Greg should do it:**
1. Go to the relevant company (Shine or Life Admin)
2. Create a new issue with the question as the title (e.g., "What was the name of that AI tool for transcription I saw on YouTube?")
3. Assign to Clawdy (Shine) or Skippy (Life Admin)
4. The CEO uses Memory Search to find the answer, or delegates to Brains/specialist agents
5. Answer appears in the issue thread

For quick questions that don't need tracking, Greg can also use Telegram commands once two-way comms is fully working.

**Do NOT create a dedicated Q&A agent** — it's unnecessary complexity.

## Important Notes

- The Memory Engine plugin was authored by "Shine People Solutions" during migration — it's custom-built for Greg's setup
- Daily consolidation runs at 11pm AEST — reviews daily notes, extracts facts, merges duplicates, decays stale entries
- Memory is company-scoped — Shine agents can't see Life Admin memory and vice versa
- The plugin adds a dashboard widget and an issue detail tab for browsing memory
- Australian English in all memory entries
