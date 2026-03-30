# Configuration Enhancements — Post Phase 5

Paste everything below this line into the Paperclip Cursor session after the current phase completes.

---

## Context

Phases 0-5 are done. The two companies exist with agents Clawdy (Shine) and Skippy (Life Admin). This phase adds the configuration layers that make Paperclip work properly — goal hierarchies, additional agents, budgets, brand guides, and org charts. These come from the Greg Isenberg live demo of Paperclip and community best practices.

**All agent names are confirmed by Greg — do NOT ask again. Create them exactly as listed below.**

**Note about Sheldon:** Named after Greg's best friend who is (by Greg's account) a shit engineer — but an engineer nonetheless. The name has personal meaning.

**MANDATORY RULE: Agent names must be consistent across companies.** If an agent does the same job in both companies, it MUST have the same name. For example, if Life Admin needs a QA agent, it must be called "Sherlock" — not something different. This avoids confusion. When creating agents in Life Admin that mirror Shine roles, duplicate the name and adjust the SOUL.md for personal tone.

## 1. Goal Hierarchies

Every project needs a measurable goal that traces back to the company mission. Agents work better when tasks carry their full goal ancestry (they know not just *what* but *why*).

**Shine Operations:**
- Company Mission: "Build and scale Shine People Solutions — Australia's leading Aboriginal recruitment and consulting firm, powered by AI-assisted workflows"
- Ask Greg to confirm or adjust this mission
- Then create goals for each project, e.g.:
  - TalentMap: "Launch a production-ready talent mapping application for Aboriginal employment programs"
  - Client Recruitment: "Deliver high-quality recruitment services with AI-assisted candidate sourcing"
  - Business Admin: "Automate invoicing, reporting, and operational tasks to reduce manual work"

**Life Admin:**
- Company Mission: "Keep the Sax family organised, healthy, and on top of everything — with AI handling the admin so Greg doesn't have to remember it all"
- Ask Greg to confirm or adjust
- Goals per project, e.g.:
  - Health Management: "Track and support Lana and Kobi's health needs with structured, private records"
  - YouTube Second Brain: "Build a searchable knowledge base from YouTube content Greg watches"

## 2. Agents & Org Charts

### Shine Operations Org Chart

```
Greg (Board of Directors)
  └── Clawdy (CEO) — claude_local, strategic oversight and delegation
        ├── Sheldon (Engineer) — claude_local, code implementation
        ├── Sherlock (QA) — claude_local, reviews and quality assurance
        ├── Nicky (Content Strategist) — claude_local, comms and documentation
        ├── Spielberg (Video Editor) — claude_local, video/animation content
        └── Banksy (Design) — claude_local, brand/visual work
```

### Confirmed Agent Names & Personalities

**Sheldon — Engineer (Shine Operations)**
- Named after: Sheldon Cooper (The Big Bang Theory)
- Role: Dedicated coding agent for TalentMap, Website, Waybook, and all Shine coding projects
- Adapter: claude_local (Max plan)
- SOUL.md personality: Methodical, precise, systematic. Takes pride in clean code. Follows established patterns. Australian English in all comments and documentation. Takes direction from Clawdy, reports completed work via issue threads. Won't cut corners — if something needs doing properly, says so.
- Skills: Code generation, testing, git operations, build processes

**Sherlock — QA Agent (Shine Operations)**
- Named after: Sherlock Holmes
- Role: Reviews all code and outputs, validates quality, runs tests, flags problems
- Adapter: claude_local (Max plan)
- SOUL.md personality: Observant, detail-oriented, notices what everyone else misses. Deductive approach — traces bugs back to root causes. Firm but fair in reviews. Won't pass something that isn't right, but explains clearly why it failed. Australian English.
- Workflow: Engineer completes task → task moves to "in_review" → Sherlock picks it up → approves or sends back with detailed feedback
- Skills: Code review, security analysis, testing, accessibility checks

