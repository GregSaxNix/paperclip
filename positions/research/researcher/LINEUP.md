# LINEUP — Researcher

**Agent ID:** 9d589490-af2a-4717-b7a8-b61c60059765  
**Character:** Researcher  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | ollama_local | grok-4.1 | ~$0.20/M | Default — web+X search, 131K context |
| Fallback 1 | ollama_local | kimi-k2.5 | ~$0.60/M | Grok unavailable; web search, long-context |
| Fallback 2 | ollama_local | qwen-plus | ~$0.26/M | Both above down; 1M context |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
