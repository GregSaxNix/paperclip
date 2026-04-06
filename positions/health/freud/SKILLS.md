# SKILLS — Freud

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `cbt-act-framework` — CBT thought records, ACT values clarification, defusion exercises, committed action
- [ ] `adhd-support-toolkit` — ADHD executive function strategies — time blindness, task initiation, hyperfocus (Kobi)
- [ ] `autism-communication-guide` — ASD communication, PDA profile, demand avoidance, sensory processing (Lana)
- [ ] `mood-journal-facilitator` — Structured mood tracking, pattern recognition, PHQ-9/GAD-7 style check-ins
- [ ] `psychotropic-education` — Medication education — SSRIs, stimulants, mood stabilisers, what to watch for
- [ ] `therapeutic-modalities-guide` — DBT, EMDR, somatic therapy, play therapy — for referral recommendations
- [ ] `deidentification-protocol` — Strip PII from psychological data before cloud queries — re-identify locally

## Notes

**LOCAL ONLY** — All data stays on the local machine. NO external MCP servers. Must maintain non-judgmental, trauma-informed tone at all times. NEVER diagnose; always encourage professional consultation for clinical decisions. The de-identification protocol enables cloud queries when frontier-model quality is needed.
