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

export async function testEnvironment(
  ctx: AdapterEnvironmentTestContext,
): Promise<AdapterEnvironmentTestResult> {
  const checks: AdapterEnvironmentCheck[] = [];
  const config = parseObject(ctx.config);
  const baseUrl = asString(config.url, "http://localhost:11434");
  const model = asString(config.model, "qwen2.5:32b");

  // 1. Validate base URL
  let url: URL | null = null;
  try {
    url = new URL(baseUrl);
  } catch {
    checks.push({
      code: "ollama_url_invalid",
      level: "error",
      message: `Invalid Ollama URL: ${baseUrl}`,
      hint: "Use an http://host:port format (default: http://localhost:11434).",
    });
    return {
      adapterType: ctx.adapterType,
      status: summarizeStatus(checks),
      checks,
      testedAt: new Date().toISOString(),
    };
  }

  checks.push({
    code: "ollama_url_configured",
    level: "info",
    message: `Ollama endpoint: ${baseUrl}`,
  });

  // 2. Probe Ollama API
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

      // 3. Check if the configured model is available
      const modelAvailable = modelNames.some(
        (n) => n === model || n.startsWith(`${model}:`) || model.startsWith(`${n.split(":")[0]}`)
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

  return {
    adapterType: ctx.adapterType,
    status: summarizeStatus(checks),
    checks,
    testedAt: new Date().toISOString(),
  };
}
