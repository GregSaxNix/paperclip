import { promises as fs } from "node:fs";
import path from "node:path";
import {
  definePlugin,
  runWorker,
  type PluginContext,
  type ToolRunContext,
  type ToolResult,
} from "@paperclipai/plugin-sdk";
import {
  JOB_KEYS,
  PLUGIN_ID,
  STATE_KEYS,
  TOOL_NAMES,
} from "./constants.js";

/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */

type MemoryEngineConfig = {
  agentHomePath?: string;
  consolidationSchedule?: string;
};

type MemoryStats = {
  dailyNoteCount: number;
  knowledgeGraphEntityCount: number;
  memoryMdSizeBytes: number;
  memoryMdLines: number;
  lastUpdated: string;
};

type SearchResult = {
  file: string;
  line: number;
  text: string;
  score: number;
};

type ExtractedFact = {
  content: string;
  source: string;
  extractedAt: string;
  category: string;
};

/* -------------------------------------------------------------------------- */
/*  Helpers                                                                   */
/* -------------------------------------------------------------------------- */

async function resolveAgentHome(
  ctx: PluginContext,
  agentId: string,
  companyId: string,
): Promise<string | null> {
  const config = (await ctx.config.get()) as MemoryEngineConfig;
  if (config.agentHomePath) return config.agentHomePath;

  try {
    const agent = await ctx.agents.get(agentId, companyId);
    if (!agent) return null;
    const adapterConfig = agent.adapterConfig as Record<string, unknown>;
    const instructionsRootPath = adapterConfig.instructionsRootPath as string | undefined;
    if (instructionsRootPath) return instructionsRootPath;
  } catch {
    // Fall through
  }
  return null;
}

async function readFileIfExists(filePath: string): Promise<string | null> {
  try {
    return await fs.readFile(filePath, "utf-8");
  } catch {
    return null;
  }
}

async function listMarkdownFiles(dirPath: string): Promise<string[]> {
  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true });
    return entries
      .filter((e) => e.isFile() && e.name.endsWith(".md"))
      .map((e) => path.join(dirPath, e.name))
      .sort();
  } catch {
    return [];
  }
}

async function listDirectories(dirPath: string): Promise<string[]> {
  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true });
    return entries
      .filter((e) => e.isDirectory())
      .map((e) => path.join(dirPath, e.name));
  } catch {
    return [];
  }
}

function searchInContent(
  content: string,
  filePath: string,
  queryTerms: string[],
  maxResults: number,
): SearchResult[] {
  const lines = content.split("\n");
  const results: SearchResult[] = [];

  for (let i = 0; i < lines.length && results.length < maxResults; i++) {
    const line = lines[i]!;
    const lowerLine = line.toLowerCase();
    const matchCount = queryTerms.filter((t) => lowerLine.includes(t)).length;
    if (matchCount > 0) {
      const contextStart = Math.max(0, i - 1);
      const contextEnd = Math.min(lines.length - 1, i + 1);
      const contextLines = lines.slice(contextStart, contextEnd + 1).join("\n");
      results.push({
        file: filePath,
        line: i + 1,
        text: contextLines,
        score: matchCount / queryTerms.length,
      });
    }
  }
  return results;
}

async function collectStats(agentHome: string): Promise<MemoryStats> {
  const memoryDir = path.join(agentHome, "memory");
  const lifeDir = path.join(agentHome, "life");
  const memoryMdPath = path.join(agentHome, "MEMORY.md");

  const dailyNotes = await listMarkdownFiles(memoryDir);

  let entityCount = 0;
  const paraCategories = ["projects", "areas", "resources", "archives"];
  for (const category of paraCategories) {
    const categoryPath = path.join(lifeDir, category);
    const dirs = await listDirectories(categoryPath);
    entityCount += dirs.length;
    if (category === "areas") {
      for (const subDir of dirs) {
        const subDirs = await listDirectories(subDir);
        entityCount += subDirs.length;
      }
    }
  }

  let memoryMdSizeBytes = 0;
  let memoryMdLines = 0;
  const memoryContent = await readFileIfExists(memoryMdPath);
  if (memoryContent) {
    memoryMdSizeBytes = Buffer.byteLength(memoryContent, "utf-8");
    memoryMdLines = memoryContent.split("\n").length;
  }

  return {
    dailyNoteCount: dailyNotes.length,
    knowledgeGraphEntityCount: entityCount,
    memoryMdSizeBytes,
    memoryMdLines,
    lastUpdated: new Date().toISOString(),
  };
}

