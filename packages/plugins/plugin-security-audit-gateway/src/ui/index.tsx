import { useState } from "react";
import {
  usePluginData,
  usePluginAction,
  type PluginWidgetProps,
} from "@paperclipai/plugin-sdk/ui";

/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */

type QuarantinedItem = {
  id: string;
  name: string;
  type: "tool" | "skill" | "plugin";
  source: string;
  author: string;
  description: string;
  status: "quarantined" | "approved" | "rejected";
  submittedAt: string;
  reviewedAt?: string;
  reviewedBy?: string;
  reviewNote?: string;
};

type AuditLogEntry = {
  id: string;
  itemId: string;
  itemName: string;
  action: "quarantined" | "approved" | "rejected";
  performedBy: string;
  performedAt: string;
  note?: string;
};

type QuarantineSummary = {
  quarantinedCount: number;
  approvedCount: number;
  rejectedCount: number;
  totalCount: number;
  recentLog: AuditLogEntry[];
};

/* -------------------------------------------------------------------------- */
/*  Shared styles                                                             */
/* -------------------------------------------------------------------------- */

const statusColours: Record<string, string> = {
  quarantined: "#d97706",
  approved: "#16a34a",
  rejected: "#dc2626",
};

function StatusBadge({ status }: { status: string }) {
  return (
    <span
      style={{
        display: "inline-block",
        fontSize: "0.7rem",
        fontWeight: 600,
        padding: "0.15rem 0.4rem",
        borderRadius: "4px",
        color: "#fff",
        backgroundColor: statusColours[status] ?? "var(--muted-foreground)",
        textTransform: "uppercase",
        letterSpacing: "0.03em",
      }}
    >
      {status}
    </span>
  );
}

function TypeBadge({ type }: { type: string }) {
  return (
    <span
      style={{
        display: "inline-block",
        fontSize: "0.65rem",
        fontWeight: 500,
        padding: "0.1rem 0.35rem",
        borderRadius: "3px",
        border: "1px solid var(--border)",
        color: "var(--muted-foreground)",
        textTransform: "uppercase",
      }}
    >
      {type}
    </span>
  );
}

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString("en-AU", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  } catch {
    return iso;
  }
}

