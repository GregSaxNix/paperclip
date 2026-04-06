# LINEUP — CTO (Gayan)

**Agent ID:** 56d606ab-a36c-4cd9-bf71-1ed422d49d4e  
**Character:** Gayan  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | claude_local | claude-opus-4-6 | FREE (Max plan) | Default |
| Fallback 1 | ollama_local | grok-code-fast-1 | ~$0.20/M | claude_local down; coding-capable |
| Fallback 2 | ollama_local | MiniMax-M2.7 | ~$0.30/M | Fallback 1 down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
