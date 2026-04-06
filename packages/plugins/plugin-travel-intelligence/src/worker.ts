import {
  definePlugin,
  runWorker,
  type PluginContext,
} from "@paperclipai/plugin-sdk";
import { ARTICLE_CATEGORIES, type ArticleCategory } from "./constants.js";

/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */

type TravelConfig = {
  projectId?: string;
  companyId?: string;
};

type ArticleSummary = {
  id: string;
  identifier: string | null;
  title: string;
  category: ArticleCategory;
  categoryLabel: string;
  status: string;
  createdAt: string;
  updatedAt: string;
};

type ArticlesResponse = {
  articles: ArticleSummary[];
  counts: Record<ArticleCategory | "total", number>;
};

type ArticleContentResponse = {
  id: string;
  title: string;
  category: ArticleCategory;
  categoryLabel: string;
  body: string | null;
  documentTitle: string | null;
  revision: number | null;
  updatedAt: string | null;
  error?: string;
};

/* -------------------------------------------------------------------------- */
/*  Helpers                                                                   */
/* -------------------------------------------------------------------------- */

const DEFAULT_PROJECT_ID = "9c6e52e2-c2eb-49d8-acb2-d36ecf609b4f";
const DEFAULT_COMPANY_ID = "505ab906-66b5-4400-b131-96b8aee91c5d";

async function resolveConfig(
  ctx: PluginContext,
): Promise<{ projectId: string; companyId: string }> {
  const config = (await ctx.config.get()) as TravelConfig;
  return {
    projectId: config.projectId ?? DEFAULT_PROJECT_ID,
    companyId: config.companyId ?? DEFAULT_COMPANY_ID,
  };
}

function detectCategory(title: string): { category: ArticleCategory; label: string } {
  const t = title.trim();
  if (t.startsWith(ARTICLE_CATEGORIES.airline)) {
    return { category: "airline", label: "Airline" };
  }
  if (t.startsWith(ARTICLE_CATEGORIES.airport)) {
    return { category: "airport", label: "Airport" };
  }
  if (t.startsWith(ARTICLE_CATEGORIES.route)) {
    return { category: "route", label: "Route" };
  }
  if (t.startsWith(ARTICLE_CATEGORIES.country)) {
    return { category: "country", label: "Country" };
  }
  return { category: "other", label: "Other" };
}

/* -------------------------------------------------------------------------- */
/*  Plugin definition                                                         */
/* -------------------------------------------------------------------------- */

const plugin = definePlugin({
  async setup(ctx) {
    ctx.logger.info("Travel Intelligence plugin setup starting");

    // ── travel-articles: list all knowledge articles ─────────────────────
    ctx.data.register("travel-articles", async (params) => {
      const { projectId, companyId } = await resolveConfig(ctx);
      const effectiveCompanyId = (params.companyId as string | undefined) ?? companyId;
      const effectiveProjectId = (params.projectId as string | undefined) ?? projectId;

      try {
        const issues = await ctx.issues.list({
          companyId: effectiveCompanyId,
          projectId: effectiveProjectId,
          limit: 200,
        });

        const articles: ArticleSummary[] = issues.map((issue) => {
          const { category, label } = detectCategory(issue.title);
          return {
            id: issue.id,
            identifier: issue.identifier ?? null,
            title: issue.title,
            category,
            categoryLabel: label,
            status: issue.status,
            createdAt: issue.createdAt instanceof Date ? issue.createdAt.toISOString() : String(issue.createdAt),
            updatedAt: issue.updatedAt instanceof Date ? issue.updatedAt.toISOString() : String(issue.updatedAt),
          };
        });

        // Sort: done articles last (they're stale candidates), then by updated desc
        articles.sort((a, b) => {
          if (a.status === "done" && b.status !== "done") return 1;
          if (a.status !== "done" && b.status === "done") return -1;
          return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
        });

        const counts: Record<ArticleCategory | "total", number> = {
          total: articles.length,
          airline: 0,
          airport: 0,
          route: 0,
          country: 0,
          other: 0,
        };
        for (const a of articles) counts[a.category]++;

        return { articles, counts } satisfies ArticlesResponse;
      } catch (err) {
        ctx.logger.error("Failed to list travel articles", { error: String(err) });
        return { articles: [], counts: { total: 0, airline: 0, airport: 0, route: 0, country: 0, other: 0 }, error: String(err) };
      }
    });

    // ── article-content: fetch the knowledge document for one issue ───────
    ctx.data.register("article-content", async (params) => {
      const { companyId } = await resolveConfig(ctx);
      const issueId = params.issueId as string | undefined;
      const effectiveCompanyId = (params.companyId as string | undefined) ?? companyId;

      if (!issueId) {
        return { error: "issueId is required" } satisfies Partial<ArticleContentResponse>;
      }

      try {
        const [issue, doc] = await Promise.all([
          ctx.issues.get(issueId, effectiveCompanyId),
          ctx.issues.documents.get(issueId, "knowledge", effectiveCompanyId),
        ]);

        if (!issue) {
          return { error: `Issue ${issueId} not found` } satisfies Partial<ArticleContentResponse>;
        }

        const { category, label } = detectCategory(issue.title);

        return {
          id: issue.id,
          title: issue.title,
          category,
          categoryLabel: label,
          body: doc?.body ?? null,
          documentTitle: doc?.title ?? null,
          revision: doc?.latestRevisionNumber ?? null,
          updatedAt: doc?.updatedAt instanceof Date
            ? doc.updatedAt.toISOString()
            : doc?.updatedAt != null
              ? String(doc.updatedAt)
              : issue.updatedAt instanceof Date
                ? issue.updatedAt.toISOString()
                : String(issue.updatedAt),
        } satisfies ArticleContentResponse;
      } catch (err) {
        ctx.logger.error("Failed to fetch article content", { issueId, error: String(err) });
        return { error: String(err) } satisfies Partial<ArticleContentResponse>;
      }
    });

    ctx.logger.info("Travel Intelligence plugin setup complete");
  },

  async onHealth() {
    return { status: "ok", message: "Travel Intelligence plugin is healthy" };
  },
});

export default plugin;
runWorker(plugin, import.meta.url);
