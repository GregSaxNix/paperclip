import {
  definePlugin,
  runWorker,
  type PluginContext,
  type ToolRunContext,
  type ToolResult,
} from "@paperclipai/plugin-sdk";
import {
  PLUGIN_ID,
  STATE_KEYS,
  TOOL_NAMES,
} from "./constants.js";

/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */

type SecurityAuditConfig = {
  autoApproveFromTrustedAuthors?: boolean;
  trustedAuthors?: string[];
};

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

/* -------------------------------------------------------------------------- */
/*  Helpers                                                                   */
/* -------------------------------------------------------------------------- */

async function getItems(ctx: PluginContext): Promise<QuarantinedItem[]> {
  const stored = await ctx.state.get({
    scopeKind: "instance",
    stateKey: STATE_KEYS.quarantinedItems,
  });
  if (Array.isArray(stored)) return stored as QuarantinedItem[];
  if (stored && typeof stored === "object" && "items" in stored) {
    return (stored as { items: QuarantinedItem[] }).items;
  }
  return [];
}

async function saveItems(ctx: PluginContext, items: QuarantinedItem[]): Promise<void> {
  await ctx.state.set(
    { scopeKind: "instance", stateKey: STATE_KEYS.quarantinedItems },
    items,
  );
}

async function getAuditLog(ctx: PluginContext): Promise<AuditLogEntry[]> {
  const stored = await ctx.state.get({
    scopeKind: "instance",
    stateKey: STATE_KEYS.auditLog,
  });
  if (Array.isArray(stored)) return stored as AuditLogEntry[];
  if (stored && typeof stored === "object" && "entries" in stored) {
    return (stored as { entries: AuditLogEntry[] }).entries;
  }
  return [];
}

async function appendAuditLog(ctx: PluginContext, entry: AuditLogEntry): Promise<void> {
  const log = await getAuditLog(ctx);
  log.push(entry);
  // Keep only the last 100 entries
  const trimmed = log.slice(-100);
  await ctx.state.set(
    { scopeKind: "instance", stateKey: STATE_KEYS.auditLog },
    trimmed,
  );
}

/** Find the first company visible to this plugin. */
async function firstCompanyId(ctx: PluginContext): Promise<string | null> {
  const companies = await ctx.companies.list();
  return companies[0]?.id ?? null;
}

/* -------------------------------------------------------------------------- */
/*  Plugin definition                                                         */
/* -------------------------------------------------------------------------- */

