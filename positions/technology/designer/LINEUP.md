# LINEUP — Designer

**Agent ID:** 5f031fe8-6bd7-4a33-a8eb-705f5f3e6c69  
**Character:** Designer  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | claude_local | claude-sonnet-4-6 | FREE (Max plan) | Default |
| Fallback 1 | gemini_local | gemini-2.5-flash | ~$0.15/M | claude_local down; strong multimodal |
| Fallback 2 | ollama_local | MiniMax-M2.7 | ~$0.30/M | Fallback 1 down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
