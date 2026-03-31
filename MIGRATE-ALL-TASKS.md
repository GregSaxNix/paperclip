# Migrate All Mission Control Tasks to Paperclip Issues

Paste everything below this line into the Paperclip Cursor session.

---

## Context

Greg's original task notes from Mission Control were not carried across during the migration. The descriptions below are extracted directly from the Mission Control database — every word is Greg's original thinking. Create each one as a proper Paperclip issue in the correct company and project, preserving the FULL description. Do NOT summarise or shorten the descriptions.

**IMPORTANT:** Copy the descriptions EXACTLY as written below. Greg put significant thought into these and was disappointed they were lost. Every detail matters.

---

## SHINE OPERATIONS — Issues to Create

### 1. YouTube Second Brain — Video Knowledge Base
**Project:** YouTube Second Brain
**Priority:** Medium
**Assign to:** Brains

**Description (copy exactly):**
Build a searchable second brain from YouTube watch history. 27,026 videos already exported from Google Takeout (Nov 2011 - Feb 2026). Parse transcripts, cluster by theme (AI news, investing, travel, agents, retirement, etc.), enable semantic search. Goal: "I saw something about X" → find the exact video and key points.

Partially built: CSV exists with 10,350+ regular videos parsed. Need: yt-dlp enrichment, topic clustering, transcript extraction, search UI.

**NOTE:** This is a Life Admin project (YouTube Second Brain), but the CSV and Google Takeout data need locating on Greg's machine. Check D:\ and D:\VS Code Projects\ for existing work.

---

### 2. Clawdy Ventures — Autonomous Income Generation
**Project:** Business Admin
**Priority:** Medium
**Assign to:** Clawdy

**Description (copy exactly):**
Build autonomous income-generating system inspired by Nat Eliason's Felix bot ($14,718 in 3 weeks from $1,000 seed). Multiple revenue streams routed through Shine People Solutions ABN.

Target: Australian small businesses. Focus: AI for small business survival.

Tier 1 (Quick wins): Info products ($500-2k/month), digital downloads ($300-1k/month), newsletter/Substack ($200-1k/month), X/Twitter content ($100-500/month).

Tier 2 (Medium-term): Micro-SaaS tools, affiliate marketing, consulting automation.

First product: "AI Survival Guide for Australian Small Business" with lead magnet "AI Readiness Scorecard".

---

### 3. Industry Vertical Content Hubs (Paywalled)
**Project:** Business Admin
**Priority:** Low
**Assign to:** Nicky

**Description (copy exactly):**
Paywalled websites with industry-specific AI resources. Living resources (updated regularly) with login portal.

Identified verticals:
1. Legal — Sole Practitioners (target: Slissa, friend) — $195
2. Geology & Prospecting (target: friend, former geologist) — $195
3. Electrical Engineering — Infrastructure (target: ConsultJR) — $195
4. Infrastructure Transaction Advisory (target: Sheldon Sherman, Etheus) — $495

Quality control: Clawdy generates → Claude Opus vets → Greg reviews → publish.

---

### 4. AI Shock Use Cases — Content Library
**Project:** Business Admin
**Priority:** Low
**Assign to:** Nicky

**Description (copy exactly):**
10 AI capabilities that shock business owners, with ROI frameworks. Content ready for publication.

1. Real-time voice translation
2. AI screen-watching worker
3. Voice cloning for calls
4. AI email management
5. Text-to-video generation
6. AI supplier negotiation
7. Churn prediction
8. Code from screenshots
9. Competitor monitoring
10. AI bookkeeping

ROI pitch: "$20k in AI tools can replace $240k in wages OR generate $240k-400k in value"

---

### 5. TalentMap Integration
**Project:** TalentMap
**Priority:** Medium
**Assign to:** Sheldon

**Description (copy exactly):**
Connect the Indigenous Talent Map project to Paperclip as a skill/tool. Agent can search and update the talent database.

Pipeline: employment/education parsing, normalised dates, experience months, OSCA occupation codes, ASCED education, layered OSCA+ANZSIC taxonomy. Upload cleansed data to Dynamics 365.

Existing project location: D:\TalentMap\shine-talentmap-app\
D365 credentials already configured in that project's .env files.

---

### 6. Set Up xAI API
**Project:** Clawdy Operations
**Priority:** High
**Assign to:** Clawdy
**Status:** Blocked — needs Greg to create account

