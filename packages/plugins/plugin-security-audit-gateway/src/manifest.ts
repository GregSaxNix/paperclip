import type { PaperclipPluginManifestV1 } from "@paperclipai/plugin-sdk";
import {
  EXPORT_NAMES,
  PLUGIN_ID,
  PLUGIN_VERSION,
  SLOT_IDS,
  TOOL_NAMES,
} from "./constants.js";

const manifest: PaperclipPluginManifestV1 = {
  id: PLUGIN_ID,
  apiVersion: 1,
  version: PLUGIN_VERSION,
  displayName: "Security Audit Gateway",
  description:
    "Quarantine imported tools, skills, and plugins before activation. Board users can approve or reject via the UI, with a full activity audit log.",
  author: "Shine People Solutions",
  categories: ["automation", "ui"],
  capabilities: [
    "companies.read",
    "agents.read",
    "issues.read",
    "plugin.state.read",
    "plugin.state.write",
    "events.subscribe",
    "activity.log.write",
    "agent.tools.register",
    "ui.dashboardWidget.register",
    "ui.page.register",
  ],
  entrypoints: {
    worker: "./dist/worker.js",
    ui: "./dist/ui",
  },
  instanceConfigSchema: {
    type: "object",
    properties: {
      autoApproveFromTrustedAuthors: {
        type: "boolean",
        title: "Auto-approve from Trusted Authors",
        description:
          "Automatically approve tools and skills submitted by trusted authors.",
        default: false,
      },
      trustedAuthors: {
        type: "array",
        title: "Trusted Authors",
        description:
          "List of author identifiers whose submissions are automatically approved.",
        items: { type: "string" },
        default: [],
      },
    },
  },
  tools: [
    {
      name: TOOL_NAMES.auditQuarantine,
      displayName: "Quarantine Item",
      description:
        "Submit a tool, skill, or plugin for quarantine review. The item will be held until a board user approves or rejects it.",
      parametersSchema: {
        type: "object",
        properties: {
          name: {
            type: "string",
            description: "Name of the tool, skill, or plugin",
          },
          type: {
            type: "string",
            enum: ["tool", "skill", "plugin"],
            description: "The type of item being quarantined",
          },
          source: {
            type: "string",
            description: "Where the item originated from (e.g. repository URL, marketplace)",
          },
          author: {
            type: "string",
            description: "The author or creator of the item",
          },
          description: {
            type: "string",
            description: "A brief description of what the item does",
          },
        },
        required: ["name", "type", "source", "author", "description"],
      },
    },
    {
      name: TOOL_NAMES.auditReview,
      displayName: "Review Quarantined Item",
      description:
        "Approve or reject a quarantined item. Updates the item status and logs the decision to the audit trail.",
      parametersSchema: {
        type: "object",
        properties: {
          itemId: {
            type: "string",
            description: "The ID of the quarantined item to review",
          },
          decision: {
            type: "string",
            enum: ["approved", "rejected"],
            description: "Whether to approve or reject the item",
          },
          reviewedBy: {
            type: "string",
            description: "The user performing the review",
          },
          note: {
            type: "string",
            description: "Optional note explaining the decision",
          },
        },
        required: ["itemId", "decision", "reviewedBy"],
      },
    },
    {
      name: TOOL_NAMES.auditList,
      displayName: "List Quarantined Items",
      description:
        "List quarantined items, optionally filtered by status.",
      parametersSchema: {
        type: "object",
        properties: {
          status: {
            type: "string",
            enum: ["quarantined", "approved", "rejected", "all"],
            description:
              "Filter by status. Defaults to quarantined (pending review).",
            default: "quarantined",
          },
        },
      },
    },
  ],
  ui: {
    slots: [
      {
        type: "dashboardWidget",
        id: SLOT_IDS.dashboardWidget,
        displayName: "Security Audit Gateway",
        exportName: EXPORT_NAMES.dashboardWidget,
      },
      {
        type: "page",
        id: SLOT_IDS.fullPage,
        displayName: "Security Audit Gateway",
        exportName: EXPORT_NAMES.fullPage,
      },
    ],
  },
};

export default manifest;
