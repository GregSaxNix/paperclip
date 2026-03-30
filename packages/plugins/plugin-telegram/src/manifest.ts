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
  displayName: "Telegram",
  description:
    "Telegram Bot integration for sending notifications on completed issues, agent errors, and ad-hoc messages via the Telegram Bot API.",
  author: "Shine People Solutions",
  categories: ["connector", "ui"],
  capabilities: [
    "companies.read",
    "agents.read",
    "issues.read",
    "issue.comments.read",
    "plugin.state.read",
    "plugin.state.write",
    "events.subscribe",
    "activity.log.write",
    "http.outbound",
    "agent.tools.register",
    "ui.dashboardWidget.register",
  ],
  entrypoints: {
    worker: "./dist/worker.js",
    ui: "./dist/ui",
  },
  instanceConfigSchema: {
    type: "object",
    properties: {
      botToken: {
        type: "string",
        title: "Bot Token",
        description: "Telegram Bot API token (from @BotFather)",
      },
      chatId: {
        type: "string",
        title: "Chat ID",
        description: "Telegram chat ID to send notifications to",
      },
      notifyOnRoutineComplete: {
        type: "boolean",
        title: "Notify on Routine Complete",
        description: "Send a Telegram notification when routines complete",
        default: true,
      },
      notifyOnAgentError: {
        type: "boolean",
        title: "Notify on Agent Error",
        description: "Send a Telegram notification when an agent errors or pauses",
        default: true,
      },
      notifyOnIssueComplete: {
        type: "boolean",
        title: "Notify on Issue Complete",
        description: "Send a Telegram notification when issues are completed",
        default: true,
      },
    },
    required: ["botToken", "chatId"],
  },
  tools: [
    {
      name: TOOL_NAMES.telegramSend,
      displayName: "Send Telegram Message",
      description:
        "Send a message to the configured Telegram chat via the Bot API.",
      parametersSchema: {
        type: "object",
        properties: {
          message: {
            type: "string",
            description: "The message text to send",
          },
          parseMode: {
            type: "string",
            enum: ["HTML", "Markdown"],
            description:
              "Optional parse mode for rich formatting. Defaults to plain text.",
          },
        },
        required: ["message"],
      },
    },
    {
      name: TOOL_NAMES.telegramStatus,
      displayName: "Telegram Bot Status",
      description:
        "Check the Telegram bot connection status by calling the getMe endpoint.",
      parametersSchema: {
        type: "object",
        properties: {},
      },
    },
  ],
  ui: {
    slots: [
      {
        type: "dashboardWidget",
        id: SLOT_IDS.dashboardWidget,
        displayName: "Telegram",
        exportName: EXPORT_NAMES.dashboardWidget,
      },
    ],
  },
};

export default manifest;