**Spielberg — Video Editor (Shine Operations)**
- Named after: Steven Spielberg
- Role: Produces video and animated content for Shine projects (VoiceClone, Digital Twin related)
- Adapter: claude_local (Max plan)
- SOUL.md personality: Visual storyteller, cinematic thinking, attention to pacing and narrative. Understands how to make content engaging. Australian English.
- Skills: Remotion skill (install via `npx remotion skills update`), video scripting, animation

**Banksy — Design Agent (Shine Operations)**
- Named after: Banksy (street artist)
- Role: Brand identity, visual design, UI/UX guidance, marketing materials
- Adapter: claude_local (Max plan)
- SOUL.md personality: Bold, distinctive, thinks about visual impact. Respects the Shine brand identity (see Brand Guide below). Makes things look iconic while staying culturally appropriate. Australian English.
- Skills: Design systems, brand guidelines, CSS/styling, visual composition

**Nicky — Content Strategist (Shine Operations)**
- Named after: Greg's friend in communications
- Role: Analyses product changes, creates client communications, documentation, announcements
- Adapter: claude_local (Max plan)
- SOUL.md personality: Professional tone matching Shine People Solutions brand voice. Understands Aboriginal employment context. Creates clear, respectful communications. Knows how to craft a message that lands. Australian English.

### Life Admin Org Chart

```
Greg (Board of Directors)
  └── Skippy (CEO) — claude_local, personal coordination
        ├── Guardian — Ollama/4090, health data only (Phase 6)
        ├── Brains (Research) — claude_local, deep research
        └── Yoda (Council Elder) — claude_local, wise synthesis (Phase 7)
```

**Brains — Research Agent (Life Admin)**
- Named after: Brains from Thunderbirds
- Role: Deep research for YouTube Second Brain, Tech-Stocks analysis, Textbook Scrape, TravelPlanner research
- Adapter: claude_local (Max plan)
- SOUL.md personality: The genius behind the scenes. Thorough, methodical researcher who digs deep and presents findings in an accessible way. Quietly brilliant — does the heavy analytical work so others don't have to. Australian English.
- Skills: Web research, document analysis, summarisation, knowledge organisation

**Yoda — Council Elder / Judge (Council of Elders — Phase 7)**
- Named after: Yoda (Star Wars)
- Role: Wise synthesis agent for the Council of Elders multi-LLM debate system
- Adapter: claude_local (Max plan) — may also use Ollama for private debates
- SOUL.md personality: Wise, measured, sees through noise to the essential truth. Synthesises multiple perspectives into clear recommendations. Speaks plainly (not in Yoda syntax — Greg wants clear communication). Australian English.
- NOTE: Don't create yet — this agent is part of Phase 7 (Council of Elders plugin)

## 3. Budget Configuration

Even on Max plan (zero Claude cost), budgets matter for future paid adapters and preventing runaway execution.

**Recommended budgets (monthly):**
| Agent | Budget | Rationale |
|---|---|---|
| Clawdy (CEO) | $50 | Strategic work, higher reasoning |
| Sheldon (Engineer) | $30 | Active coding, high volume |
| Sherlock (QA) | $20 | Review work, lower volume |
| Spielberg (Video) | $15 | Periodic video work |
| Banksy (Design) | $15 | Periodic design work |
| Content Strategist | $15 | Periodic communications |
| Skippy (CEO) | $25 | Personal coordination |
| Brains (Research) | $20 | Research can be intensive |
| Guardian (future) | $0 | Local Ollama, no API cost |

Also configure **maxTurnsPerRun** for each agent to prevent runaway execution:
- CEO agents (Clawdy, Skippy): 25 turns
- Sheldon (Engineer): 50 turns (coding can need more iterations)
- Sherlock (QA): 15 turns
- Spielberg, Banksy, Content: 15 turns
- Brains (Research): 30 turns (research needs room to explore)

## 4. Issue Prefixes

