import type { TranscriptEntry } from "../types";

export function parseOllamaStdoutLine(line: string, ts: string): TranscriptEntry[] {
  // Filter out internal log lines, pass through assistant content
  if (line.startsWith("[ollama]")) {
    return [{ kind: "stdout", ts, text: line }];
  }
  return [{ kind: "assistant", ts, text: line }];
}
