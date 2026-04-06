import type {
  AdapterEnvironmentCheck,
  AdapterEnvironmentTestContext,
  AdapterEnvironmentTestResult,
} from "../types.js";
import { asString, parseObject } from "../utils.js";

function summarizeStatus(checks: AdapterEnvironmentCheck[]): AdapterEnvironmentTestResult["status"] {
  if (checks.some((check) => check.level === "error")) return "fail";
  if (checks.some((check) => check.level === "warn")) return "warn";
  return "pass";
}

interface OllamaModel {
  id?: string;
  name?: string;
}

interface ChatResponse {
  choices?: Array<{ message?: { content?: string } }>;
}

function isCloudUrl(url: string): boolean {
  try {
    const { hostname } = new URL(url);
    return hostname !== "localhost" && !hostname.startsWith("127.") && !hostname.startsWith("192.168.");
  } catch {
    return false;
  }
}

export async function testEnvironment(
  ctx: AdapterEnvironmentTestContext,
): Promise<AdapterEnvironmentTestResult> {
  const checks: AdapterEnvironmentCheck[] = [];
  const config = parseObject(ctx.config);
  const baseUrl = asString(config.url, "http://localhost:11434");
  const model = asString(config.model, "qwen2.5:32b");
  const apiKey = asString(config.apiKey ?? (config as Record<string, unknown>).apiKey, "").trim();

  // 1. Validate base URL
  let url: URL | null = null;
  try {
    url = new URL(baseUrl);
  } catch {
    checks.push({
      code: "ollama_url_invalid",
      level: "error",
      message: `Invalid URL: ${baseUrl}`,
      hint: "Use http://localhost:11434 for local Ollama, or the cloud API base URL.",
    });
    return {
      adapterType: ctx.adapterType,
      status: summarizeStatus(checks),
      checks,
      testedAt: new Date().toISOString(),
    };
  }

  const cloud = isCloudUrl(baseUrl);

  checks.push({
    code: "ollama_url_configured",
    level: "info",
    message: `${cloud ? "Cloud API" : "Ollama"} endpoint: ${baseUrl}`,
  });

  if (cloud) {
    // --- Cloud API path: probe with a real chat completion request ---
    if (!apiKey) {
      checks.push({
        code: "cloud_api_key_missing",
        level: "error",
        message: "No API key set. Cloud providers require an API key.",
        hint: "Enter your API key in the API Key field above.",
      });
      return {
        adapterType: ctx.adapterType,
        status: summarizeStatus(checks),
        checks,
        testedAt: new Date().toISOString(),
      };
    }

    checks.push({
      code: "cloud_api_key_present",
      level: "info",
      message: "API key is set.",
    });

    const endpoint = `${baseUrl.replace(/\/+$/, "")}/v1/chat/completions`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: {
          "content-type": "application/json",
          authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: "Reply with only the word: ready" }],
          max_tokens: 10,
          stream: false,
        }),
        signal: controller.signal,
      });

      if (res.ok) {
        const data = (await res.json()) as ChatResponse;
        const reply = data.choices?.[0]?.message?.content ?? "";
        checks.push({
          code: "cloud_api_ok",
          level: "info",
          message: `Cloud API responded successfully. Model: ${model}. Reply: "${reply.slice(0, 80)}"`,
        });
      } else {
        const body = await res.text().catch(() => "");
        const hint =
          res.status === 401
            ? "API key is invalid or expired. Check it in the agent config."
            : res.status === 404
              ? "Model not found or endpoint path is wrong. Check the model name and URL."
              : res.status === 429
                ? "Rate limit hit. Try again shortly."
                : undefined;
        checks.push({
          code: "cloud_api_error",
          level: "error",
          message: `Cloud API returned HTTP ${res.status}: ${body.slice(0, 200)}`,
          ...(hint ? { hint } : {}),
        });
      }
    } catch (err) {
      const timedOut = err instanceof DOMException && err.name === "AbortError";
      checks.push({
        code: "cloud_api_unreachable",
        level: "error",
        message: timedOut
          ? `Request timed out after 15s. The endpoint may be slow or unreachable.`
          : err instanceof Error
            ? err.message
            : "Cannot reach cloud API",
        hint: timedOut ? "Check your internet connection and the API URL." : undefined,
      });
    } finally {
      clearTimeout(timeout);
    }
  } else {
    // --- Local Ollama path: check /api/tags ---
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    try {
      const res = await fetch(`${baseUrl.replace(/\/+$/, "")}/api/tags`, {
        signal: controller.signal,
      });
      if (res.ok) {
        const data = (await res.json()) as { models?: OllamaModel[] };
        const models = data.models ?? [];
        const modelNames = models.map((m) => m.name ?? m.id ?? "unknown");

        checks.push({
          code: "ollama_api_reachable",
          level: "info",
          message: `Ollama is running with ${models.length} model(s): ${modelNames.join(", ")}`,
        });

        const modelAvailable = modelNames.some(
          (n) => n === model || n.startsWith(`${model}:`) || model.startsWith(`${n.split(":")[0]}`),
        );

        if (modelAvailable) {
          checks.push({
            code: "ollama_model_available",
            level: "info",
            message: `Model "${model}" is available locally.`,
          });
        } else {
          checks.push({
            code: "ollama_model_missing",
            level: "warn",
            message: `Model "${model}" not found. Available: ${modelNames.join(", ")}`,
            hint: `Run: ollama pull ${model}`,
          });
        }
      } else {
        checks.push({
          code: "ollama_api_error",
          level: "error",
          message: `Ollama API returned HTTP ${res.status}.`,
        });
      }
    } catch (err) {
      checks.push({
        code: "ollama_api_unreachable",
        level: "error",
        message: err instanceof Error ? err.message : "Cannot reach Ollama API",
        hint: "Ensure Ollama is running: ollama serve",
      });
    } finally {
      clearTimeout(timeout);
    }
  }

  return {
    adapterType: ctx.adapterType,
    status: summarizeStatus(checks),
    checks,
    testedAt: new Date().toISOString(),
  };
}