**Description (copy exactly):**
Add Grok/xAI as research source with built-in X search. Requires Greg to create account at console.x.ai and get API key.

**Blocker:** Greg needs to register at console.x.ai and provide the API key via the Paperclip web UI (NEVER paste in chat).

---

### 7. Set Up X API v2
**Project:** Clawdy Operations
**Priority:** Medium
**Assign to:** Clawdy
**Status:** Blocked — needs Greg to apply

**Description (copy exactly):**
Direct X API access for programmatic searches. Requires Greg to apply at developer.x.com.

**Blocker:** Greg needs to apply for developer access at developer.x.com.

---

### 8. Crypto Trade Tracking + Xero Integration
**Project:** Business Admin
**Priority:** Low
**Assign to:** Sheldon

**Description (copy exactly):**
Custom ATO-compliant crypto trade tracking system for Shine's accounting.

Features: Auto-import from exchanges (Coinbase, Binance, Kraken, Independent Reserve, BTC Markets, Swyftx), real-time AUD conversion, profit/loss calculations, Xero export, ATO-compliant reporting.

Phases: Phase 1 MVP (Telegram-based entry) → Phase 2 (exchange API automation) → Phase 3 (Xero integration) → Phase 4 (web dashboard + autonomous mode).

Build vs buy analysis: Custom solution (20-40 hours) breaks even vs commercial tools in 6-12 months.

---

### 9. Discord Server Setup (Primary Channel)
**Project:** Clawdy Operations
**Priority:** High
**Assign to:** Clawdy

**Description (copy exactly):**
Set up private Discord server as primary messaging channel. Per-topic channels, family access, thread support.