/** Find the first company visible to this plugin. */
async function firstCompanyId(ctx: PluginContext): Promise<string | null> {
  const companies = await ctx.companies.list();
  return companies[0]?.id ?? null;
}

/** Find the first agent for a company. */
async function firstAgentId(ctx: PluginContext, companyId: string): Promise<string | null> {
  const agents = await ctx.agents.list({ companyId });
  return agents[0]?.id ?? null;
}

/* -------------------------------------------------------------------------- */
/*  Flush logic                                                               */
/* -------------------------------------------------------------------------- */

async function performFlush(
  ctx: PluginContext,
  agentHome: string,
  agentId: string,
  companyId: string,
  daysBack: number,
): Promise<{ success: boolean; message: string; entriesPromoted: number }> {
  const memoryDir = path.join(agentHome, "memory");
  const memoryMdPath = path.join(agentHome, "MEMORY.md");

  const now = new Date();
  const cutoff = new Date(now.getTime() - daysBack * 24 * 60 * 60 * 1000);
  const allNotes = await listMarkdownFiles(memoryDir);
  const recentNotes = allNotes.filter((notePath) => {
    const basename = path.basename(notePath, ".md");
    const noteDate = new Date(basename);
    return !isNaN(noteDate.getTime()) && noteDate >= cutoff;
  });

  if (recentNotes.length === 0) {
    return {
      success: true,
      message: `No daily notes found in the last ${daysBack} days.`,
      entriesPromoted: 0,
    };
  }

  const keyEntries: string[] = [];
  for (const notePath of recentNotes) {
    const content = await readFileIfExists(notePath);
    if (!content) continue;
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      if (
        (trimmed.startsWith("- ") || trimmed.startsWith("* ")) &&
        trimmed.length > 30 &&
        /\b(learn|decid|prefer|important|remember|note|realise|discover|confirm|update|change|fix|bug|feature|deploy|migrat)\w*/i.test(trimmed)
      ) {
        keyEntries.push(trimmed);
      }
    }
  }

  if (keyEntries.length === 0) {
    return {
      success: true,
      message: `Reviewed ${recentNotes.length} daily note(s) — no key entries to promote.`,
      entriesPromoted: 0,
    };
  }

  let existingMemory = (await readFileIfExists(memoryMdPath)) ?? "";
  const dateStr = now.toISOString().split("T")[0];
  const newSection = [
    "",
    `## Promoted from daily notes (${dateStr})`,
    "",
    ...keyEntries,
    "",
  ].join("\n");

  existingMemory += newSection;
  await fs.writeFile(memoryMdPath, existingMemory, "utf-8");

  await ctx.activity.log({
    companyId,
    message: `Memory Engine: promoted ${keyEntries.length} entries from ${recentNotes.length} daily note(s) to MEMORY.md`,
    entityType: "agent",
    entityId: agentId,
    metadata: {
      entriesPromoted: keyEntries.length,
      daysReviewed: daysBack,
      notesReviewed: recentNotes.length,
    },
  });

  return {
    success: true,
    message: `Promoted ${keyEntries.length} entries from ${recentNotes.length} daily note(s) to MEMORY.md.`,
    entriesPromoted: keyEntries.length,
  };
}

/* -------------------------------------------------------------------------- */
/*  Plugin definition                                                         */
/* -------------------------------------------------------------------------- */

