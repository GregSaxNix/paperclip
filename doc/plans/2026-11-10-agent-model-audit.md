# Agent model audit, 10 November 2026

Checked against each provider's model list (`GET /v1/models`) and a one-token chat call per model, using the keys in `D:\paperclip\.env`. No agent's model was changed. Two agents (Council Contrarian, Sentry) had their provider address and key put back, because `position_manager.py sub` had wiped them; their model is unchanged.

## What providers offer today

| Provider | Models listed |
|---|---|
| xAI | grok-4.3, grok-4.5, grok-4.6, grok-4.7, grok-4.20 (reasoning, non-reasoning, multi-agent), grok-build-0.1 |
| DeepSeek | deepseek-flash, deepseek-v4-pro |
| Moonshot | kimi-k2.6, kimi-k2.7-code, kimi-k3, kimi-k3.1-pro (+ highspeed variants) |
| MiniMax | MiniMax-M2 to M2.7, MiniMax-M3, MiniMax-M3.1-Flash |
| Mistral, Qwen | not checked: no API key in `.env` |
| Local Ollama | gemma4:26b, gemma4:12b, qwen3.8:27b, gpt-oss:20b, llama3.2 |

Old names are often still accepted and quietly served by a newer model:
- `grok-3`, `grok-3-mini` are served as **grok-4.3**; `grok-code-fast-1` as **grok-build-0.1**.
- `deepseek-chat` and `deepseek-reasoner` are both served as **deepseek-flash** (so "reasoner" agents no longer get a separate reasoning model).
- `MiniMax-Text-01` still answers as itself but is no longer listed.
- Rejected outright: `moonshot-v1-32k` (404), `kimi-k2.5` (404), `deepseek-v4` (400, "use deepseek-flash or deepseek-v4-pro").

## Live agents

| Agent | Adapter / model | Result |
|---|---|---|
| Travel Agent | ollama_local / moonshot-v1-32k | **Broken**: Moonshot no longer offers it |
| Council Contrarian | ollama_local / grok-3 | Stale name, served as grok-4.3. Address was missing, now restored |
| Council EU | ollama_local / grok-3 | Stale name, served as grok-4.3 (lineup says Mistral, which has no key) |
| Sentry | ollama_local / deepseek-reasoner | Stale name, served as deepseek-flash. Address was missing, now restored |
| Accountant, Finance, Council CH | ollama_local / deepseek-reasoner | Stale name, served as deepseek-flash |
| Senior Engineer, QA Bot | ollama_local / deepseek-chat | Stale name, served as deepseek-flash |
| Content Lead | ollama_local / MiniMax-Text-01 | Works, but no longer listed |
| Researcher | ollama_local / kimi-k2.6 | Offered (handled in the Model Lineup Monitor thread) |
| Clawdy, Gayan, COO, Yoda | claude_local / claude-opus-4-6 | Works (Clawdy ran successfully at 12:53 pm today) |
| Spielberg, Designer, Gemini | gemini_local / gemini-2.5-flash | Not checked: no Gemini key on this PC |
| Engineer, Council Tech | codex_local / gpt-5.3-codex | Not checked |
| Council Local | ollama_local / gemma4:12b | Installed |
| Doc, Freud | ollama_local / gemma4:26b | Installed |

## Lineup files (`positions/*/LINEUP.md`) that would break an agent if used

`restore` and `sync` copy the Primary row of these files onto the agent, so stale rows matter:
- Senior Engineer and QA Bot Primary is `deepseek-v4` (rejected).
- Researcher Primary is `grok-4.1`; Researcher, Finance, Travel Agent and Council CH list `kimi-k2.5` (rejected).
- Council EU Primary is `mistral-large-latest`; Researcher lists `qwen-plus`: no keys, so the fixed script refuses these instead of breaking the agent.
- Many live agents differ from their lineup Primary (for example COO, Designer, Content Lead, Accountant, Travel Agent). Do not run `restore all` or `sync all` until the lineups are brought up to date.

Choosing replacement models is Greg's decision.
