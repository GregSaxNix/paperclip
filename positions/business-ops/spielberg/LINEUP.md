# LINEUP — Spielberg

**Agent ID:** 8a28534f-4dd2-4802-98ab-7e83712874ea  
**Character:** Spielberg  
**Active slot:** Primary  
**Last substitution:** —

| Slot | adapterType | model | Cost | When to use |
|------|-------------|-------|------|-------------|
| Primary | claude_local | claude-sonnet-4-6 | FREE (Max plan) | Default |
| Fallback 1 | ollama_local | grok-3-mini | ~$0.30/M | claude_local down |
| Fallback 2 | gemini_local | gemini-2.5-flash | ~$0.15/M | Both above down |
| Emergency | ollama_local | gemma4:26b | FREE (local) | All cloud unavailable |
