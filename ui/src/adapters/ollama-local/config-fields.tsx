import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import type { AdapterConfigFieldsProps } from "../types";
import {
  Field,
  DraftInput,
  help,
} from "../../components/agent-config-primitives";
import { ModelDropdown } from "../../components/AgentConfigForm";

const inputClass =
  "w-full rounded-md border border-border px-2.5 py-1.5 bg-transparent outline-none text-sm font-mono placeholder:text-muted-foreground/40";

export function OllamaConfigFields({
  isCreate,
  values,
  set,
  config,
  eff,
  mark,
  models,
}: AdapterConfigFieldsProps) {
  const [modelOpen, setModelOpen] = useState(false);
  const [keyVisible, setKeyVisible] = useState(false);

  const currentModel = isCreate
    ? values!.model ?? ""
    : eff("adapterConfig", "model", String(config.model ?? ""));

  const currentApiKey = isCreate
    ? values!.apiKey ?? ""
    : eff("adapterConfig", "apiKey", String(config.apiKey ?? ""));

  return (
    <>
      <Field label="Ollama URL" hint="Base URL for Ollama API. Default: http://localhost:11434">
        <DraftInput
          value={
            isCreate
              ? values!.url ?? "http://localhost:11434"
              : eff("adapterConfig", "url", String(config.url ?? "http://localhost:11434"))
          }
          onCommit={(v) =>
            isCreate
              ? set!({ url: v })
              : mark("adapterConfig", "url", v || undefined)
          }
          immediate
          className={inputClass}
          placeholder="http://localhost:11434"
        />
      </Field>
      <Field label="Model" hint={help.model}>
        {models.length > 0 ? (
          <ModelDropdown
            models={models}
            value={currentModel}
            onChange={(v) =>
              isCreate
                ? set!({ model: v })
                : mark("adapterConfig", "model", v || undefined)
            }
            open={modelOpen}
            onOpenChange={setModelOpen}
            allowDefault={false}
            required={false}
            groupByProvider={false}
          />
        ) : (
          <DraftInput
            value={currentModel}
            onCommit={(v) =>
              isCreate
                ? set!({ model: v })
                : mark("adapterConfig", "model", v || undefined)
            }
            immediate
            className={inputClass}
            placeholder="llama3.1:8b-instruct"
          />
        )}
      </Field>
      <Field label="API Key" hint="Bearer token for cloud API auth (DeepSeek, xAI, Mistral, etc.). Leave empty for local Ollama.">
        <div className="relative">
          <button
            type="button"
            onClick={() => setKeyVisible((v) => !v)}
            className="absolute left-2 top-1/2 -translate-y-1/2 text-muted-foreground/50 hover:text-muted-foreground transition-colors"
          >
            {keyVisible ? <Eye className="h-3.5 w-3.5" /> : <EyeOff className="h-3.5 w-3.5" />}
          </button>
          <DraftInput
            value={currentApiKey}
            onCommit={(v) =>
              isCreate
                ? set!({ apiKey: v })
                : mark("adapterConfig", "apiKey", v || undefined)
            }
            immediate
            type={keyVisible ? "text" : "password"}
            className={inputClass + " pl-8"}
            placeholder="sk-..."
          />
        </div>
      </Field>
    </>
  );
}
