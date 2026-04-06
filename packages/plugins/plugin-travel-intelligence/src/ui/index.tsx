import { useState } from "react";
import {
  usePluginData,
  MarkdownBlock,
  MetricCard,
  type PluginWidgetProps,
  type PluginDetailTabProps,
} from "@paperclipai/plugin-sdk/ui";
import type { ArticleCategory } from "../constants.js";

/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */

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
  error?: string;
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

type CategoryTab = "all" | ArticleCategory;

/* -------------------------------------------------------------------------- */
/*  Category icons                                                            */
/* -------------------------------------------------------------------------- */

const CATEGORY_ICONS: Record<ArticleCategory | "all", string> = {
  all: "🌏",
  airline: "✈",
  airport: "🛬",
  route: "🗺",
  country: "🏳",
  other: "📄",
};

const CATEGORY_LABELS: Record<CategoryTab, string> = {
  all: "All",
  airline: "Airlines",
  airport: "Airports",
  route: "Routes",
  country: "Countries",
  other: "Other",
};

/* -------------------------------------------------------------------------- */
/*  Helpers                                                                   */
/* -------------------------------------------------------------------------- */

function relativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);
  if (mins < 2) return "just now";
  if (mins < 60) return `${mins}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 30) return `${days}d ago`;
  return new Date(iso).toLocaleDateString("en-AU", { day: "numeric", month: "short", year: "numeric" });
}

/** Strip the category prefix from the title for cleaner display. */
function shortTitle(title: string): string {
  return title
    .replace(/^Airline Profile:\s*/i, "")
    .replace(/^Airport Profile:\s*/i, "")
    .replace(/^Route:\s*/i, "")
    .replace(/^Country:\s*/i, "")
    .trim();
}

/* -------------------------------------------------------------------------- */
/*  Article card                                                              */
/* -------------------------------------------------------------------------- */

function ArticleCard({
  article,
  selected,
  onClick,
}: {
  article: ArticleSummary;
  selected: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "0.25rem",
        padding: "0.75rem",
        borderRadius: "6px",
        border: `1px solid ${selected ? "var(--primary)" : "var(--border)"}`,
        background: selected ? "var(--accent)" : "var(--card)",
        cursor: "pointer",
        textAlign: "left",
        width: "100%",
        transition: "border-color 0.15s, background 0.15s",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
        <span style={{ fontSize: "1rem" }}>{CATEGORY_ICONS[article.category]}</span>
        <span style={{ fontSize: "0.8rem", fontWeight: 600, color: "var(--foreground)", lineHeight: 1.3 }}>
          {shortTitle(article.title)}
        </span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", flexWrap: "wrap" }}>
        <span
          style={{
            fontSize: "0.65rem",
            padding: "0.1rem 0.4rem",
            borderRadius: "3px",
            background: "var(--muted)",
            color: "var(--muted-foreground)",
            fontWeight: 500,
          }}
        >
          {article.categoryLabel}
        </span>
        {article.identifier && (
          <span style={{ fontSize: "0.65rem", color: "var(--muted-foreground)" }}>
            {article.identifier}
          </span>
        )}
        <span style={{ fontSize: "0.65rem", color: "var(--muted-foreground)", marginLeft: "auto" }}>
          {relativeTime(article.updatedAt)}
        </span>
      </div>
    </button>
  );
}

/* -------------------------------------------------------------------------- */
/*  Article detail pane                                                       */
/* -------------------------------------------------------------------------- */

function ArticleDetailPane({
  issueId,
  companyId,
  onClose,
}: {
  issueId: string;
  companyId: string;
  onClose: () => void;
}) {
  const { data, loading, error } = usePluginData<ArticleContentResponse>("article-content", {
    issueId,
    companyId,
  });

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "0.75rem",
        height: "100%",
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "0.5rem" }}>
        {data && !data.error && (
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <span style={{ fontSize: "1.1rem" }}>{CATEGORY_ICONS[data.category]}</span>
              <span style={{ fontSize: "0.95rem", fontWeight: 700 }}>{shortTitle(data.title)}</span>
            </div>
            {data.updatedAt && (
              <div style={{ fontSize: "0.7rem", color: "var(--muted-foreground)", marginTop: "0.2rem" }}>
                Last updated {relativeTime(data.updatedAt)}
                {data.revision != null && ` · revision ${data.revision}`}
              </div>
            )}
          </div>
        )}
        <button
          type="button"
          onClick={onClose}
          aria-label="Close article"
          style={{
            flexShrink: 0,
            fontSize: "0.75rem",
            padding: "0.2rem 0.5rem",
            borderRadius: "4px",
            border: "1px solid var(--border)",
            background: "var(--card)",
            color: "var(--muted-foreground)",
            cursor: "pointer",
          }}
        >
          ✕ Close
        </button>
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflowY: "auto" }}>
        {loading && (
          <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>Loading article…</div>
        )}
        {error && (
          <div style={{ fontSize: "0.8rem", color: "var(--destructive)" }}>
            Failed to load article: {error.message}
          </div>
        )}
        {data?.error && (
          <div style={{ fontSize: "0.8rem", color: "var(--destructive)" }}>{data.error}</div>
        )}
        {data?.body ? (
          <MarkdownBlock content={data.body} />
        ) : (
          !loading && !error && (
            <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
              No knowledge document found for this article yet.
            </div>
          )
        )}
      </div>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*  Project detail tab — the main knowledge browser                          */
/* -------------------------------------------------------------------------- */

export function TravelKnowledgeProjectTab({ context }: PluginDetailTabProps) {
  const [activeTab, setActiveTab] = useState<CategoryTab>("all");
  const [search, setSearch] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const companyId = context.companyId ?? "";

  const { data, loading, error } = usePluginData<ArticlesResponse>("travel-articles", {
    companyId,
    projectId: context.entityId,
  });

  const articles = data?.articles ?? [];
  const counts = data?.counts;

  const filtered = articles.filter((a) => {
    const matchesTab = activeTab === "all" || a.category === activeTab;
    const matchesSearch =
      search.trim() === "" ||
      a.title.toLowerCase().includes(search.toLowerCase());
    return matchesTab && matchesSearch;
  });

  const tabs: CategoryTab[] = ["all", "airline", "airport", "route", "country"];

  return (
    <section
      aria-label="Travel Knowledge Base"
      style={{ padding: "1rem", display: "flex", flexDirection: "column", gap: "0.75rem", height: "100%" }}
    >
      {/* Search */}
      <input
        type="search"
        placeholder="Search airlines, airports, routes…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{
          width: "100%",
          padding: "0.5rem 0.75rem",
          borderRadius: "6px",
          border: "1px solid var(--border)",
          background: "var(--input)",
          color: "var(--foreground)",
          fontSize: "0.875rem",
          outline: "none",
          boxSizing: "border-box",
        }}
      />

      {/* Category tabs */}
      <div style={{ display: "flex", gap: "0.3rem", flexWrap: "wrap" }}>
        {tabs.map((tab) => (
          <button
            key={tab}
            type="button"
            onClick={() => setActiveTab(tab)}
            style={{
              fontSize: "0.75rem",
              padding: "0.3rem 0.6rem",
              borderRadius: "4px",
              border: "1px solid var(--border)",
              background: activeTab === tab ? "var(--primary)" : "var(--card)",
              color: activeTab === tab ? "var(--primary-foreground)" : "var(--foreground)",
              cursor: "pointer",
              fontWeight: activeTab === tab ? 600 : 400,
            }}
          >
            {CATEGORY_ICONS[tab]} {CATEGORY_LABELS[tab]}
            {counts && tab !== "all" && counts[tab] > 0 && (
              <span style={{ marginLeft: "0.3rem", opacity: 0.7 }}>({counts[tab]})</span>
            )}
            {counts && tab === "all" && counts.total > 0 && (
              <span style={{ marginLeft: "0.3rem", opacity: 0.7 }}>({counts.total})</span>
            )}
          </button>
        ))}
      </div>

      {/* Body: list + detail pane */}
      <div style={{ flex: 1, overflow: "hidden", display: "flex", gap: "1rem" }}>
        {/* Article list */}
        <div
          style={{
            flex: selectedId ? "0 0 280px" : "1",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "0.4rem",
          }}
        >
          {loading && (
            <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>Loading knowledge base…</div>
          )}
          {error && (
            <div style={{ fontSize: "0.8rem", color: "var(--destructive)" }}>
              Failed to load articles: {error.message}
            </div>
          )}
          {data?.error && (
            <div style={{ fontSize: "0.8rem", color: "var(--destructive)" }}>{data.error}</div>
          )}
          {!loading && filtered.length === 0 && !error && !data?.error && (
            <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
              {search ? "No articles match your search." : "No articles in this category yet."}
            </div>
          )}
          {filtered.map((article) => (
            <ArticleCard
              key={article.id}
              article={article}
              selected={selectedId === article.id}
              onClick={() => setSelectedId(selectedId === article.id ? null : article.id)}
            />
          ))}
        </div>

        {/* Detail pane */}
        {selectedId && (
          <div
            style={{
              flex: 1,
              overflow: "hidden",
              padding: "1rem",
              borderRadius: "6px",
              border: "1px solid var(--border)",
              background: "var(--card)",
            }}
          >
            <ArticleDetailPane
              issueId={selectedId}
              companyId={companyId}
              onClose={() => setSelectedId(null)}
            />
          </div>
        )}
      </div>
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  Issue detail tab — view a single article's knowledge document             */
/* -------------------------------------------------------------------------- */

export function TravelArticleTab({ context }: PluginDetailTabProps) {
  const companyId = context.companyId ?? "";
  const issueId = context.entityId;

  const { data, loading, error } = usePluginData<ArticleContentResponse>("article-content", {
    issueId,
    companyId,
  });

  return (
    <section
      aria-label="Knowledge Article"
      style={{ padding: "1rem", display: "flex", flexDirection: "column", gap: "0.75rem" }}
    >
      {loading && (
        <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>Loading knowledge article…</div>
      )}
      {error && (
        <div style={{ fontSize: "0.8rem", color: "var(--destructive)" }}>
          Failed to load article: {error.message}
        </div>
      )}
      {data?.error && (
        <div style={{ fontSize: "0.8rem", color: "var(--destructive)" }}>{data.error}</div>
      )}
      {data && !data.error && (
        <>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", flexWrap: "wrap" }}>
            <span
              style={{
                fontSize: "0.7rem",
                padding: "0.15rem 0.45rem",
                borderRadius: "3px",
                background: "var(--muted)",
                color: "var(--muted-foreground)",
                fontWeight: 500,
              }}
            >
              {CATEGORY_ICONS[data.category]} {data.categoryLabel}
            </span>
            {data.updatedAt && (
              <span style={{ fontSize: "0.7rem", color: "var(--muted-foreground)" }}>
                Last updated {relativeTime(data.updatedAt)}
                {data.revision != null && ` · revision ${data.revision}`}
              </span>
            )}
          </div>
          {data.body ? (
            <MarkdownBlock content={data.body} />
          ) : (
            <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
              No knowledge document has been written for this article yet. Ask an agent to research and document it.
            </div>
          )}
        </>
      )}
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  Dashboard widget                                                          */
/* -------------------------------------------------------------------------- */

export function TravelDashboardWidget({ context }: PluginWidgetProps) {
  const companyId = context.companyId ?? "";

  const { data, loading } = usePluginData<ArticlesResponse>("travel-articles", {
    companyId,
  });

  const counts = data?.counts;

  return (
    <section
      aria-label="Travel Intelligence"
      style={{ padding: "1rem", display: "flex", flexDirection: "column", gap: "0.75rem" }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
        <span style={{ fontSize: "1.1rem" }}>🌏</span>
        <strong style={{ fontSize: "0.875rem" }}>Travel Intelligence</strong>
      </div>

      {loading && (
        <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>Loading…</div>
      )}

      {counts && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "0.5rem",
          }}
        >
          <MetricCard label="Airlines" value={counts.airline} />
          <MetricCard label="Airports" value={counts.airport} />
          <MetricCard label="Routes" value={counts.route} />
          <MetricCard label="Countries" value={counts.country} />
        </div>
      )}

      {data?.error && (
        <div style={{ fontSize: "0.75rem", color: "var(--destructive)" }}>{data.error}</div>
      )}
    </section>
  );
}
