# LINEUP — Finance

**Agent ID:** TBD — provision first  
**Character:** Finance  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | ollama_local | deepseek-reasoner (R1) | ~$0.55/M | Default — chain-of-thought for financial analysis |
| Fallback 1 | ollama_local | kimi-k2.5 | ~$0.60/M | DeepSeek unavailable; long-context analyst |
| Fallback 2 | claude_local | claude-sonnet-4-6 | FREE (Max plan) | Both above down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
