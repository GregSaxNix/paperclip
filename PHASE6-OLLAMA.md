# Phase 6: Ollama/4090 Private Agent for Life Admin

Paste everything below this line into the Paperclip Cursor session.

---

## Context

Phases 0-5 are complete. Two companies (Shine Operations + Life Admin) are running with agents Clawdy and Skippy. Now we need a local private agent for sensitive health/family data that must never leave the machine.

## What This Phase Does

Set up Ollama running on Greg's NVIDIA 4090 GPU, create an HTTP webhook adapter in Paperclip pointing at it, and create a private agent in the Life Admin company for health-sensitive tasks.

## Requirements

1. **All health/medical data stays local** — never sent to cloud APIs. This agent processes sensitive data about Greg's children (Lana: developmental delays/autism, Kobi: ADHD).
2. **Zero cost** — Ollama is free, runs locally on the 4090.
3. **Integrated into Paperclip** — the agent appears in Life Admin alongside Skippy, tasks can be assigned to it, results appear in issue threads like any other agent.

## Steps

### 1. Install Ollama
- Check if Ollama is already installed: `where ollama` or `ollama --version`
- If not, install it: `winget install Ollama.Ollama` or download from https://ollama.com
- Verify it starts and the API is accessible at `http://localhost:11434`

### 2. Pull a Suitable Model
- For a 4090 (24GB VRAM), good options:
  - `ollama pull llama3.1:70b-instruct-q4_K_M` (if VRAM allows — test first)
  - `ollama pull llama3.1:8b-instruct` (safe choice, fast, fits easily)
  - `ollama pull deepseek-coder-v2:16b` (good for coding tasks)
  - `ollama pull mistral:7b-instruct` (general purpose, very fast)
- Start with `llama3.1:8b-instruct` for testing, upgrade later if needed
- Verify with: `ollama run llama3.1:8b-instruct "Hello, are you working?"`

### 3. Create HTTP Webhook Adapter in Paperclip
- Configure an adapter that sends requests to Ollama's OpenAI-compatible API:
  - Endpoint: `http://localhost:11434/v1/chat/completions`
  - Model: whatever was pulled in step 2
  - No API key needed (local)
- Check Paperclip's adapter documentation for how HTTP/webhook adapters are configured

### 4. Create the Private Agent in Life Admin
- **Name:** Something like "Guardian" or "Vault" — suggests privacy/protection. Ask Greg what he prefers.
- **Company:** Life Admin
- **Adapter:** The Ollama HTTP adapter from step 3
- **SOUL.md personality:**
  - Empathetic and careful with sensitive information
  - Specialises in health management, therapy tracking, medical research summaries
  - Never suggests sharing health data externally
  - Australian English
  - Understands neurodivergence (autism, ADHD) — factual, non-judgemental, evidence-based
  - Proactive about flagging health appointment reminders and therapy milestones
- **Memory:** Separate MEMORY.md for health-related context (therapy progress, medication, appointments)

### 5. Test It
- Create a test issue in Life Admin's Health Management project
- Assign it to the new private agent
- Verify the response comes from Ollama (check logs — should show localhost:11434 requests, NOT Anthropic API)
- Verify no data left the machine

### 6. Configure Routing Guidance
- Add a note/skill to Life Admin that guides task assignment:
  - Health Management project tasks → Private agent (local, never cloud)
  - All other Life Admin tasks → Skippy (Claude via Max plan)
- This is guidance for Greg, not automatic routing (Greg picks the agent when creating issues)

## Important Notes

- The 4090 has 24GB VRAM — more than enough for 8B-13B parameter models, possibly 70B quantised
- Ollama runs as a background service — it doesn't interfere with Paperclip
- Greg accesses everything through the same Paperclip dashboard — no separate UI needed
- If Ollama isn't working or the model is too slow, fall back to Skippy (Claude) for non-health tasks and flag health tasks as "pending local agent"

## What to Do First

Check if Ollama is installed, install it if not, pull a model, test it works, then configure the Paperclip adapter and agent. Ask Greg for the agent name preference before creating it.
