import type { PaperclipPluginManifestV1 } from "@paperclipai/plugin-sdk";
import {
  EXPORT_NAMES,
  JOB_KEYS,
  PLUGIN_ID,
  PLUGIN_VERSION,
  SLOT_IDS,
  TOOL_NAMES,
} from "./constants.js";

const manifest: PaperclipPluginManifestV1 = {
  id: PLUGIN_ID,
  apiVersion: 1,
  version: PLUGIN_VERSION,
  displayName: "Memory Engine",
  description:
    "Fact extraction from completed tasks, full-text search across memory files, AI-driven consolidation, and flush-to-MEMORY.md for promoting daily entries to long-term memory.",
  author: "Shine Operations",
  categories: ["automation", "ui"],
  capabilities: [
    "companies.read",
    "projects.read",
    "project.workspaces.read",
    "issues.read",
    "issue.comments.read",
    "agents.read",
    "activity.log.write",
    "plugin.state.read",
    "plugin.state.write",
    "events.subscribe",
    "jobs.schedule",
    "agent.tools.register",
    "ui.dashboardWidget.register",
    "ui.detailTab.register",
  ],
  entrypoints: {
    worker: "./dist/worker.js",
    ui: "./dist/ui",
  },
  instanceConfigSchema: {
    type: "object",
    properties: {
      agentHomePath: {
        type: "string",
        title: "Agent Home Path",
        description:
          "Root path for agent memory files (MEMORY.md, memory/ directory, life/ directory)",
      },
      consolidationSchedule: {
        type: "string",
        title: "Consolidation Schedule (Cron)",
        description: "Cron expression for daily fact consolidation job",
        default: "0 23 * * *",
      },
    },
  },
  tools: [
    {
      name: TOOL_NAMES.memorySearch,
      displayName: "Memory Search",
      description:
        "Full-text search across all memory files (daily notes, MEMORY.md, knowledge graph entities). Returns matching excerpts with file paths.",
      parametersSchema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "Search query — keywords or natural language phrase",
          },
          scope: {
            type: "string",
            enum: ["all", "daily_notes", "knowledge_graph", "tacit"],
            description:
              "Limit search to a specific memory layer. Defaults to all.",
            default: "all",
          },
          limit: {
            type: "number",
            description: "Maximum number of results to return",
            default: 10,
          },
        },
        required: ["query"],
      },
    },
    {
      name: TOOL_NAMES.memoryExtractFacts,
      displayName: "Extract Facts from Issue",
      description:
        "Extract durable facts from a completed issue thread (title, description, comments) and store them in the knowledge graph.",
      parametersSchema: {
        type: "object",
        properties: {
          issueId: {
            type: "string",
            description: "The issue ID to extract facts from",
          },
          agentId: {
            type: "string",
            description: "The agent ID whose memory to update",
          },
        },
        required: ["issueId", "agentId"],
      },
    },
    {
      name: TOOL_NAMES.memoryFlush,
      displayName: "Flush to MEMORY.md",
      description:
        "Promote important entries from recent daily notes into the agent's long-term MEMORY.md file. Merges duplicates, resolves contradictions, and updates existing sections.",
      parametersSchema: {
        type: "object",
        properties: {
          agentId: {
            type: "string",
            description: "The agent ID whose memory to flush",
          },
          daysBack: {
            type: "number",
            description:
              "Number of days of daily notes to review. Defaults to 7.",
            default: 7,
          },
        },
        required: ["agentId"],
      },
    },
    {
      name: TOOL_NAMES.memoryStats,
      displayName: "Memory Statistics",
      description:
        "Returns statistics about the agent's memory: number of daily notes, knowledge graph entities, facts, and MEMORY.md size.",
      parametersSchema: {
        type: "object",
        properties: {
          agentId: {
            type: "string",
            description: "The agent ID to get stats for",
          },
        },
        required: ["agentId"],
      },
    },
  ],
  jobs: [
    {
      jobKey: JOB_KEYS.dailyConsolidation,
      displayName: "Daily Memory Consolidation",
      description:
        "Reviews daily notes, extracts facts to knowledge graph, merges duplicates, and decays stale entries.",
      schedule: "0 23 * * *",
    },
  ],
  ui: {
    slots: [
      {
        type: "dashboardWidget",
        id: SLOT_IDS.dashboardWidget,
        displayName: "Memory Engine",
        exportName: EXPORT_NAMES.dashboardWidget,
      },
      {
        type: "detailTab",
        id: SLOT_IDS.issueDetailTab,
        displayName: "Memory Facts",
        exportName: EXPORT_NAMES.issueDetailTab,
        entityTypes: ["issue"],
      },
    ],
  },
};

export default manifest;
