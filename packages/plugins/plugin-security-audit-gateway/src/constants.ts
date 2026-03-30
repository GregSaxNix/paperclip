export const PLUGIN_ID = "shine.security-audit-gateway";
export const PLUGIN_VERSION = "0.1.0";

export const TOOL_NAMES = {
  auditQuarantine: "audit_quarantine",
  auditReview: "audit_review",
  auditList: "audit_list",
} as const;

export const SLOT_IDS = {
  dashboardWidget: "security-audit-dashboard-widget",
  fullPage: "security-audit-page",
} as const;

export const EXPORT_NAMES = {
  dashboardWidget: "SecurityAuditWidget",
  fullPage: "SecurityAuditPage",
} as const;

export const STATE_KEYS = {
  quarantinedItems: "quarantined-items",
  auditLog: "audit-log",
} as const;
