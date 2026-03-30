export const PLUGIN_ID = "shine.telegram";
export const PLUGIN_VERSION = "0.1.0";

export const TOOL_NAMES = {
  telegramSend: "telegram_send",
  telegramStatus: "telegram_status",
} as const;

export const SLOT_IDS = {
  dashboardWidget: "telegram-dashboard-widget",
} as const;

export const EXPORT_NAMES = {
  dashboardWidget: "TelegramDashboardWidget",
} as const;

export const STATE_KEYS = {
  recentMessages: "recent-messages",
} as const;