const plugin = definePlugin({
  async setup(ctx) {
    ctx.logger.info("Memory Engine plugin setup starting");

    // ── Event subscriptions ──────────────────────────────────────────────
    ctx.events.on("issue.updated", async (event) => {
      const payload = event.payload as Record<string, unknown>;
      // Check if issue was completed
      if (payload.status === "done" || payload.status === "completed") {
        ctx.logger.info("Issue completed — facts available for extraction", {
          issueId: event.entityId,
        });
        if (event.entityId) {
          const pendingKey = `pending-extraction:${event.entityId}`;
          await ctx.state.set(
            { scopeKind: "instance", stateKey: pendingKey },
            { issueId: event.entityId, completedAt: new Date().toISOString() },
          );
        }
      }
    });

    // ── Data handlers (for UI) ───────────────────────────────────────────
    ctx.data.register("memory-stats", async (params) => {
      let companyId = params.companyId as string | undefined;
      let agentId = params.agentId as string | undefined;

      if (!companyId) companyId = (await firstCompanyId(ctx)) ?? undefined;
      if (!companyId) return { error: "No company found" };
      if (!agentId) agentId = (await firstAgentId(ctx, companyId)) ?? undefined;
      if (!agentId) return { error: "No agents found" };

      const agentHome = await resolveAgentHome(ctx, agentId, companyId);
      if (!agentHome) return { error: "Could not resolve agent home path" };
      return await collectStats(agentHome);
    });

    ctx.data.register("recent-facts", async (params) => {
      const agentId = params.agentId as string;
      if (!agentId) return { facts: [] };
      const stored = await ctx.state.get({
        scopeKind: "agent",
        scopeId: agentId,
        stateKey: STATE_KEYS.factIndex,
      });
      return stored ?? { facts: [] };
    });

    // ── Action handlers (for UI) ─────────────────────────────────────────
    ctx.actions.register("trigger-flush", async (params) => {
      let companyId = params.companyId as string | undefined;
      let agentId = params.agentId as string | undefined;

      if (!companyId) companyId = (await firstCompanyId(ctx)) ?? undefined;
      if (!companyId) return { success: false, error: "No company found" };
      if (!agentId) agentId = (await firstAgentId(ctx, companyId)) ?? undefined;
      if (!agentId) return { success: false, error: "No agents found" };

      const agentHome = await resolveAgentHome(ctx, agentId, companyId);
      if (!agentHome) return { success: false, error: "Could not resolve agent home" };
      return await performFlush(ctx, agentHome, agentId, companyId, 7);
    });

    // ── Tools ────────────────────────────────────────────────────────────
    ctx.tools.register(
      TOOL_NAMES.memorySearch,
      {
        displayName: "Memory Search",
        description: "Full-text search across memory files.",
        parametersSchema: {
          type: "object",
          properties: {
            query: { type: "string" },
            scope: { type: "string", enum: ["all", "daily_notes", "knowledge_graph", "tacit"] },
            limit: { type: "number" },
          },
          required: ["query"],
        },
      },
      async (rawParams: unknown, toolCtx: ToolRunContext): Promise<ToolResult> => {
        const params = rawParams as Record<string, unknown>;
        const query = params.query as string;
        const scope = (params.scope as string) ?? "all";
        const limit = (params.limit as number) ?? 10;

        const agentHome = await resolveAgentHome(ctx, toolCtx.agentId, toolCtx.companyId);
        if (!agentHome) return { error: "Could not resolve agent home path" };

        const queryTerms = query.toLowerCase().split(/\s+/).filter((t) => t.length > 1);
        if (queryTerms.length === 0) return { error: "Query too short" };

        const allResults: SearchResult[] = [];

        if (scope === "all" || scope === "daily_notes") {
          const notes = await listMarkdownFiles(path.join(agentHome, "memory"));
          for (const note of notes) {
            const content = await readFileIfExists(note);
            if (content) allResults.push(...searchInContent(content, note, queryTerms, limit));
          }
        }

        if (scope === "all" || scope === "tacit") {
          const content = await readFileIfExists(path.join(agentHome, "MEMORY.md"));
          if (content) allResults.push(...searchInContent(content, path.join(agentHome, "MEMORY.md"), queryTerms, limit));
        }

        if (scope === "all" || scope === "knowledge_graph") {
          const lifeDir = path.join(agentHome, "life");
          for (const category of ["projects", "areas", "resources", "archives"]) {
            const entityDirs = await listDirectories(path.join(lifeDir, category));
            for (const entityDir of entityDirs) {
              const content = await readFileIfExists(path.join(entityDir, "summary.md"));
              if (content) allResults.push(...searchInContent(content, path.join(entityDir, "summary.md"), queryTerms, limit));
            }
          }
        }

        allResults.sort((a, b) => b.score - a.score);
        const topResults = allResults.slice(0, limit);

        if (topResults.length === 0) {
          return { content: `No results found for "${query}" in ${scope} scope.` };
        }

        const formatted = topResults
          .map((r) => `**${path.basename(r.file)}** (line ${r.line}, score: ${(r.score * 100).toFixed(0)}%)\n${r.text}`)
          .join("\n\n---\n\n");

        return {
          content: `Found ${topResults.length} result(s) for "${query}":\n\n${formatted}`,
          data: { results: topResults },
        };
      },
    );

    ctx.tools.register(
      TOOL_NAMES.memoryExtractFacts,
      {
        displayName: "Extract Facts from Issue",
        description: "Extract durable facts from a completed issue thread and store them.",
        parametersSchema: {
          type: "object",
          properties: {
            issueId: { type: "string" },
            agentId: { type: "string" },
          },
          required: ["issueId", "agentId"],
        },
      },
      async (rawParams: unknown, toolCtx: ToolRunContext): Promise<ToolResult> => {
        const params = rawParams as Record<string, unknown>;
        const issueId = params.issueId as string;
        const agentId = params.agentId as string;

        const issue = await ctx.issues.get(issueId, toolCtx.companyId);
        if (!issue) return { error: `Could not find issue ${issueId}` };

        let comments: Array<{ body?: string | null }> = [];
        try {
          comments = await ctx.issues.listComments(issueId, toolCtx.companyId);
        } catch {
          // Comments may not be available
        }

        const threadParts: string[] = [`# ${issue.title}`];
        if (issue.description) threadParts.push(issue.description);
        for (const comment of comments) {
          if (comment.body) threadParts.push(comment.body);
        }
        const fullThread = threadParts.join("\n\n");

        const facts: ExtractedFact[] = [];
        for (const line of fullThread.split("\n")) {
          const trimmed = line.trim();
          if (
            (trimmed.startsWith("- ") || trimmed.startsWith("* ") || /^[A-Z].*:/.test(trimmed)) &&
            trimmed.length > 20 &&
            trimmed.length < 500
          ) {
            facts.push({
              content: trimmed.replace(/^[-*]\s+/, ""),
              source: `issue:${issue.identifier ?? issueId}`,
              extractedAt: new Date().toISOString(),
              category: "issue-extraction",
            });
          }
        }

        const existingFacts =
          ((await ctx.state.get({
            scopeKind: "agent",
            scopeId: agentId,
            stateKey: STATE_KEYS.factIndex,
          })) as { facts: ExtractedFact[] } | null) ?? { facts: [] };

        existingFacts.facts.push(...facts);
        await ctx.state.set(
          { scopeKind: "agent", scopeId: agentId, stateKey: STATE_KEYS.factIndex },
          existingFacts,
        );

        await ctx.state.delete({
          scopeKind: "instance",
          stateKey: `pending-extraction:${issueId}`,
        });

        await ctx.activity.log({
          companyId: issue.companyId,
          message: `Memory Engine: extracted ${facts.length} fact(s) from ${issue.identifier ?? issueId}`,
          entityType: "issue",
          entityId: issueId,
          metadata: { factCount: facts.length, issueIdentifier: issue.identifier },
        });

        return {
          content: `Extracted ${facts.length} fact(s) from ${issue.identifier ?? issueId}.`,
          data: { factCount: facts.length, facts },
        };
      },
    );

    ctx.tools.register(
      TOOL_NAMES.memoryFlush,
      {
        displayName: "Flush to MEMORY.md",
        description: "Promote daily note entries to long-term MEMORY.md.",
        parametersSchema: {
          type: "object",
          properties: {
            agentId: { type: "string" },
            daysBack: { type: "number" },
          },
          required: ["agentId"],
        },
      },
      async (rawParams: unknown, toolCtx: ToolRunContext): Promise<ToolResult> => {
        const params = rawParams as Record<string, unknown>;
        const agentId = params.agentId as string;
        const daysBack = (params.daysBack as number) ?? 7;

        const agentHome = await resolveAgentHome(ctx, agentId, toolCtx.companyId);
        if (!agentHome) return { error: "Could not resolve agent home path" };

        const result = await performFlush(ctx, agentHome, agentId, toolCtx.companyId, daysBack);
        return { content: result.message, data: result };
      },
    );

    ctx.tools.register(
      TOOL_NAMES.memoryStats,
      {
        displayName: "Memory Statistics",
        description: "Returns statistics about an agent's memory files.",
        parametersSchema: {
          type: "object",
          properties: { agentId: { type: "string" } },
          required: ["agentId"],
        },
      },
      async (rawParams: unknown, toolCtx: ToolRunContext): Promise<ToolResult> => {
        const params = rawParams as Record<string, unknown>;
        const agentId = params.agentId as string;

        const agentHome = await resolveAgentHome(ctx, agentId, toolCtx.companyId);
        if (!agentHome) return { error: "Could not resolve agent home path" };

        const stats = await collectStats(agentHome);
        await ctx.state.set(
          { scopeKind: "agent", scopeId: agentId, stateKey: STATE_KEYS.memoryStats },
          stats,
        );

        return {
          content: [
            `Memory stats for agent:`,
            `  Daily notes: ${stats.dailyNoteCount}`,
            `  Knowledge graph entities: ${stats.knowledgeGraphEntityCount}`,
            `  MEMORY.md: ${stats.memoryMdLines} lines (${(stats.memoryMdSizeBytes / 1024).toFixed(1)} KB)`,
          ].join("\n"),
          data: stats,
        };
      },
    );

    // ── Jobs ─────────────────────────────────────────────────────────────
    ctx.jobs.register(JOB_KEYS.dailyConsolidation, async (job) => {
      ctx.logger.info("Starting daily memory consolidation", {
        runId: job.runId,
        trigger: job.trigger,
      });

      const companyId = await firstCompanyId(ctx);
      if (!companyId) {
        ctx.logger.warn("No company found for consolidation");
        return;
      }

      const agents = await ctx.agents.list({ companyId });
      for (const agent of agents) {
        const agentHome = await resolveAgentHome(ctx, agent.id, companyId);
        if (!agentHome) continue;

        try {
          const stats = await collectStats(agentHome);
          await ctx.state.set(
            { scopeKind: "agent", scopeId: agent.id, stateKey: STATE_KEYS.memoryStats },
            stats,
          );
          ctx.logger.info("Memory stats updated for agent", {
            agentId: agent.id,
            agentName: agent.name,
            dailyNotes: stats.dailyNoteCount,
            entities: stats.knowledgeGraphEntityCount,
          });
        } catch (err) {
          ctx.logger.warn("Failed to consolidate memory for agent", {
            agentId: agent.id,
            error: String(err),
          });
        }
      }

      await ctx.state.set(
        { scopeKind: "instance", stateKey: STATE_KEYS.consolidationLog },
        {
          lastRun: new Date().toISOString(),
          agentsProcessed: agents.length,
          trigger: job.trigger,
        },
      );

      ctx.logger.info("Daily memory consolidation complete");
    });

    ctx.logger.info("Memory Engine plugin setup complete");
  },

  async onHealth() {
    return { status: "ok", message: "Memory Engine plugin is healthy" };
  },
});

export default plugin;
runWorker(plugin, import.meta.url);
