/**
 * Plugin bridge initialization.
 *
 * Registers the host's React instances and bridge hook implementations
 * on a global object so that the plugin module loader can inject them
 * into plugin UI bundles at load time.
 *
 * Call `initPluginBridge()` once during app startup (in `main.tsx`), before
 * any plugin UI modules are loaded.
 *
 * @see PLUGIN_SPEC.md §19.0.1 — Plugin UI SDK
 * @see PLUGIN_SPEC.md §19.0.2 — Bundle Isolation
 */

import {
  usePluginData,
  usePluginAction,
  useHostContext,
  usePluginStream,
  usePluginToast,
} from "./bridge.js";
import { createElement } from "react";
import { MarkdownBody } from "../components/MarkdownBody.js";

function SdkMarkdownBlock({ content }: { content: string }) {
  return createElement(MarkdownBody, null, content);
}

function SdkMetricCard({ label, value, unit }: { label: string; value: number | string; unit?: string }) {
  return createElement(
    "div",
    { style: { padding: "0.5rem", borderRadius: "4px", border: "1px solid var(--border)", background: "var(--card)" } },
    createElement("div", { style: { fontSize: "0.7rem", color: "var(--muted-foreground)", marginBottom: "0.25rem" } }, label),
    createElement("div", { style: { fontSize: "1.1rem", fontWeight: 600 } }, String(value), unit ? createElement("span", { style: { fontSize: "0.75rem", marginLeft: "0.2rem" } }, unit) : null),
  );
}

// ---------------------------------------------------------------------------
// Global bridge registry
// ---------------------------------------------------------------------------

/**
 * The global bridge registry shape.
 *
 * This is placed on `globalThis.__paperclipPluginBridge__` and consumed by
 * the plugin module loader to provide implementations for external imports.
 */
export interface PluginBridgeRegistry {
  react: unknown;
  reactDom: unknown;
  sdkUi: Record<string, unknown>;
}

declare global {
  // eslint-disable-next-line no-var
  var __paperclipPluginBridge__: PluginBridgeRegistry | undefined;
}

/**
 * Initialize the plugin bridge global registry.
 *
 * Registers the host's React, ReactDOM, and SDK UI bridge implementations
 * on `globalThis.__paperclipPluginBridge__` so the plugin module loader
 * can provide them to plugin bundles.
 *
 * @param react - The host's React module
 * @param reactDom - The host's ReactDOM module
 */
export function initPluginBridge(
  react: typeof import("react"),
  reactDom: typeof import("react-dom"),
): void {
  globalThis.__paperclipPluginBridge__ = {
    react,
    reactDom,
    sdkUi: {
      usePluginData,
      usePluginAction,
      useHostContext,
      usePluginStream,
      usePluginToast,
      MarkdownBlock: SdkMarkdownBlock,
      MetricCard: SdkMetricCard,
    },
  };
}
