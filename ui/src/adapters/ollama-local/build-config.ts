import type { CreateConfigValues } from "../types";

export function buildOllamaConfig(v: CreateConfigValues): Record<string, unknown> {
  const ac: Record<string, unknown> = {};
  ac.url = v.url || "http://localhost:11434";
  if (v.model) ac.model = v.model;
  if (v.apiKey) ac.apiKey = v.apiKey;
  ac.timeoutMs = 120_000;
  return ac;
}