const plugin = definePlugin({
  async setup(ctx) {
    ctx.logger.info("Security Audit Gateway plugin setup starting");

    // ── Data handlers (for UI) ───────────────────────────────────────────

    ctx.data.register("quarantine-summary", async () => {
      const items = await getItems(ctx);
      const log = await getAuditLog(ctx);

      const quarantinedCount = items.filter((i) => i.status === "quarantined").length;
      const approvedCount = items.filter((i) => i.status === "approved").length;
      const rejectedCount = items.filter((i) => i.status === "rejected").length;
      const recentLog = log.slice(-3).reverse();

      return {
        quarantinedCount,
        approvedCount,
        rejectedCount,
        totalCount: items.length,
        recentLog,
      };
    });

    ctx.data.register("quarantined-items", async (params) => {
      const items = await getItems(ctx);
      const status = (params.status as string) ?? "all";

      if (status === "all") return { items };
      return { items: items.filter((i) => i.status === status) };
    });

    ctx.data.register("audit-log", async () => {
      const log = await getAuditLog(ctx);
      return { entries: log.slice().reverse() };
    });

    // ── Action handlers (for UI) ─────────────────────────────────────────

    ctx.actions.register("approve-item", async (params) => {
      const itemId = params.itemId as string;
      const reviewedBy = (params.reviewedBy as string) ?? "Board User";
      const note = params.note as string | undefined;

      const items = await getItems(ctx);
      const item = items.find((i) => i.id === itemId);
      if (!item) return { success: false, error: "Item not found" };
      if (item.status !== "quarantined") {
        return { success: false, error: `Item has already been ${item.status}` };
      }

      item.status = "approved";
      item.reviewedAt = new Date().toISOString();
      item.reviewedBy = reviewedBy;
      if (note) item.reviewNote = note;

      await saveItems(ctx, items);

      const logEntry: AuditLogEntry = {
        id: crypto.randomUUID(),
        itemId: item.id,
        itemName: item.name,
        action: "approved",
        performedBy: reviewedBy,
        performedAt: item.reviewedAt,
        note,
      };
      await appendAuditLog(ctx, logEntry);

      const companyId = await firstCompanyId(ctx);
      if (companyId) {
        await ctx.activity.log({
          companyId,
          message: `Security Audit: approved ${item.type} "${item.name}" by ${item.author}`,
          entityType: "plugin",
          entityId: PLUGIN_ID,
          metadata: { itemId: item.id, itemName: item.name, decision: "approved" },
        });
      }

      return { success: true, item };
    });

    ctx.actions.register("reject-item", async (params) => {
      const itemId = params.itemId as string;
      const reviewedBy = (params.reviewedBy as string) ?? "Board User";
      const note = params.note as string | undefined;

      const items = await getItems(ctx);
      const item = items.find((i) => i.id === itemId);
      if (!item) return { success: false, error: "Item not found" };
      if (item.status !== "quarantined") {
        return { success: false, error: `Item has already been ${item.status}` };
      }

      item.status = "rejected";
      item.reviewedAt = new Date().toISOString();
      item.reviewedBy = reviewedBy;
      if (note) item.reviewNote = note;

      await saveItems(ctx, items);

      const logEntry: AuditLogEntry = {
        id: crypto.randomUUID(),
        itemId: item.id,
        itemName: item.name,
        action: "rejected",
        performedBy: reviewedBy,
        performedAt: item.reviewedAt,
        note,
      };
      await appendAuditLog(ctx, logEntry);

      const companyId = await firstCompanyId(ctx);
      if (companyId) {
        await ctx.activity.log({
          companyId,
          message: `Security Audit: rejected ${item.type} "${item.name}" by ${item.author}`,
          entityType: "plugin",
          entityId: PLUGIN_ID,
          metadata: { itemId: item.id, itemName: item.name, decision: "rejected" },
        });
      }

      return { success: true, item };
    });

    // ── Tools ────────────────────────────────────────────────────────────

    ctx.tools.register(
      TOOL_NAMES.auditQuarantine,
      {
        displayName: "Quarantine Item",
        description:
          "Submit a tool, skill, or plugin for quarantine review.",
        parametersSchema: {
          type: "object",
          properties: {
            name: { type: "string" },
            type: { type: "string", enum: ["tool", "skill", "plugin"] },
            source: { type: "string" },
            author: { type: "string" },
            description: { type: "string" },
          },
          required: ["name", "type", "source", "author", "description"],
        },
      },
      async (rawParams: unknown, toolCtx: ToolRunContext): Promise<ToolResult> => {
        const params = rawParams as Record<string, unknown>;
        const name = params.name as string;
        const type = params.type as "tool" | "skill" | "plugin";
        const source = params.source as string;
        const author = params.author as string;
        const description = params.description as string;

        const config = (await ctx.config.get()) as SecurityAuditConfig;
        const autoApprove =
          config.autoApproveFromTrustedAuthors === true &&
          Array.isArray(config.trustedAuthors) &&
          config.trustedAuthors.includes(author);

        const now = new Date().toISOString();
        const newItem: QuarantinedItem = {
          id: crypto.randomUUID(),
          name,
          type,
          source,
          author,
          description,
          status: autoApprove ? "approved" : "quarantined",
          submittedAt: now,
        };

        if (autoApprove) {
          newItem.reviewedAt = now;
          newItem.reviewedBy = "system (trusted author)";
          newItem.reviewNote = "Auto-approved — author is on the trusted list.";
        }

        const items = await getItems(ctx);
        items.push(newItem);
        await saveItems(ctx, items);

        const logEntry: AuditLogEntry = {
          id: crypto.randomUUID(),
          itemId: newItem.id,
          itemName: newItem.name,
          action: autoApprove ? "approved" : "quarantined",
          performedBy: autoApprove ? "system (trusted author)" : "system",
          performedAt: now,
          note: autoApprove
            ? "Auto-approved — author is on the trusted list."
            : undefined,
        };
        await appendAuditLog(ctx, logEntry);

        const companyId = toolCtx.companyId ?? (await firstCompanyId(ctx));
        if (companyId) {
          await ctx.activity.log({
            companyId,
            message: autoApprove
              ? `Security Audit: auto-approved ${type} "${name}" from trusted author "${author}"`
              : `Security Audit: quarantined ${type} "${name}" by "${author}" — pending review`,
            entityType: "plugin",
            entityId: PLUGIN_ID,
            metadata: {
              itemId: newItem.id,
              itemName: name,
              status: newItem.status,
              author,
            },
          });
        }

        return {
          content: autoApprove
            ? `${type} "${name}" was auto-approved (trusted author: ${author}).`
            : `${type} "${name}" has been quarantined and is pending review.`,
          data: { item: newItem },
        };
      },
    );

    ctx.tools.register(
      TOOL_NAMES.auditReview,
      {
        displayName: "Review Quarantined Item",
        description:
          "Approve or reject a quarantined item.",
        parametersSchema: {
          type: "object",
          properties: {
            itemId: { type: "string" },
            decision: { type: "string", enum: ["approved", "rejected"] },
            reviewedBy: { type: "string" },
            note: { type: "string" },
          },
          required: ["itemId", "decision", "reviewedBy"],
        },
      },
      async (rawParams: unknown, toolCtx: ToolRunContext): Promise<ToolResult> => {
        const params = rawParams as Record<string, unknown>;
        const itemId = params.itemId as string;
        const decision = params.decision as "approved" | "rejected";
        const reviewedBy = params.reviewedBy as string;
        const note = params.note as string | undefined;

        const items = await getItems(ctx);
        const item = items.find((i) => i.id === itemId);
        if (!item) {
          return { error: `Quarantined item with ID "${itemId}" not found.` };
        }
        if (item.status !== "quarantined") {
          return {
            error: `Item "${item.name}" has already been ${item.status}. Only quarantined items can be reviewed.`,
          };
        }

        const now = new Date().toISOString();
        item.status = decision;
        item.reviewedAt = now;
        item.reviewedBy = reviewedBy;
        if (note) item.reviewNote = note;

        await saveItems(ctx, items);

        const logEntry: AuditLogEntry = {
          id: crypto.randomUUID(),
          itemId: item.id,
          itemName: item.name,
          action: decision,
          performedBy: reviewedBy,
          performedAt: now,
          note,
        };
        await appendAuditLog(ctx, logEntry);

        const companyId = toolCtx.companyId ?? (await firstCompanyId(ctx));
        if (companyId) {
          await ctx.activity.log({
            companyId,
            message: `Security Audit: ${decision} ${item.type} "${item.name}" — reviewed by ${reviewedBy}`,
            entityType: "plugin",
            entityId: PLUGIN_ID,
            metadata: {
              itemId: item.id,
              itemName: item.name,
              decision,
              reviewedBy,
            },
          });
        }

        return {
          content: `${item.type} "${item.name}" has been ${decision} by ${reviewedBy}.${note ? ` Note: ${note}` : ""}`,
          data: { item },
        };
      },
    );

    ctx.tools.register(
      TOOL_NAMES.auditList,
      {
        displayName: "List Quarantined Items",
        description:
          "List quarantined items, optionally filtered by status.",
        parametersSchema: {
          type: "object",
          properties: {
            status: {
              type: "string",
              enum: ["quarantined", "approved", "rejected", "all"],
            },
          },
        },
      },
      async (rawParams: unknown): Promise<ToolResult> => {
        const params = rawParams as Record<string, unknown>;
        const status = (params.status as string) ?? "quarantined";

        const items = await getItems(ctx);
        const filtered =
          status === "all"
            ? items
            : items.filter((i) => i.status === status);

        if (filtered.length === 0) {
          return {
            content: `No items found with status "${status}".`,
            data: { items: [] },
          };
        }

        const lines = filtered.map(
          (i) =>
            `- [${i.status.toUpperCase()}] ${i.name} (${i.type}) by ${i.author} — submitted ${i.submittedAt.split("T")[0]}`,
        );

        return {
          content: `Found ${filtered.length} item(s):\n${lines.join("\n")}`,
          data: { items: filtered },
        };
      },
    );

    ctx.logger.info("Security Audit Gateway plugin setup complete");
  },

  async onHealth() {
    return { status: "ok", message: "Security Audit Gateway plugin is healthy" };
  },
});

export default plugin;
runWorker(plugin, import.meta.url);
