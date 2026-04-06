# Life Admin — Organisation Structure

**Company:** Life Admin (merging Shine People Solutions)  
**Purpose:** AI-powered life operating system for Greg & Tegan Sax  
**Scope:** Shine People Solutions (winding down), personal/family life, finances, and upcoming gypsy years travel  
**Last updated:** 2026-04-06

---

## EXECUTIVE LEADERSHIP

| Role | Agent | Model | Heartbeat |
|------|-------|-------|-----------|
| CEO | Clawdy | Claude Opus (claude_local) | TBD — strategic wake-up only |
| COO | COO | TBD (from matrix) | Off |
| CTO | Gayan | Claude Opus → Codex → MiniMax | Off |

**Notes:**
- CEO and CTO confirmed as Claude Opus (free via Max plan)
- CTO fallback chain: Codex/GPT-5.3 → MiniMax-M2.7
- Clawdy is the CEO of the merged company (former Skippy, with lobster icon)

---

## TECHNOLOGY & ENGINEERING

| Role | Agent | Model | Notes |
|------|-------|-------|-------|
| Senior Engineer | Senior Engineer | DeepSeek V3 (→ Grok-Code-Fast-1 → MiniMax fallback) | Complex builds; primary engineer |
| Engineer | Engineer (Codex/GPT 5.3) | gpt-5.3-codex → MiniMax fallback | Codex-based tasks; falls back to MiniMax when Plus limits hit |
| QA Bot | QA Bot | TBD | Code review, testing |
| Designer | Designer | TBD | UI/UX design |

**Notes:**
- Most coding done in Cursor; Paperclip tech agents for architecture, specs, code review, docs
- Codex → MiniMax is the confirmed fallback when ChatGPT Plus limits are hit

---

## BUSINESS OPERATIONS (Shine + Consulting)

| Role | Agent | Model | Notes |
|------|-------|-------|-------|
| Content Lead | Content Lead | TBD | Writing, proposals, Shine comms, social |
| Accountant | Accountant | TBD | Shine finances, invoicing, bookkeeping |
| Spielberg | Spielberg | TBD | Video content planning |

**Notes:**
- Shine is winding down from active business → background income (consulting) over time
- These agents primarily handle Shine's remaining operations

---

## PERSONAL FINANCE & INVESTMENTS

| Role | Agent | Model | Notes |
|------|-------|-------|-------|
| Finance | Finance *(to create)* | TBD | Portfolio monitoring, super, budgeting, travel fund |

**Notes:**
- NEW AGENT — does not yet exist; create after LLM matrix is finalised
- Covers: share portfolio (ASX/ETFs), superannuation, travel budget planning, occasional consulting income tracking

---

## FAMILY & HEALTH ⚠️ LOCAL ONLY

| Role | Agent | Model | Hard constraint |
|------|-------|-------|-----------------|
| Health & Family | Doc | gemma4:26b (Ollama local) | **NEVER cloud — private** |
| Psychiatrist | Freud | gemma4:26b (Ollama local) | **NEVER cloud — private** |

**Notes:**
- Doc handles: NDIS planning, general health tracking, appointment scheduling, wellbeing journaling, refers patients to Freud
- Freud handles: psychological/psychiatric specialist support; receives referrals from Doc
- Both agents run LOCAL ONLY on the RTX 4090 via Ollama — health data never leaves the machine (Lana, Kobi, Greg, Tegan)
- These are the ONLY agents with a hard privacy constraint; no exceptions

---

## TRAVEL & LIFESTYLE

| Role | Agent | Model | Notes |
|------|-------|-------|-------|
| Travel Planner | Travel Agent *(to create)* | TBD | Gypsy years planning, logistics |

**Notes:**
- NEW AGENT — does not yet exist
- Gypsy years begin within 12 months
- Covers: accommodation research, visa requirements, travel routes, itinerary planning, packing, remote work logistics

---

## RESEARCH & INTELLIGENCE

| Role | Agent | Model | Notes |
|------|-------|-------|-------|
| Researcher | Researcher | TBD | Cross-department research, intelligence gathering |

---

## COUNCIL OF ELDERS (Advisory Overlay — 6 Members)

Council members are on-demand only — **no heartbeat**. Triggered for complex decisions, debates, and high-stakes choices.

| Role | Agent | Model | Perspective |
|------|-------|-------|-------------|
| Judge (synthesiser) | Yoda | Claude Opus | Final arbiter; synthesises debate into recommendation |
| Devil's Advocate | Skeptic | Grok-3 (xAI) | Challenges assumptions; unconventional view |
| Local Voice | Gemma | gemma4:26b (local) | Free, always-available local perspective |
| European/Balanced | Mistral | mistral-large-latest | Balanced, rigorous European perspective |
| Long-Context Analyst | Kimi | Kimi K2.5 | Deep analysis of long documents; careful reasoning |
| Technical | Codex | gpt-5.3-codex | Technical and code perspective |

**Notes:**
- Trimmed from 11 members to 6 for quality over quantity
- Removed: Sonnet, Haiku, DeepSeek, Grok (standalone), MiniMax council slot, Gemini council slot
- Skeptic = former Maverick (renamed); now uses Grok-3 model

---

## UNASSIGNED / TO EVALUATE AFTER MATRIX

| Agent | Current State | Decision |
|-------|--------------|----------|
| Haiku | ollama_local/gemma4:26b | Evaluate: fast utility agent OR archive |
| Sonnet | ollama_local/gemma4:26b | Evaluate: balanced voice OR archive |
| DeepSeek | ollama_local/deepseek-chat | Archive (not in council or active roster) |
| Grok | ollama_local/grok-3 | Archive (Skeptic now handles this role) |
| MiniMax | ollama_local/MiniMax-M2.7 | Repurpose as Senior Engineer config; archive this slot |
| Gemini | gemini_local/gemini-2.5-flash | Evaluate: useful for multimodal tasks OR archive |

---

## TOTAL POSITION SUMMARY

| Category | Count |
|----------|-------|
| Executive | 3 |
| Technology | 4 |
| Business Ops | 3 |
| Finance | 1 (new) |
| Family & Health | 2 |
| Travel | 1 (new) |
| Research | 1 |
| Council | 6 |
| **Active total** | **21** |
| To evaluate | 6 |

---

## NEW AGENTS TO CREATE

After LLM matrix is finalised and strategic wake-up begins:

1. **Finance** — Personal Finance & Investments department
2. **Travel Agent** — Travel & Lifestyle department

Both need:
- SOUL.md with role description and personality
- AGENTS.md / MEMORY.md
- Assigned skills (at minimum: `paperclip`, `para-memory-files`)
- Adapter configured per LLM matrix recommendation
