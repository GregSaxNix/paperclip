import type { ServerAdapterModule } from "../types.js";
import { execute } from "./execute.js";
import { testEnvironment } from "./test.js";

export const ollamaLocalAdapter: ServerAdapterModule = {
  type: "ollama_local",
  execute,
  testEnvironment,
  models: [
    { id: "gemma4:12b", label: "Gemma 4 12B (daily local)" },
    { id: "gemma4:26b", label: "Gemma 4 26B (Doc/Freud)" },
    { id: "qwen3.8:27b", label: "Qwen 3.8 27B (coding)" },
    { id: "gpt-oss:20b", label: "gpt-oss 20B (reasoning)" },
    { id: "llama3.2:latest", label: "Llama 3.2 3B" },
  ],
  agentConfigurationDoc: `# ollama_local agent configuration

Adapter: ollama_local

Runs models via Ollama locally or any OpenAI-compatible chat completions endpoint. When apiKey is set, adds Bearer auth for cloud API providers (DeepSeek, xAI/Grok, Mistral, etc.).

Core fields:
- url (string, optional): Ollama base URL. Default: http://localhost:11434
- model (string, required): Model name to use (e.g. gemma4:12b)
- timeoutMs (number, optional): Request timeout in milliseconds. Default: 120000
- apiKey (string, optional): Bearer token for cloud API auth. When set, adds Authorization header. Enables use with OpenAI-compatible cloud APIs (DeepSeek, xAI, Mistral, etc.)
- inputTokenPriceUsd (number, optional): Cost per input token in USD (e.g. 0.000003 for $3/M tokens). Default: 0. Set for API-backed models to enable cost tracking.
- outputTokenPriceUsd (number, optional): Cost per output token in USD (e.g. 0.000015 for $15/M tokens). Default: 0. Set for API-backed models to enable cost tracking.
`,
};