Server structure: GENERAL (#dashboard-feed, #quick-tasks, #council-memos), PROJECTS (#shine-website, #talentmap, #mission-control), PERSONAL (#health, #home, #ideas), FAMILY (#tegan, #kobi, #lana), ADMIN (#agent-logs, #cost-alerts).

Permissions: Greg=admin (all channels), Tegan=GENERAL+PERSONAL+FAMILY+selected PROJECTS, Kobi/Lana=own FAMILY channel only.

**NOTE:** Discord channels span both companies (business + personal). The server structure includes both Shine and Life Admin topics. Consider whether this should be a cross-company infrastructure task.

---

### 10. Change Plan Ledger — Automatic Rollback System
**Project:** Clawdy Operations
**Priority:** Medium
**Assign to:** Sheldon

**Description (copy exactly):**
Automatic change tracking and rollback guardrails for high-impact changes. Full spec exists from OpenClaw incident (2026-02-25 Google 400 error loop that required 2 hours recovery).

Features: Append-only ledger, rollback points before changes, health checks post-change, automatic rollback on failure, loop detection.

User commands: /change_plan status, history, rollback, freeze/unfreeze.

**NOTE:** Check if a spec file exists at D:\mission-control\projects\change-plan-ledger\SPEC.md — if so, reference it.

---

### 11. Shine Website
**Project:** Shine Website
**Priority:** Medium
**Assign to:** Sheldon

**Description:**
Existing Shine People Solutions website project at D:\shine-website\shine-website\. Next.js + Tailwind + Framer Motion. Needs ongoing development and maintenance.

---

## LIFE ADMIN — Issues to Create

### 12. YouTube Second Brain — Video Knowledge Base
**Project:** YouTube Second Brain
**Priority:** Medium
**Assign to:** Brains

**Description (copy exactly):**
Build a searchable second brain from YouTube watch history. 27,026 videos already exported from Google Takeout (Nov 2011 - Feb 2026). Parse transcripts, cluster by theme (AI news, investing, travel, agents, retirement, etc.), enable semantic search. Goal: "I saw something about X" → find the exact video and key points.

Partially built: CSV exists with 10,350+ regular videos parsed. Need: yt-dlp enrichment, topic clustering, transcript extraction, search UI.

Sub-tasks:
1. Locate the existing CSV and Google Takeout export on Greg's machine (check D:\, D:\VS Code Projects\)
2. Set up yt-dlp for transcript extraction
3. Build topic clustering (AI news, investing, travel, agents, retirement, health, etc.)
4. Extract transcripts for all 27,026 videos
5. Build semantic search (RAG or full-text search)
6. Build a search UI accessible from Paperclip or standalone

**NOTE:** The youtube and youtube-transcript skills are already installed and assigned to Brains. The faster-whisper skill could help with videos that lack transcripts (download audio → local transcription on 4090).

---

### 13. 24/7 Autonomous Work System
**Project:** Family Scheduling
**Priority:** Medium
**Assign to:** Skippy

**Description (copy exactly):**
Full autonomous daily operations without prompting. Builds on heartbeat system.

Schedule:
- Daily 6 AM: Briefing, propose tasks, check overnight progress
- Daily 2 PM: Review incomplete tasks, propose next actions
- Daily 9 PM: Check for updates, post changelog to Discord
- Daily 11:59 PM: Close daily notes, tag for review
- Weekly Friday 5 PM: Consolidate 7 days → MEMORY.md
- Monthly: Compact MEMORY.md if >2000 words
- Quarterly: Deep review, archive completed projects

**NOTE:** Some of this is already implemented via Paperclip routines (daily briefings, weekly reviews). Map the remaining schedule items to new routines. The Discord changelog requires the Discord server to be set up first (see Shine issue #9).

---

### 14. Travel Planner — Club Wyndham Booking Manager
**Project:** TravelPlanner
**Priority:** Low
**Assign to:** Brains

**Description (copy exactly):**
Booking manager and accommodation checker for Club Wyndham South Pacific credits (662k credits, Mar/May/Oct memberships, 100 Club level).

Supporting semi-nomadic lifestyle starting 2027: Kirra → US (up to 6 months) → Canada (up to 3 months) → return late Nov/Dec.

**NOTE:** The tour-planner skill is already installed. This issue is specifically about Club Wyndham credit management and availability checking, not general travel planning.

---

### 15. ClawdyVoice — Push-to-Talk Voice Input
**Project:** Personal Finances (or create a "Tools & Utilities" project if more appropriate)
**Priority:** Medium
**Assign to:** Sheldon

**Description (copy exactly):**
Real-time speech-to-text for dictating to agents. Push-to-talk via hotkey (Ctrl+Shift+V), OpenAI Whisper transcription, auto-detection of silence, direct text insertion.

Two options: Python script (more features) or web-based HTML (zero-install, works immediately). Recommended: web-based with Web Speech API + Whisper fallback.

Greg wants this as primary input method long-term.

Prior Work: Greg has a working WhisperTranscribe project at D:\WhisperTranscribe — a Flask web UI + worker scripts for local Whisper transcription. Includes Flask server (web_app.py), chunk worker (chunk_worker.py), standalone CLI transcription (transcribe_app.py), auto-start scripts. Uses Python 3.10+ and ffmpeg. This existing work may be useful as a foundation or reference.

**NOTE:** Greg is currently using Windows Win+H for voice input which partially solves this. The faster-whisper skill is installed. Claude Code CLI also has /voice command in the terminal. This issue is about a more integrated push-to-talk solution — assess whether the existing options are sufficient or if a custom build is still needed.

---

### 16. Tech-Stocks Research
**Project:** Tech-Stocks
**Priority:** Low
**Assign to:** Brains

**Description:**
Ongoing stock market research and tracking for personal investment decisions. The stock-market-pro skill is already installed and assigned to Brains.

Create this as a standing issue for Brains to provide regular market analysis when Greg requests it.

---

### 17. Music Generator
**Project:** Music Generator
**Priority:** Low
**Assign to:** Skippy

**Description:**
Personal music generation project. The ace-music skill is available for installation (Tier 3). Check D:\ and D:\VS Code Projects\ for existing project files.

---

### 18. Textbook Scrape
**Project:** Textbook Scrape
**Priority:** Low
**Assign to:** Brains

**Description:**
Document and textbook scraping/analysis project. The pdf-ocr and firecrawl skills are already installed. Check D:\ and D:\VS Code Projects\ for existing project files (may be listed as "Jobin_Scraper" based on SKILLS.md scan).

---

## VERIFICATION

After creating all issues, confirm:
1. Every issue has the FULL description (not summarised)
2. Issues are in the correct company and project
3. Assigned to the correct agent
4. Priority and status (blocked where noted) are set correctly
5. Report back to Greg with a summary of all issues created and their locations

**Navigation for Greg to verify:**
- **Shine Operations:** Click company name (top-left) → **Issues** in left sidebar → verify all Shine issues appear
- **Life Admin:** Switch to Life Admin (top-left company switcher) → **Issues** → verify all Life Admin issues appear
