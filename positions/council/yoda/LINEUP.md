# LINEUP — Yoda (Council Judge)

**Agent ID:** 19c2937c-8e11-4f18-a166-9cdec6ab07e5  
**Character:** Yoda  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | claude_local | claude-opus-4-6 | FREE (Max plan) | Default — best reasoning for judgement |
| Fallback 1 | ollama_local | grok-3 | ~$3/M | claude_local down; strong reasoning |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | Both above down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
