import type { ServerAdapterModule } from "../types.js";
import { execute } from "./execute.js";
import { testEnvironment } from "./test.js";

export const ollamaLocalAdapter: ServerAdapterModule = {
  type: "ollama_local",
  execute,
  testEnvironment,
  models: [
    { id: "qwen2.5:32b", label: "Qwen 2.5 32B (recommended)" },
    { id: "llama3.1:8b", label: "Llama 3.1 8B" },
    { id: "llama3.2:latest", label: "Llama 3.2 3B" },
    { id: "mistral:7b-instruct", label: "Mistral 7B Instruct" },
    { id: "deepseek-coder:6.7b", label: "DeepSeek Coder 6.7B" },
  ],
  agentConfigurationDoc: `# ollama_local agent configuration

Adapter: ollama_local

Runs models locally via Ollama on the host machine. All data stays local — nothing is sent to external APIs. Uses Ollama's OpenAI-compatible chat completions endpoint.

Core fields:
- url (string, optional): Ollama base URL. Default: http://localhost:11434
- model (string, required): Model name to use (e.g. llama3.1:8b-instruct)
- timeoutMs (number, optional): Request timeout in milliseconds. Default: 120000
`,
};