function formatDateTime(iso: string): string {
  try {
    return new Date(iso).toLocaleString("en-AU", {
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return iso;
  }
}

/* -------------------------------------------------------------------------- */
/*  Dashboard Widget                                                          */
/* -------------------------------------------------------------------------- */

export function SecurityAuditWidget({ context }: PluginWidgetProps) {
  const { data: summary, loading } = usePluginData<QuarantineSummary>(
    "quarantine-summary",
    { companyId: context.companyId ?? "" },
  );

  return (
    <section
      aria-label="Security Audit Gateway"
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
        <strong style={{ fontSize: "0.875rem" }}>Security Audit Gateway</strong>
      </div>

      {loading && (
        <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
          Loading audit summary...
        </div>
      )}

      {summary && (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: "0.5rem",
              fontSize: "0.8rem",
            }}
          >
            <StatCard
              label="Pending"
              value={summary.quarantinedCount}
              accent={statusColours.quarantined}
            />
            <StatCard
              label="Approved"
              value={summary.approvedCount}
              accent={statusColours.approved}
            />
            <StatCard
              label="Rejected"
              value={summary.rejectedCount}
              accent={statusColours.rejected}
            />
          </div>

          {summary.recentLog.length > 0 && (
            <div style={{ fontSize: "0.75rem" }}>
              <div
                style={{
                  fontWeight: 600,
                  marginBottom: "0.3rem",
                  color: "var(--muted-foreground)",
                }}
              >
                Recent Activity
              </div>
              {summary.recentLog.map((entry) => (
                <div
                  key={entry.id}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "0.4rem",
                    marginBottom: "0.25rem",
                  }}
                >
                  <StatusBadge status={entry.action} />
                  <span>{entry.itemName}</span>
                  <span style={{ color: "var(--muted-foreground)" }}>
                    — {formatDate(entry.performedAt)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </section>
  );
}

function StatCard({
  label,
  value,
  accent,
}: {
  label: string;
  value: number | string;
  accent?: string;
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
      <div style={{ fontSize: "1.1rem", fontWeight: 600, color: accent }}>{value}</div>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*  Full Page                                                                 */
/* -------------------------------------------------------------------------- */

type TabKey = "pending" | "approved" | "rejected" | "log";

export function SecurityAuditPage({ context }: PluginWidgetProps) {
  const [activeTab, setActiveTab] = useState<TabKey>("pending");

  const tabs: { key: TabKey; label: string }[] = [
    { key: "pending", label: "Pending Review" },
    { key: "approved", label: "Approved" },
    { key: "rejected", label: "Rejected" },
    { key: "log", label: "Audit Log" },
  ];

  return (
    <section
      aria-label="Security Audit Gateway"
      style={{ padding: "1.5rem", fontSize: "0.85rem" }}
    >
      <h2 style={{ margin: "0 0 1rem 0", fontSize: "1.25rem" }}>
        Security Audit Gateway
      </h2>

      {/* Tab bar */}
      <div
        style={{
          display: "flex",
          gap: "0",
          borderBottom: "2px solid var(--border)",
          marginBottom: "1rem",
        }}
      >
        {tabs.map((tab) => (
          <button
            key={tab.key}
            type="button"
            onClick={() => setActiveTab(tab.key)}
            style={{
              padding: "0.5rem 1rem",
              fontSize: "0.85rem",
              fontWeight: activeTab === tab.key ? 600 : 400,
              border: "none",
              borderBottom:
                activeTab === tab.key
                  ? "2px solid var(--primary)"
                  : "2px solid transparent",
              background: "transparent",
              color:
                activeTab === tab.key
                  ? "var(--primary)"
                  : "var(--muted-foreground)",
              cursor: "pointer",
              marginBottom: "-2px",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "pending" && <PendingTab companyId={context.companyId ?? ""} />}
      {activeTab === "approved" && <ReviewedTab status="approved" />}
      {activeTab === "rejected" && <ReviewedTab status="rejected" />}
      {activeTab === "log" && <AuditLogTab />}
    </section>
  );
}

/* -------------------------------------------------------------------------- */
/*  Pending Review Tab                                                        */
/* -------------------------------------------------------------------------- */

function PendingTab({ companyId }: { companyId: string }) {
  const { data, loading } = usePluginData<{ items: QuarantinedItem[] }>(
    "quarantined-items",
    { status: "quarantined", companyId },
  );
  const approveAction = usePluginAction("approve-item");
  const rejectAction = usePluginAction("reject-item");

  const [reviewNotes, setReviewNotes] = useState<Record<string, string>>({});
  const [processing, setProcessing] = useState<Record<string, boolean>>({});
  const [feedback, setFeedback] = useState<Record<string, string>>({});

  const handleReview = async (
    itemId: string,
    decision: "approved" | "rejected",
  ) => {
    setProcessing((prev) => ({ ...prev, [itemId]: true }));
    setFeedback((prev) => ({ ...prev, [itemId]: "" }));
    try {
      const action = decision === "approved" ? approveAction : rejectAction;
      const result = await action({
        itemId,
        reviewedBy: "Board User",
        note: reviewNotes[itemId] || undefined,
      });
      if (result && typeof result === "object" && "success" in result) {
        const r = result as { success: boolean; error?: string };
        if (r.success) {
          setFeedback((prev) => ({
            ...prev,
            [itemId]: `Item ${decision} successfully.`,
          }));
        } else {
          setFeedback((prev) => ({
            ...prev,
            [itemId]: r.error ?? `Failed to ${decision} item.`,
          }));
        }
      }
    } catch {
      setFeedback((prev) => ({ ...prev, [itemId]: "Action failed." }));
    } finally {
      setProcessing((prev) => ({ ...prev, [itemId]: false }));
    }
  };

  if (loading) {
    return (
      <div style={{ color: "var(--muted-foreground)" }}>
        Loading pending items...
      </div>
    );
  }

  const items = data?.items ?? [];

  if (items.length === 0) {
    return (
      <div style={{ color: "var(--muted-foreground)", padding: "1rem 0" }}>
        No items are currently awaiting review. All clear!
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
      {items.map((item) => (
        <div
          key={item.id}
          style={{
            border: "1px solid var(--border)",
            borderRadius: "6px",
            padding: "0.75rem",
            background: "var(--card)",
          }}
        >
          {/* Header */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
              marginBottom: "0.4rem",
            }}
          >
            <strong>{item.name}</strong>
            <TypeBadge type={item.type} />
            <StatusBadge status={item.status} />
          </div>

          {/* Details */}
          <div
            style={{
              fontSize: "0.8rem",
              color: "var(--muted-foreground)",
              marginBottom: "0.3rem",
            }}
          >
            <span>Source: {item.source}</span>
            <span style={{ margin: "0 0.5rem" }}>|</span>
            <span>Author: {item.author}</span>
            <span style={{ margin: "0 0.5rem" }}>|</span>
            <span>Submitted: {formatDate(item.submittedAt)}</span>
          </div>

          <div style={{ fontSize: "0.8rem", marginBottom: "0.5rem" }}>
            {item.description}
          </div>

          {/* Note input */}
          <div style={{ display: "flex", gap: "0.4rem", alignItems: "center" }}>
            <input
              type="text"
              placeholder="Optional review note..."
              value={reviewNotes[item.id] ?? ""}
              onChange={(e) =>
                setReviewNotes((prev) => ({
                  ...prev,
                  [item.id]: e.target.value,
                }))
              }
              style={{
                flex: 1,
                padding: "0.3rem 0.5rem",
                fontSize: "0.8rem",
                borderRadius: "4px",
                border: "1px solid var(--border)",
                background: "var(--background)",
                color: "var(--foreground)",
              }}
            />
            <button
              type="button"
              disabled={processing[item.id]}
              onClick={() => handleReview(item.id, "approved")}
              style={{
                padding: "0.3rem 0.7rem",
                fontSize: "0.8rem",
                fontWeight: 600,
                borderRadius: "4px",
                border: "none",
                background: "#16a34a",
                color: "#fff",
                cursor: processing[item.id] ? "wait" : "pointer",
                opacity: processing[item.id] ? 0.6 : 1,
              }}
            >
              Approve
            </button>
            <button
              type="button"
              disabled={processing[item.id]}
              onClick={() => handleReview(item.id, "rejected")}
              style={{
                padding: "0.3rem 0.7rem",
                fontSize: "0.8rem",
                fontWeight: 600,
                borderRadius: "4px",
                border: "none",
                background: "#dc2626",
                color: "#fff",
                cursor: processing[item.id] ? "wait" : "pointer",
                opacity: processing[item.id] ? 0.6 : 1,
              }}
            >
              Reject
            </button>
          </div>

          {/* Feedback */}
          {feedback[item.id] && (
            <div
              style={{
                fontSize: "0.75rem",
                color: "var(--muted-foreground)",
                marginTop: "0.3rem",
              }}
            >
              {feedback[item.id]}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*  Approved / Rejected Tab                                                   */
/* -------------------------------------------------------------------------- */

function ReviewedTab({ status }: { status: "approved" | "rejected" }) {
  const { data, loading } = usePluginData<{ items: QuarantinedItem[] }>(
    "quarantined-items",
    { status },
  );

  if (loading) {
    return (
      <div style={{ color: "var(--muted-foreground)" }}>
        Loading {status} items...
      </div>
    );
  }

  const items = data?.items ?? [];

  if (items.length === 0) {
    return (
      <div style={{ color: "var(--muted-foreground)", padding: "1rem 0" }}>
        No {status} items found.
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
      {items.map((item) => (
        <div
          key={item.id}
          style={{
            border: "1px solid var(--border)",
            borderRadius: "6px",
            padding: "0.75rem",
            background: "var(--card)",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
              marginBottom: "0.3rem",
            }}
          >
            <strong>{item.name}</strong>
            <TypeBadge type={item.type} />
            <StatusBadge status={item.status} />
          </div>

          <div
            style={{
              fontSize: "0.8rem",
              color: "var(--muted-foreground)",
              marginBottom: "0.2rem",
            }}
          >
            <span>Source: {item.source}</span>
            <span style={{ margin: "0 0.5rem" }}>|</span>
            <span>Author: {item.author}</span>
          </div>

          <div style={{ fontSize: "0.8rem", marginBottom: "0.3rem" }}>
            {item.description}
          </div>

          <div
            style={{
              fontSize: "0.75rem",
              color: "var(--muted-foreground)",
            }}
          >
            {status === "approved" ? "Approved" : "Rejected"} by{" "}
            <strong>{item.reviewedBy ?? "Unknown"}</strong> on{" "}
            {item.reviewedAt ? formatDate(item.reviewedAt) : "N/A"}
            {item.reviewNote && (
              <span>
                {" "}
                — <em>{item.reviewNote}</em>
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*  Audit Log Tab                                                             */
/* -------------------------------------------------------------------------- */

function AuditLogTab() {
  const { data, loading } = usePluginData<{ entries: AuditLogEntry[] }>(
    "audit-log",
    {},
  );

  if (loading) {
    return (
      <div style={{ color: "var(--muted-foreground)" }}>
        Loading audit log...
      </div>
    );
  }

  const entries = data?.entries ?? [];

  if (entries.length === 0) {
    return (
      <div style={{ color: "var(--muted-foreground)", padding: "1rem 0" }}>
        No audit log entries yet. Activity will appear here as items are
        quarantined, approved, or rejected.
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "0.35rem" }}>
      {entries.map((entry) => (
        <div
          key={entry.id}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            padding: "0.4rem 0.5rem",
            borderRadius: "4px",
            border: "1px solid var(--border)",
            background: "var(--card)",
            fontSize: "0.8rem",
          }}
        >
          <StatusBadge status={entry.action} />
          <strong>{entry.itemName}</strong>
          <span style={{ color: "var(--muted-foreground)" }}>
            by {entry.performedBy}
          </span>
          <span style={{ color: "var(--muted-foreground)", marginLeft: "auto" }}>
            {formatDateTime(entry.performedAt)}
          </span>
          {entry.note && (
            <span
              style={{
                fontSize: "0.75rem",
                color: "var(--muted-foreground)",
                fontStyle: "italic",
              }}
            >
              — {entry.note}
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
