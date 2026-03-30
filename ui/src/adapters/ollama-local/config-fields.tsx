import type { AdapterConfigFieldsProps } from "../types";
import {
  Field,
  DraftInput,
  help,
} from "../../components/agent-config-primitives";

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
          <select
            value={
              isCreate
                ? values!.model ?? ""
                : eff("adapterConfig", "model", String(config.model ?? ""))
            }
            onChange={(e) =>
              isCreate
                ? set!({ model: e.target.value })
                : mark("adapterConfig", "model", e.target.value || undefined)
            }
            className={inputClass}
          >
            <option value="">Select a model...</option>
            {models.map((m) => (
              <option key={m.id} value={m.id}>
                {m.label}
              </option>
            ))}
          </select>
        ) : (
          <DraftInput
            value={
              isCreate
                ? values!.model ?? ""
                : eff("adapterConfig", "model", String(config.model ?? ""))
            }
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
    </>
  );
}