Set up prefixes to avoid task ID confusion:
- **Shine Operations:** `SHN-`
- **Life Admin:** `LA-`

## 5. Brand Identity Guide (Shine Operations)

**Greg's brand colours have been extracted from the Shine Website and TalentMap projects. Do NOT ask Greg for these — use the values below.**

Create a `BRAND.md` file that all Shine agents reference:

### Shine People Solutions — Brand Identity Guide

**Company:** Shine People Solutions
**Founder:** Greg Sax (Taungurung man)
**Focus:** Aboriginal recruitment and consulting

**Primary Colour Palette (Taungurung Country Ochre Palette):**
| Colour | Hex | Usage |
|---|---|---|
| Primary Gold | `#df9704` | Core brand colour — buttons, headings, accents |
| Dark Gold/Ochre | `#c47a2c` | Hover states, secondary accents |
| Ochre | `#a25718` | Earth tones, supporting colour |
| Accent Brown | `#8B4513` | Grounding elements |
| Copper | `#CD853F` | Warm accents |
| Cream | `#F5DEB3` | Light backgrounds, cards |
| Light Gold | `#FDF6E3` | Subtle backgrounds |

**Dark Mode Colours:**
| Colour | Hex | Usage |
|---|---|---|
| Background | `#1a1a1a` | Main background |
| Card Background | `#242424` | Card surfaces |
| Card Border | `#3a3a3a` | Card edges |
| Foreground Text | `#ededed` | Primary text |
| Muted Text | `#9ca3af` | Secondary text |

**Typography:**
- Body: **Lato** (weights: 300, 400, 700)
- Headings: **Poppins** (weights: 400-900)
- Accent/Display: **Finger Paint** (cursive, used sparingly)

**Tone of Voice:**
- Professional but warm — not corporate-speak
- Culturally respectful — Aboriginal self-determination and cultural safety are non-negotiable
- Plain language — Greg's clients are people, not corporations
- Confident but humble — Shine is proud of its work without being boastful
- Australian English always (colour, organisation, normalise)

**Key Values (Must Be Reflected in All Communications):**
- Aboriginal self-determination
- Cultural safety and respect
- Community-led outcomes
- Practical, real-world impact
- Transparency and honesty

**Things to NEVER Do:**
- Never use deficit language about Aboriginal people or communities
- Never use stock imagery that doesn't represent Aboriginal Australians authentically
- Never make promises the company can't deliver
- Never use jargon that excludes people
- Never compromise on cultural safety for expediency

**Cultural Context:**
The colour palette is inspired by the ochre landscape of Taungurung Country. Greg is a Taungurung man — this cultural connection to Country is central to the brand identity, not decorative.

## 6. SKILLS.md Per Project Directory

Each project directory on the filesystem should have a SKILLS.md file that tells agents what workflows are available.

For each project repo, create a SKILLS.md containing:
- What the project does
- How to run it (dev server, build, test commands)
- Key file locations
- Deployment process
- Common tasks and how to do them

Scan the following directories to find project repos and create SKILLS.md files:
- `D:\TalentMap\shine-talentmap-app\`
- `D:\shine-website\shine-website\`
- `D:\VS Code Projects\` (scan for all project directories)
- `D:\` (scan for top-level project directories)

## 7. Heartbeat Tuning

Update heartbeat intervals based on agent roles:
| Agent | Interval | Rationale |
|---|---|---|
| Clawdy (CEO) | 30 minutes | Strategic oversight, delegation |
| Sheldon (Engineer) | 10 minutes when active, 60 minutes when idle | Active coding needs fast cycles |
| Sherlock (QA) | 15 minutes | Reviews after engineer completes |
| Spielberg (Video) | 60 minutes | Periodic, not time-critical |
| Banksy (Design) | 60 minutes | Periodic, not time-critical |
| Content Strategist | 60 minutes | Periodic, not time-critical |
| Skippy (CEO) | 30 minutes | Personal coordination |
| Brains (Research) | 30 minutes | Research needs moderate responsiveness |

Keep the existing daily/weekly routines (morning check-in, weekly synthesis, family briefing, health review).

## 8. Automated Updates from Upstream

Greg forked the repo from paperclipai/paperclip. Set up the upstream remote and create a helper script for pulling updates.

```bash
# One-time setup (if not already done)
cd /d/paperclip
git remote add upstream https://github.com/paperclipai/paperclip.git

