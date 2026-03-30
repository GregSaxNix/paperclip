export const PLUGIN_ID = "shine.memory-engine";
export const PLUGIN_VERSION = "0.1.0";

export const TOOL_NAMES = {
  memorySearch: "memory_search",
  memoryExtractFacts: "memory_extract_facts",
  memoryFlush: "memory_flush",
  memoryStats: "memory_stats",
} as const;

export const JOB_KEYS = {
  dailyConsolidation: "daily-consolidation",
} as const;

export const SLOT_IDS = {
  dashboardWidget: "memory-engine-dashboard-widget",
  issueDetailTab: "memory-engine-issue-facts",
} as const;

export const EXPORT_NAMES = {
  dashboardWidget: "MemoryDashboardWidget",
  issueDetailTab: "MemoryIssueFactsTab",
} as const;

export const STATE_KEYS = {
  factIndex: "fact-index",
  consolidationLog: "consolidation-log",
  memoryStats: "memory-stats",
} as const;
