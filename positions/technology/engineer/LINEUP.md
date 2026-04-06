# LINEUP — Engineer

**Agent ID:** 787afb8c-df1d-4632-8ee3-40da4d06f17b  
**Character:** Engineer  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | codex_local | gpt-5.3-codex | Weekly quota (finite) | When Codex quota available |
| Fallback 1 | ollama_local | grok-code-fast-1 | ~$0.20/M | ⚠️ ACTIVE NOW — Codex quota exhausted |
| Fallback 2 | ollama_local | MiniMax-M2.7 | ~$0.30/M | Fallback 1 down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |

**⚠️ Note:** Codex weekly quota was exhausted 2026-04-06. Engineer is currently on Fallback 1 (Grok-Code-Fast-1) until quota resets. Run `python position_manager.py check-quota` to check status.
