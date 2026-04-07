# LINEUP — CyberSecurity

**Agent ID:** _(pending — run `python scripts/position_manager.py provision CyberSecurity`)_
**Character:** Sentry
**Active slot:** Primary
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | ollama_local | deepseek-reasoner | ~$0.55/M | Default — top reasoning (score 10), ideal for threat modelling |
| Fallback 1 | ollama_local | grok-3 | ~$3/M | Algorithm pick — highest reasoning+coding combo outside Reasoner |
| Fallback 2 | ollama_local | deepseek-chat | ~$0.27/M | Cost-efficient fallback, solid reasoning+coding |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |

**Model selection rationale:**
DeepSeek R1 leads on threat modelling and vulnerability analysis — tasks that require sustained multi-step reasoning (score 10). Grok-3 as Fallback 1 brings top-tier reasoning and strong coding at higher cost. DeepSeek V4 (Chat) as cost-efficient Fallback 2. Algorithm score: 8.60 / 8.40 / 8.00.
