export const PLUGIN_ID = "shine.travel-intelligence";
export const PLUGIN_VERSION = "0.1.0";

export const SLOT_IDS = {
  dashboardWidget: "travel-intelligence-dashboard-widget",
  projectDetailTab: "travel-intelligence-project-tab",
  issueDetailTab: "travel-intelligence-article-tab",
} as const;

export const EXPORT_NAMES = {
  dashboardWidget: "TravelDashboardWidget",
  projectDetailTab: "TravelKnowledgeProjectTab",
  issueDetailTab: "TravelArticleTab",
} as const;

/** Title prefix → article category mapping */
export const ARTICLE_CATEGORIES = {
  airline: "Airline Profile:",
  airport: "Airport Profile:",
  route: "Route:",
  country: "Country:",
} as const;

export type ArticleCategory = "airline" | "airport" | "route" | "country" | "other";
