# LINEUP — Accountant

**Agent ID:** e51a0fc4-367f-4e2c-9ad5-702a0cba546b  
**Character:** Accountant  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | claude_local | claude-haiku-4-5 | FREE (Max plan) | Default — structured tasks, very fast |
| Fallback 1 | ollama_local | deepseek-chat | ~$0.26/M | claude_local down |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | Both above down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
