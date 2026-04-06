# SKILLS — Doc

Assign system skills via `POST /api/agents/:id/skills/sync` (run `python scripts/position_manager.py sync {key}`).

## System Skills (installed)
_Synced to the agent by `position_manager.py`. These are active now._

- paperclip — Core platform control
- para-memory-files — PARA-method memory — maintains complete family health history

## Document Skills (install from anthropics/skills)
_Official Anthropic vetted skills. Install via Paperclip Plugin Manager or API._

- [ ] `pdf` — Referral letters, pathology reports, specialist letters, test results

## Custom Build Skills (pending)
_These skills do not exist publicly in the right form. Build progressively as needed._

- [ ] `health-biometrics-tracker` — Parse Apple Health exports, Garmin data, ResMed CPAP data — interpret trends
- [ ] `blood-test-analyzer` — Interpret blood panels (CBC, lipids, hormones, vitamins), flag concerning trends
- [ ] `dna-health-analysis` — Read 23andMe/Ancestry raw data — interpret health-relevant SNPs, risk summary
- [ ] `medication-tracker` — Medication schedules, dosing, interaction checking, compliance tracking
- [ ] `ndis-navigator` — NDIS plan structure, funding categories, goal writing, review preparation (Australia)
- [ ] `deidentification-protocol` — Strip PII from health data before cloud queries — re-identify locally after

## Notes

**LOCAL ONLY** — All data stays on the local machine. NO external MCP servers. The de-identification protocol (`deidentification-protocol` skill) enables cloud queries by stripping names/dates/diagnoses before sending, then re-identifying locally.
