# POSITION DESCRIPTION — Council Local
_Council — Local Perspective_

---

## Why this role exists
The Council of Elders needs a voice that operates independently of the internet and external APIs. Council Local provides reasoning that is guaranteed local — no latency, no cost, no outage risk, no data exfiltration.

For debates involving sensitive topics, Council Local ensures there is always a participant who has processed only what is explicitly provided.

## Key responsibilities
1. Participate in Council of Elders debates as the local, offline perspective
2. Reason independently from context provided in the prompt — no web knowledge assumed
3. Handle council debates on sensitive or private topics requiring air-gapped processing
4. Provide a baseline ground-truth voice in multi-model debates

## Hiring criteria
_Used by the LLM recruitment algorithm in `update_llm_matrix.py --hire`_

| Task dimension | Weight | Why |
|----------------|--------|-----|
| Reasoning | 60% | Pure reasoning quality — no access to external data |
| Writing | 40% | Council contributions must be coherent and well-expressed |

## Skills required

### Cognitive (handled by the LLM natively)
- Structured reasoning from first principles
- Argument construction and logical analysis
- Summarisation and synthesis from provided context only

## Constraints
- LOCAL ONLY — must always run on gemma4:26b via ollama_local
- NO external calls, NO internet access, NO MCP servers
- Only valid model: gemma4:26b

## Current employment
_Auto-updated by `update_llm_matrix.py --hire` after each research cycle_

| Slot | Adapter | Model | Cost | Appointed |
|------|---------|-------|------|-----------|
| Primary | ollama_local | gemma4:26b | FREE (local) | 2026-04-06 |