# Create update script at D:\paperclip\scripts\update-from-upstream.sh
```

The update script should:
1. Stash any uncommitted changes
2. Fetch upstream master
3. Merge upstream/master (abort if conflicts, tell Greg)
4. Run `pnpm install` (in case dependencies changed)
5. Restart the dev server (migrations run automatically on startup)
6. Report what changed (show release notes if a new version tag exists)

Also create a **weekly routine** for Clawdy that checks if upstream has new releases and notifies Greg via the dashboard (or Telegram once installed).

## 9. Importable Company Templates

The Paperclip community has pre-configured agent teams available for import. Check:
- What templates are available via the import feature
- Whether any are relevant to Greg's use cases (recruitment agency, content team, etc.)
- The "Agency Agents" repository (60,000+ stars, 100+ agents)

Don't import anything without Greg's approval — just report what's available.

## 10. Taste and Values Encoding

The video emphasised that AI can code, write, and plan — but cannot know what you actually want. The founder's job is encoding taste and values into agent instructions.

For Greg, this means:
- Aboriginal cultural safety and respect in all Shine communications
- Plain language (Greg is a vibe coder, not a developer)
- Australian English always
- Privacy-first for family/health data
- Proactive about reminders (Greg has poor memory)
- Taungurung cultural connection is central, not decorative

Ensure these are encoded in every agent's SOUL.md, not just Clawdy's.

## 11. Skills from skills.sh (Post-Migration — After All Config is Complete)

Once all agents are configured and the migration is stable, install community skills from skills.sh. **Security is critical** — 341 malicious skills were found in the registry in February 2026 (2.5% of all skills).

### Installation Process
1. **First**, verify our Phase 4 Security Audit Gateway plugin is active
2. **Second**, manually review the `skill-vetter` skill's source code on GitHub before installing it (it's the security scanner — we need to trust it before trusting it to scan others): https://github.com/search?q=skill-vetter+openclaw
3. Install `skill-vetter` and use it to scan every subsequent skill before activation
4. Install skills one at a time, quarantine each, review the audit report, then activate

### Tier 1: Install First (Essential)

| Skill | Install Command | Assign To | Purpose |
|---|---|---|---|
| skill-vetter | `npx skills add <owner>/skill-vetter` | System-wide | Scans skills for security risks — INSTALL THIS FIRST |
| office365-connector | `npx skills add <owner>/office365-connector` | Shine: Clawdy, Nicky | Microsoft 365 email, calendar, contacts |
| faster-whisper | `npx skills add <owner>/faster-whisper` | Shine: Sheldon, Spielberg | Local GPU transcription on 4090 — audio never leaves machine |
| supabase-ops | `npx skills add <owner>/supabase-ops` | Shine: Sheldon | Expert Supabase/PostgreSQL management for TalentMap |
| remotion-best-practices | `npx skills add <owner>/remotion-best-practices` | Shine: Spielberg | Complete Remotion video toolkit |
| firecrawl | `npx skills add <owner>/firecrawl` | Shine: Clawdy | Web scraping for recruitment sourcing |
| github | `npx skills add <owner>/github` | Shine: Sheldon, Sherlock | GitHub workflow automation |
| youtube | `npx skills add <owner>/youtube` | Life Admin: Brains | YouTube search and transcript fetching |

### Tier 2: High Value

| Skill | Install Command | Assign To | Purpose |
|---|---|---|---|
| abm-outbound | `npx skills add <owner>/abm-outbound` | Shine: Clawdy | LinkedIn recruitment outreach automation |
| adhd-assistant | `npx skills add <owner>/adhd-assistant` | Life Admin: Skippy | ADHD-friendly planning and routine support (for Kobi) |
| qa-patrol | `npx skills add <owner>/qa-patrol` | Shine: Sherlock | Automated QA testing — 39 bug patterns |
| stock-market-pro | `npx skills add <owner>/stock-market-pro` | Life Admin: Brains | Stock tracking, analysis, charts |
| tour-planner | `npx skills add <owner>/tour-planner` | Life Admin: Skippy | Travel itineraries — 150+ destinations, no API keys needed |
| pdf-ocr | `npx skills add <owner>/pdf-ocr` | Shine: Clawdy | OCR extraction from scanned resumes/documents |
| frontend-design | `npx skills add <owner>/frontend-design` | Shine: Banksy | Production-grade UI design guidance |
| self-improving-agent | `npx skills add <owner>/self-improving-agent` | All agents | Learn from mistakes, log preferences |

### Tier 3: Nice to Have (Install When Needed)

| Skill | Install Command | Assign To | Purpose |
|---|---|---|---|
| voice-ai-tts | `npx skills add <owner>/voice-ai-tts` | Shine: Spielberg | Voice cloning from audio samples |
| n8n-workflow | `npx skills add <owner>/n8n-workflow` | Shine: Clawdy | Multi-app workflow automation, 800+ apps |
| ace-music | `npx skills add <owner>/ace-music` | Life Admin: Skippy | AI music generation |
| expense-tracker-pro | `npx skills add <owner>/expense-tracker-pro` | Shine: Clawdy | Business expense tracking |
| summarize | `npx skills add <owner>/summarize` | All agents | Condense URLs, PDFs, audio, YouTube videos |
| bibigpt-skill | `npx skills add <owner>/bibigpt-skill` | Life Admin: Brains | YouTube highlights with timestamps, cross-video Q&A |
| notion | `npx skills add <owner>/notion` | Shine: Nicky | Client documentation via Notion |

### Health & Family Skills (For Life Admin — Use Local Agent When Available)

| Skill | Install Command | Assign To | Purpose |
|---|---|---|---|
| adhd-assistant | `npx skills add <owner>/adhd-assistant` | Skippy | ADHD daily planning, task breakdown, routine support |
| adhd-body-doubling | `npx skills add <owner>/adhd-body-doubling` | Skippy | Virtual co-working with micro-steps |
| health-guardian | `npx skills add <owner>/health-guardian` | Guardian (once set up) | Proactive health monitoring |

**NOTE:** For each `npx skills add` command, look up the actual owner/repo on skills.sh or GitHub before running. The `<owner>` placeholders need to be replaced with real repository paths. Search skills.sh for each skill name to find the correct install path.

**NOTE 2:** Some skills require API keys (e.g., office365-connector needs Microsoft Graph API credentials, firecrawl needs an API key). Document which keys are needed and add them to Paperclip's encrypted secrets store — NEVER store them in plain text or environment variables.

---

## What to Do First

1. Ask Greg to confirm/adjust the company missions (Section 1)
2. All agent names are confirmed — do NOT ask Greg again
3. Create all confirmed agents with their SOUL.md personalities (Section 2)
4. Set up org charts in both companies (Section 2)
5. Create BRAND.md and attach as a skill to all Shine agents (Section 5)
6. Set budgets, maxTurnsPerRun, and issue prefixes (Sections 3-4)
7. Create the upstream update script and weekly check routine (Section 8)
8. Scan project directories for SKILLS.md creation (Section 6)
9. Update heartbeat intervals (Section 7)
10. Check available company templates and report to Greg (Section 9)
11. After all above is stable, begin skills installation following Section 11 (Tier 1 first, then Tier 2, then Tier 3)
