# LINEUP — Travel Agent

**Agent ID:** TBD — provision first  
**Character:** Travel Agent  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | claude_local | claude-sonnet-4-6 | FREE (Max plan) | Default |
| Fallback 1 | ollama_local | kimi-k2.5 | ~$0.60/M | claude_local down; web search + long docs |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | Both above down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
