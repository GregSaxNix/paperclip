import type { CLIAdapterModule } from "@paperclipai/adapter-utils";
import { printOllamaStdoutEvent } from "./format-event.js";

export const ollamaCLIAdapter: CLIAdapterModule = {
  type: "ollama_local",
  formatStdoutEvent: printOllamaStdoutEvent,
};
