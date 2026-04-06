# LINEUP — CEO (Clawdy)

**Agent ID:** 297d6a61-9900-4e31-9e7e-8ec3fa93c7a3  
**Character:** Clawdy  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | claude_local | claude-opus-4-6 | FREE (Max plan) | Default |
| Fallback 1 | ollama_local | grok-3 | ~$3/M | claude_local down or Anthropic outage |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | Both Primary and Fallback 1 down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |

**Note:** Fallback 1 is intentionally a non-Anthropic provider — if claude_local is down, Sonnet would also be unavailable. Grok-3 provides comparable strategic reasoning from a completely separate infrastructure.

**If Anthropic Max plan is ever revoked:** Insert `http` adapter → `api.anthropic.com` (Opus billed per token) between Primary and Fallback 1. Deferred until needed.
