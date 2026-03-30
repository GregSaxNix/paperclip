import type { AdapterExecutionContext, AdapterExecutionResult } from "../types.js";
import { asString, asNumber, renderTemplate } from "../utils.js";
import { readFile } from "node:fs/promises";

interface OllamaChatMessage {
  role: string;
  content: string;
}

interface OllamaChatResponse {
  id?: string;
  choices: Array<{
    message: OllamaChatMessage;
    finish_reason: string;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
  model?: string;
}

export async function execute(ctx: AdapterExecutionContext): Promise<AdapterExecutionResult> {
  const { runId, agent, config, context, onLog } = ctx;

  const baseUrl = asString(config.url, "http://localhost:11434");
  const model = asString(config.model, "qwen2.5:32b");
  const timeoutMs = asNumber(config.timeoutMs, 120_000);
  const instructionsFilePath = asString(config.instructionsFilePath, "").trim();

  const endpoint = `${baseUrl.replace(/\/+$/, "")}/v1/chat/completions`;

  // Build system prompt from instructions file (SOUL.md) if available
  let systemPrompt = "";
  if (instructionsFilePath) {
    try {
      systemPrompt = await readFile(instructionsFilePath, "utf-8");
    } catch {
      await onLog("stderr", `[ollama] Could not read instructions file: ${instructionsFilePath}\n`);
    }
  }

  // Render prompt template with Paperclip template variables
  const promptTemplate = asString(
    config.promptTemplate,
    "You are agent {{agent.name}}. Check your assigned tasks in Paperclip and complete them.",
  );
  const templateData = {
    agent: {
      id: agent.id,
      name: agent.name,
      companyId: agent.companyId,
    },
    run: { id: runId, source: "on_demand" },
    context,
  };
  const renderedPrompt = renderTemplate(promptTemplate, templateData);

  // Build wake reason into the prompt
  const wakeReason =
    typeof context.wakeReason === "string" && context.wakeReason.trim().length > 0
      ? context.wakeReason.trim()
      : null;

  // Compose the user message from the rendered prompt + wake reason
  const userMessageParts: string[] = [];
  if (renderedPrompt) userMessageParts.push(renderedPrompt);
  if (wakeReason && wakeReason !== renderedPrompt) {
    userMessageParts.push(`\nWake reason: ${wakeReason}`);
  }

  const userMessage = userMessageParts.join("\n").trim();

  if (!userMessage && !systemPrompt) {
    return {
      exitCode: 1,
      signal: null,
      timedOut: false,
      errorMessage: "No prompt or instructions available for Ollama agent.",
    };
  }

  // Build the messages array
  const messages: OllamaChatMessage[] = [];
  if (systemPrompt) {
    messages.push({ role: "system", content: systemPrompt });
  }
  messages.push({ role: "user", content: userMessage || "Continue your work." });

  const controller = new AbortController();
  const timer = timeoutMs > 0 ? setTimeout(() => controller.abort(), timeoutMs) : null;

  try {
    await onLog("stdout", `[ollama] Sending request to ${endpoint} (model: ${model})\n`);

    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        model,
        messages,
        stream: false,
      }),
      ...(timer ? { signal: controller.signal } : {}),
    });

    if (!res.ok) {
      const body = await res.text().catch(() => "");
      const errorMessage = `Ollama returned HTTP ${res.status}: ${body}`.slice(0, 500);
      await onLog("stderr", `[ollama] ${errorMessage}\n`);
      return {
        exitCode: 1,
        signal: null,
        timedOut: false,
        errorMessage,
      };
    }

    const data = (await res.json()) as OllamaChatResponse;

    const assistantContent = data.choices?.[0]?.message?.content ?? "";
    if (assistantContent) {
      await onLog("stdout", assistantContent);
    }

    const usage = data.usage;

    return {
      exitCode: 0,
      signal: null,
      timedOut: false,
      provider: "ollama",
      model: data.model ?? model,
      summary: assistantContent.slice(0, 200),
      resultJson: assistantContent ? { issueComment: assistantContent } : undefined,
      usage: usage
        ? {
            inputTokens: usage.prompt_tokens,
            outputTokens: usage.completion_tokens,
          }
        : undefined,
      costUsd: 0, // Local model — zero cost
    };
  } catch (err) {
    const timedOut = err instanceof DOMException && err.name === "AbortError";
    const errorMessage = timedOut
      ? `Ollama request timed out after ${timeoutMs}ms`
      : err instanceof Error
        ? err.message
        : "Unknown error calling Ollama";

    await onLog("stderr", `[ollama] ${errorMessage}\n`);

    return {
      exitCode: 1,
      signal: null,
      timedOut,
      errorMessage,
    };
  } finally {
    if (timer) clearTimeout(timer);
  }
}
