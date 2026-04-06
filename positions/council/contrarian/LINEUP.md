# LINEUP — Council Contrarian

**Agent ID:** e8ce7488-0d6d-42c8-a63f-88e46d8a0a7c  
**Character:** Council Contrarian  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | ollama_local | grok-3 | ~$3/M | Default — bold, web-aware, contrarian |
| Fallback 1 | ollama_local | grok-3-mini | ~$0.30/M | Grok-3 unavailable |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All Grok unavailable (use contrarian system prompt) |

**Note on Gemma as emergency contrarian:** gemma4:26b can be run in a contrarian mode via system prompt: "Take the opposing view on every proposal. Surface risks. Challenge every assumption. Be the devil's advocate." Less sophisticated than Grok-3 but functional.
