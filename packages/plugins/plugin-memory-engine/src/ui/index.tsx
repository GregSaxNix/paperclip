import { useState } from "react";
import {
  usePluginData,
  usePluginAction,
  type PluginWidgetProps,
  type PluginDetailTabProps,
} from "@paperclipai/plugin-sdk/ui";

/* -------------------------------------------------------------------------- */
/*  Dashboard Widget                                                          */
/* -------------------------------------------------------------------------- */

type MemoryStatsData = {
  dailyNoteCount: number;
  knowledgeGraphEntityCount: number;
  memoryMdSizeBytes: number;
  memoryMdLines: number;
  lastUpdated: string;
  error?: string;
};

export function MemoryDashboardWidget({ context }: PluginWidgetProps) {
  const [flushing, setFlushing] = useState(false);
  const [flushMessage, setFlushMessage] = useState<string | null>(null);

  const { data: stats, loading: statsLoading } = usePluginData<MemoryStatsData>(
    "memory-stats",
    { agentId: "", companyId: context.companyId ?? "" },
  );

  const triggerFlush = usePluginAction("trigger-flush");

  const handleFlush = async () => {
    setFlushing(true);
    setFlushMessage(null);
    try {
      const result = await triggerFlush({ agentId: "" });
      if (result && typeof result === "object" && "message" in result) {
        setFlushMessage(String((result as { message: string }).message));
      }
    } catch {
      setFlushMessage("Flush failed");
    } finally {
      setFlushing(false);
    }
  };

  return (
    <section
      aria-label="Memory Engine"
      style={{
        padding: "1rem",
        display: "flex",
        flexDirection: "column",
        gap: "0.75rem",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <strong style={{ fontSize: "0.875rem" }}>Memory Engine</strong>
        <button
          type="button"
          onClick={handleFlush}
          disabled={flushing}
          style={{
            fontSize: "0.75rem",
            padding: "0.25rem 0.5rem",
            borderRadius: "4px",
            border: "1px solid var(--border)",
            background: "var(--primary)",
            color: "var(--primary-foreground)",
            cursor: flushing ? "wait" : "pointer",
            opacity: flushing ? 0.6 : 1,
          }}
        >
          {flushing ? "Saving..." : "Save to MEMORY.md"}
        </button>
      </div>

      {flushMessage && (
        <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
          {flushMessage}
        </div>
      )}

      {statsLoading && (
        <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
          Loading memory stats...
        </div>
      )}

      {stats && !stats.error && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "0.5rem",
            fontSize: "0.8rem",
          }}
        >
          <StatCard label="Daily Notes" value={stats.dailyNoteCount} />
          <StatCard
            label="Knowledge Graph"
            value={stats.knowledgeGraphEntityCount}
          />
          <StatCard label="MEMORY.md Lines" value={stats.memoryMdLines} />
          <StatCard
            label="MEMORY.md Size"
            value={`${(stats.memoryMdSizeBytes / 1024).toFixed(1)} KB`}
          />
        </div>
      )}

      {stats?.error && (
        <div style={{ fontSize: "0.8rem", color: "var(--destructive)" }}>
          {stats.error}
        </div>
      )}
    </section>
  );
}

function StatCard({
  label,
  value,
}: {
  label: string;
  value: number | string;
}) {
  return (
    <div
      style={{
        padding: "0.5rem",
        borderRadius: "4px",
        border: "1px solid var(--border)",
        background: "var(--card)",
      }}
    >
      <div
        style={{
          fontSize: "0.7rem",
          color: "var(--muted-foreground)",
          marginBottom: "0.25rem",
        }}
      >
        {label}
      </div>
      <div style={{ fontSize: "1.1rem", fontWeight: 600 }}>{value}</div>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*  Issue Detail Tab — Extracted Facts                                        */
/* -------------------------------------------------------------------------- */

type ExtractedFact = {
  content: string;
  source: string;
  extractedAt: string;
  category: string;
};

export function MemoryIssueFactsTab({ context }: PluginDetailTabProps) {
  const { data: factsData, loading } = usePluginData<{
    facts: ExtractedFact[];
  }>("recent-facts", { agentId: "" });

  const issueFacts =
    factsData?.facts?.filter((f) => f.source.includes(context.entityId)) ?? [];

  return (
    <section
      aria-label="Memory Facts"
      style={{ padding: "1rem", fontSize: "0.85rem" }}
    >
      <strong>Extracted Facts</strong>

      {loading && (
        <div style={{ color: "var(--muted-foreground)", marginTop: "0.5rem" }}>
          Loading facts...
        </div>
      )}

      {!loading && issueFacts.length === 0 && (
        <div style={{ color: "var(--muted-foreground)", marginTop: "0.5rem" }}>
          No facts have been extracted from this issue yet. Use the{" "}
          <code>memory_extract_facts</code> tool or wait for the daily
          consolidation job.
        </div>
      )}

      {issueFacts.length > 0 && (
        <ul style={{ marginTop: "0.5rem", paddingLeft: "1.2rem" }}>
          {issueFacts.map((fact, i) => (
            <li
              key={`${fact.extractedAt}-${i}`}
              style={{ marginBottom: "0.35rem" }}
            >
              {fact.content}
              <span
                style={{
                  fontSize: "0.7rem",
                  color: "var(--muted-foreground)",
                  marginLeft: "0.5rem",
                }}
              >
                ({new Date(fact.extractedAt).toLocaleDateString()})
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
