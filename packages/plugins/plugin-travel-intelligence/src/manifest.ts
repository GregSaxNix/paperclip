import type { PaperclipPluginManifestV1 } from "@paperclipai/plugin-sdk";
import { EXPORT_NAMES, PLUGIN_ID, PLUGIN_VERSION, SLOT_IDS } from "./constants.js";

const manifest: PaperclipPluginManifestV1 = {
  id: PLUGIN_ID,
  apiVersion: 1,
  version: PLUGIN_VERSION,
  displayName: "Travel Intelligence",
  description:
    "Browse and search airline, airport, route, and country knowledge articles. One living wiki article per entity, updated as things change.",
  author: "Shine People Solutions",
  categories: ["ui", "automation"],
  capabilities: [
    "companies.read",
    "projects.read",
    "issues.read",
    "issues.create",
    "issue.documents.read",
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
      projectId: {
        type: "string",
        title: "Travel Intelligence Project ID",
        description:
          "UUID of the Travel Intelligence Paperclip project. Defaults to the known project ID.",
        default: "9c6e52e2-c2eb-49d8-acb2-d36ecf609b4f",
      },
      companyId: {
        type: "string",
        title: "Life Admin Company ID",
        description:
          "UUID of the company that owns the Travel Intelligence project.",
        default: "505ab906-66b5-4400-b131-96b8aee91c5d",
      },
    },
  },
  ui: {
    slots: [
      {
        type: "dashboardWidget",
        id: SLOT_IDS.dashboardWidget,
        displayName: "Travel Intelligence",
        exportName: EXPORT_NAMES.dashboardWidget,
      },
      {
        type: "detailTab",
        id: SLOT_IDS.projectDetailTab,
        displayName: "Knowledge Base",
        exportName: EXPORT_NAMES.projectDetailTab,
        entityTypes: ["project"],
        order: 5,
      },
      {
        type: "detailTab",
        id: SLOT_IDS.issueDetailTab,
        displayName: "Knowledge Article",
        exportName: EXPORT_NAMES.issueDetailTab,
        entityTypes: ["issue"],
        order: 5,
      },
    ],
  },
};

export default manifest;
