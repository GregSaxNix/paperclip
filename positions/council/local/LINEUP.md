# LINEUP — Council Local

**Agent ID:** 579e8c85-f6f2-4ddb-af55-e970312756a3  
**Character:** Council Local  
**Active slot:** Primary (LOCAL ONLY)  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | ollama_local | gemma4:12b | FREE (local) | Default — and only option |

**Note:** Council Local runs on gemma4:12b local (switched from gemma4:26b on 2026-06-07). Gemma 4 12B nearly matches the 26B's quality at less than half the VRAM (7.6 GB vs 17 GB), so it stays the always-available, always-free, always-private council voice while freeing GPU headroom for other local agents to run at the same time. The two health agents (Doc, Freud) keep gemma4:26b. No fallback chain needed; the model IS the identity for this position.
