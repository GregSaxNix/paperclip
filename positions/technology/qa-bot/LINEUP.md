# LINEUP — QA Bot

**Agent ID:** 6ba034eb-b618-4aef-9de8-afc8336853be  
**Character:** QA Bot  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | ollama_local | deepseek-v4 | ~$0.30/M | Default — strong code review |
| Fallback 1 | ollama_local | codestral | ~$0.30/M | DeepSeek unavailable; code specialist |
| Fallback 2 | claude_local | claude-haiku-4-5 | FREE (Max plan) | Both above down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
