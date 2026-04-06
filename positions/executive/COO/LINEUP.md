# LINEUP — COO

**Agent ID:** b9acdc0e-671b-4956-9d14-ee9761ad9f06  
**Character:** COO  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | claude_local | claude-sonnet-4-6 | FREE (Max plan) | Default |
| Fallback 1 | ollama_local | mistral-large-latest | ~$2/M | claude_local down |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | Both above down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
