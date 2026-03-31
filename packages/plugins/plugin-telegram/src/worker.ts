import {
  definePlugin,
  runWorker,
  type PluginContext,
  type PluginWebhookInput,
  type ToolRunContext,
  type ToolResult,
} from "@paperclipai/plugin-sdk";
import {
  PLUGIN_ID,
  STATE_KEYS,
  TOOL_NAMES,
  WEBHOOK_KEYS,
} from "./constants.js";

/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */

type TelegramConfig = {
  botToken: string;
  chatId: string;
  webhookSecret?: string;
  notifyOnRoutineComplete?: boolean;
  notifyOnAgentError?: boolean;
  notifyOnIssueComplete?: boolean;
};

type SentMessage = {
  text: string;
  sentAt: string;
  success: boolean;
};

type BotInfo = {
  ok: boolean;
  id?: number;
  first_name?: string;
  username?: string;
  error?: string;
};

/** Maps Telegram message_id → Paperclip issue context for reply routing. */
type MessageMapEntry = {
  issueId: string;
  companyId: string;
  identifier: string;
  sentAt: string;
};

type MessageMap = Record<string, MessageMapEntry>;

/** Telegram Update object (subset of fields we care about). */
type TelegramUpdate = {
  update_id: number;
  message?: {
    message_id: number;
    from?: { id: number; first_name?: string; username?: string };
    chat: { id: number; type: string };
    text?: string;
    reply_to_message?: {
      message_id: number;
      text?: string;
    };
    date: number;
  };
};

/* -------------------------------------------------------------------------- */
/*  Module-level context (set during setup, used by onWebhook)                */
/* -------------------------------------------------------------------------- */

let currentContext: PluginContext | null = null;

/** Track processed Telegram update IDs to prevent duplicate handling. */
const processedUpdates = new Set<number>();
const MAX_PROCESSED_UPDATES = 500;

/* -------------------------------------------------------------------------- */
/*  Helpers                                                                   */
/* -------------------------------------------------------------------------- */

async function getConfig(ctx: PluginContext): Promise<TelegramConfig | null> {
  const raw = (await ctx.config.get()) as TelegramConfig | null;
  if (!raw?.botToken || !raw?.chatId) return null;
  return raw;
}

async function sendTelegramMessage(
  ctx: PluginContext,
  token: string,
  chatId: string,
  message: string,
  parseMode?: string,
): Promise<{ ok: boolean; result?: { message_id: number }; description?: string }> {
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  const body: Record<string, unknown> = {
    chat_id: chatId,
    text: message,
  };
  if (parseMode) {
    body.parse_mode = parseMode;
  }

  const response = await ctx.http.fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  return (await response.json()) as { ok: boolean; result?: { message_id: number }; description?: string };
}

async function getBotInfo(
  ctx: PluginContext,
  token: string,
): Promise<BotInfo> {
  const url = `https://api.telegram.org/bot${token}/getMe`;

  try {
    const response = await ctx.http.fetch(url, { method: "GET" });
    const data = (await response.json()) as {
      ok: boolean;
      result?: { id: number; first_name: string; username: string };
      description?: string;
    };

    if (data.ok && data.result) {
      return {
        ok: true,
        id: data.result.id,
        first_name: data.result.first_name,
        username: data.result.username,
      };
    }

    return { ok: false, error: data.description ?? "Unknown error from Telegram API" };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}

async function recordSentMessage(
  ctx: PluginContext,
  text: string,
  success: boolean,
): Promise<void> {
  const existing = (await ctx.state.get({
    scopeKind: "instance",
    stateKey: STATE_KEYS.recentMessages,
  })) as { messages: SentMessage[] } | null;

  const messages = existing?.messages ?? [];
  messages.unshift({
    text: text.length > 200 ? text.slice(0, 200) + "..." : text,
    sentAt: new Date().toISOString(),
    success,
  });

  if (messages.length > 5) {
    messages.length = 5;
  }

  await ctx.state.set(
    { scopeKind: "instance", stateKey: STATE_KEYS.recentMessages },
    { messages },
  );
}

/** Load the Telegram message_id → Paperclip issue mapping from state. */
async function loadMessageMap(ctx: PluginContext): Promise<MessageMap> {
  const stored = (await ctx.state.get({
    scopeKind: "instance",
    stateKey: STATE_KEYS.messageMap,
  })) as { map: MessageMap } | null;
  return stored?.map ?? {};
}

/** Save the message map, keeping only the last 200 entries. */
async function saveMessageMap(ctx: PluginContext, map: MessageMap): Promise<void> {
  const entries = Object.entries(map);
  if (entries.length > 200) {
    entries.sort((a, b) => b[1].sentAt.localeCompare(a[1].sentAt));
    const trimmed: MessageMap = {};
    for (const [k, v] of entries.slice(0, 200)) {
      trimmed[k] = v;
    }
    map = trimmed;
  }
  await ctx.state.set(
    { scopeKind: "instance", stateKey: STATE_KEYS.messageMap },
    { map },
  );
}

/** Send a notification and track the Telegram message_id for reply routing. */
async function sendTrackedNotification(
  ctx: PluginContext,
  config: TelegramConfig,
  text: string,
  issueId: string,
  companyId: string,
  identifier: string,
): Promise<void> {
  const result = await sendTelegramMessage(ctx, config.botToken, config.chatId, text);
  await recordSentMessage(ctx, text, result.ok);

  if (result.ok && result.result?.message_id) {
    const map = await loadMessageMap(ctx);
    map[String(result.result.message_id)] = {
      issueId,
      companyId,
      identifier,
      sentAt: new Date().toISOString(),
    };
    await saveMessageMap(ctx, map);
  }
}

/* -------------------------------------------------------------------------- */
/*  Bot command handlers                                                      */
/* -------------------------------------------------------------------------- */

/** Find an issue by its identifier (e.g. SHN-5) across all companies. */
async function findIssueByIdentifier(ctx: PluginContext, identifier: string) {
  const companies = await ctx.companies.list({});
  for (const company of companies) {
    const issues = await ctx.issues.list({ companyId: company.id, limit: 100 });
    const upper = identifier.toUpperCase();
    const match = issues.find((i) => i.identifier?.toUpperCase() === upper);
    if (match) return match;
  }
  return null;
}

async function handleCommand(
  ctx: PluginContext,
  config: TelegramConfig,
  command: string,
  args: string,
): Promise<void> {
  switch (command) {
    case "/status": {
      if (!args.trim()) {
        await sendTelegramMessage(ctx, config.botToken, config.chatId,
          "Usage: /status <issue-id>\nExample: /status SHN-5");
        return;
      }
      const issue = await findIssueByIdentifier(ctx, args.trim());
      if (!issue) {
        await sendTelegramMessage(ctx, config.botToken, config.chatId,
          `Issue ${args.trim()} not found.`);
        return;
      }
      const lines = [
        `${issue.identifier ?? args.trim()}: ${issue.title}`,
        `Status: ${issue.status}`,
        `Priority: ${issue.priority}`,
        issue.assigneeAgentId ? `Assigned to: agent ${issue.assigneeAgentId}` : "Unassigned",
      ];
      await sendTelegramMessage(ctx, config.botToken, config.chatId, lines.join("\n"));
      return;
    }

    case "/issues": {
      try {
        const companies = await ctx.companies.list({});
        const allIssues: string[] = [];
        for (const company of companies) {
          try {
            const issues = await ctx.issues.list({ companyId: company.id, limit: 50 });
            for (const issue of issues) {
              if (issue.status !== "done" && issue.status !== "cancelled") {
                allIssues.push(`${issue.identifier ?? "?"}: ${issue.title} [${issue.status}]`);
              }
            }
          } catch (companyErr) {
            ctx.logger.warn("Failed to list issues for company", { companyId: company.id, error: String(companyErr) });
          }
        }
        if (allIssues.length === 0) {
          await sendTelegramMessage(ctx, config.botToken, config.chatId, "No active issues.");
        } else {
          const text = `Active issues (${allIssues.length}):\n\n` + allIssues.slice(0, 20).join("\n");
          await sendTelegramMessage(ctx, config.botToken, config.chatId, text);
        }
      } catch (err) {
        await sendTelegramMessage(ctx, config.botToken, config.chatId, `Error listing issues: ${String(err)}`);
      }
      return;
    }

    case "/agents": {
      try {
        const companies = await ctx.companies.list({});
        const lines: string[] = [];
        for (const company of companies) {
          try {
            const agents = await ctx.agents.list({ companyId: company.id });
            lines.push(`\n${company.name}:`);
            for (const agent of agents) {
              lines.push(`  ${agent.name} (${agent.title ?? agent.role}) — ${agent.status}`);
            }
          } catch (companyErr) {
            ctx.logger.warn("Failed to list agents for company", { companyId: company.id, error: String(companyErr) });
          }
        }
        await sendTelegramMessage(ctx, config.botToken, config.chatId,
          lines.length > 0 ? lines.join("\n") : "No agents found.");
      } catch (err) {
        await sendTelegramMessage(ctx, config.botToken, config.chatId, `Error listing agents: ${String(err)}`);
      }
      return;
    }

    case "/approve": {
      if (!args.trim()) {
        await sendTelegramMessage(ctx, config.botToken, config.chatId,
          "Usage: /approve <issue-id>\nExample: /approve SHN-5");
        return;
      }
      const issue = await findIssueByIdentifier(ctx, args.trim());
      if (!issue) {
        await sendTelegramMessage(ctx, config.botToken, config.chatId,
          `Issue ${args.trim()} not found.`);
        return;
      }
      try {
        await ctx.issues.update(issue.id, { status: "done" }, issue.companyId);
        await sendTelegramMessage(ctx, config.botToken, config.chatId,
          `Approved and closed: ${issue.identifier ?? args.trim()}`);
      } catch (err) {
        await sendTelegramMessage(ctx, config.botToken, config.chatId,
          `Failed to approve ${args.trim()}: ${String(err)}`);
      }
      return;
    }

    case "/help": {
      await sendTelegramMessage(ctx, config.botToken, config.chatId, [
        "Paperclip Bot Commands:",
        "",
        "/status <issue-id> — Check issue status",
        "/issues — List active issues",
        "/agents — List all agents and their status",
        "/approve <issue-id> — Mark issue as done",
        "/help — Show this message",
        "",
        "Reply to any notification to add a comment to that issue.",
      ].join("\n"));
      return;
    }

    default: {
      await sendTelegramMessage(ctx, config.botToken, config.chatId,
        `Unknown command: ${command}\nType /help for available commands.`);
    }
  }
}

/* -------------------------------------------------------------------------- */
/*  Plugin definition                                                         */
/* -------------------------------------------------------------------------- */

const plugin = definePlugin({
  async setup(ctx) {
    ctx.logger.info("Telegram plugin v0.2.0 setup starting (two-way)");
    currentContext = ctx;

    // ── Event subscriptions ──────────────────────────────────────────────
    ctx.events.on("issue.updated", async (event) => {
      const config = await getConfig(ctx);
      if (!config) return;
      if (config.notifyOnIssueComplete === false) return;

      const payload = event.payload as Record<string, unknown>;
      if (payload.status === "done" || payload.status === "completed") {
        const identifier = (payload.identifier as string) ?? "";
        const issueTitle =
          (payload.title as string) ??
          identifier ??
          event.entityId ??
          "Unknown issue";

        const message = `Issue completed: ${identifier ? identifier + " — " : ""}${issueTitle}`;

        try {
          await sendTrackedNotification(
            ctx,
            config,
            message,
            event.entityId ?? "",
            (payload.companyId as string) ?? "",
            identifier,
          );

          if (event.entityId) {
            await ctx.activity.log({
              companyId: (payload.companyId as string) ?? "",
              message: `Telegram: sent issue completion notification for ${issueTitle}`,
              entityType: "issue",
              entityId: event.entityId,
              metadata: { telegramOk: true },
            });
          }
        } catch (err) {
          ctx.logger.warn("Failed to send Telegram issue notification", {
            error: String(err),
          });
          await recordSentMessage(ctx, message, false);
        }
      }
    });

    ctx.events.on("agent.run.failed", async (event) => {
      const config = await getConfig(ctx);
      if (!config) return;
      if (config.notifyOnAgentError === false) return;

      const payload = event.payload as Record<string, unknown>;
      const agentName =
        (payload.agentName as string) ??
        (payload.name as string) ??
        event.entityId ??
        "Unknown agent";
      const reason = (payload.reason as string) ?? (payload.error as string) ?? "No reason provided";

      const message = `Agent run failed: ${agentName}\nReason: ${reason}`;

      try {
        const result = await sendTelegramMessage(
          ctx,
          config.botToken,
          config.chatId,
          message,
        );
        await recordSentMessage(ctx, message, result.ok);

        if (event.entityId) {
          await ctx.activity.log({
            companyId: (payload.companyId as string) ?? "",
            message: `Telegram: sent agent run-failed notification for ${agentName}`,
            entityType: "agent",
            entityId: event.entityId,
            metadata: { telegramOk: result.ok, reason },
          });
        }
      } catch (err) {
        ctx.logger.warn("Failed to send Telegram agent-run-failed notification", {
          error: String(err),
        });
        await recordSentMessage(ctx, message, false);
      }
    });

    // ── Data handlers (for UI) ───────────────────────────────────────────
    ctx.data.register("bot-status", async (_params) => {
      const config = await getConfig(ctx);
      if (!config) {
        return { connected: false, error: "Bot token or chat ID not configured" };
      }

      const info = await getBotInfo(ctx, config.botToken);
      if (info.ok) {
        return {
          connected: true,
          botId: info.id,
          botName: info.first_name,
          botUsername: info.username,
        };
      }

      return { connected: false, error: info.error ?? "Could not reach Telegram API" };
    });

    ctx.data.register("recent-messages", async (_params) => {
      const stored = (await ctx.state.get({
        scopeKind: "instance",
        stateKey: STATE_KEYS.recentMessages,
      })) as { messages: SentMessage[] } | null;

      return { messages: stored?.messages ?? [] };
    });

    // ── Action handlers (for UI) ─────────────────────────────────────────
    ctx.actions.register("send-test", async (_params) => {
      const config = await getConfig(ctx);
      if (!config) {
        return { success: false, error: "Bot token or chat ID not configured" };
      }

      const message = `Paperclip test message — ${new Date().toISOString()}`;

      try {
        const result = await sendTelegramMessage(
          ctx,
          config.botToken,
          config.chatId,
          message,
        );
        await recordSentMessage(ctx, message, result.ok);

        if (result.ok) {
          return { success: true, message: "Test message sent successfully" };
        }
        return {
          success: false,
          error: result.description ?? "Telegram API returned an error",
        };
      } catch (err) {
        await recordSentMessage(ctx, message, false);
        return { success: false, error: String(err) };
      }
    });

    // ── Tools ────────────────────────────────────────────────────────────
    ctx.tools.register(
      TOOL_NAMES.telegramSend,
      {
        displayName: "Send Telegram Message",
        description: "Send a message to the configured Telegram chat via the Bot API.",
        parametersSchema: {
          type: "object",
          properties: {
            message: { type: "string" },
            parseMode: { type: "string", enum: ["HTML", "Markdown"] },
          },
          required: ["message"],
        },
      },
      async (rawParams: unknown, toolCtx: ToolRunContext): Promise<ToolResult> => {
        const params = rawParams as Record<string, unknown>;
        const messageText = params.message as string;
        const parseMode = params.parseMode as string | undefined;

        if (!messageText || messageText.trim().length === 0) {
          return { error: "Message text is required and must not be empty" };
        }

        const config = await getConfig(ctx);
        if (!config) {
          return { error: "Telegram bot token or chat ID not configured. Please configure the plugin instance first." };
        }

        try {
          const result = await sendTelegramMessage(
            ctx,
            config.botToken,
            config.chatId,
            messageText,
            parseMode,
          );
          await recordSentMessage(ctx, messageText, result.ok);

          await ctx.activity.log({
            companyId: toolCtx.companyId,
            message: `Telegram: agent sent message via telegram_send tool`,
            entityType: "agent",
            entityId: toolCtx.agentId,
            metadata: { telegramOk: result.ok, messageLength: messageText.length },
          });

          if (result.ok) {
            return { content: "Message sent to Telegram successfully." };
          }
          return {
            error: `Telegram API error: ${result.description ?? "unknown error"}`,
          };
        } catch (err) {
          await recordSentMessage(ctx, messageText, false);
          return { error: `Failed to send Telegram message: ${String(err)}` };
        }
      },
    );

    ctx.tools.register(
      TOOL_NAMES.telegramStatus,
      {
        displayName: "Telegram Bot Status",
        description: "Check the Telegram bot connection status by calling the getMe endpoint.",
        parametersSchema: {
          type: "object",
          properties: {},
        },
      },
      async (_rawParams: unknown, _toolCtx: ToolRunContext): Promise<ToolResult> => {
        const config = await getConfig(ctx);
        if (!config) {
          return { error: "Telegram bot token not configured. Please configure the plugin instance first." };
        }

        const info = await getBotInfo(ctx, config.botToken);

        if (info.ok) {
          return {
            content: [
              `Telegram bot is connected.`,
              `  Name: ${info.first_name}`,
              `  Username: @${info.username}`,
              `  Bot ID: ${info.id}`,
            ].join("\n"),
            data: {
              connected: true,
              botId: info.id,
              botName: info.first_name,
              botUsername: info.username,
            },
          };
        }

        return {
          error: `Telegram bot is not reachable: ${info.error}`,
        };
      },
    );

    ctx.logger.info("Telegram plugin v0.2.0 setup complete (two-way enabled)");
  },

  // ── Webhook handler (inbound Telegram messages) ─────────────────────────
  async onWebhook(input: PluginWebhookInput) {
    const ctx = currentContext;
    if (!ctx) {
      throw new Error("Telegram plugin not initialised — onWebhook called before setup");
    }

    if (input.endpointKey !== WEBHOOK_KEYS.telegramUpdate) {
      throw new Error(`Unsupported webhook endpoint: "${input.endpointKey}"`);
    }

    const config = await getConfig(ctx);
    if (!config) {
      ctx.logger.warn("Telegram webhook received but plugin not configured");
      return;
    }

    // ── Verify Telegram secret token ────────────────────────────────
    if (config.webhookSecret) {
      const headerSecret = input.headers?.["x-telegram-bot-api-secret-token"];
      if (headerSecret !== config.webhookSecret) {
        ctx.logger.warn("Telegram webhook rejected: invalid secret token");
        return;
      }
    }

    const update = input.parsedBody as TelegramUpdate | null;
    if (!update?.message?.text) {
      return; // Ignore non-text updates (photos, stickers, etc.)
    }

    // ── Deduplicate: skip already-processed updates ─────────────────
    if (processedUpdates.has(update.update_id)) {
      return;
    }
    processedUpdates.add(update.update_id);
    if (processedUpdates.size > MAX_PROCESSED_UPDATES) {
      const oldest = processedUpdates.values().next().value!;
      processedUpdates.delete(oldest);
    }

    const msg = update.message;
    const chatId = String(msg.chat.id);

    // Only process messages from the configured chat
    if (chatId !== config.chatId) {
      ctx.logger.warn("Telegram update from unexpected chat", { chatId, expectedChatId: config.chatId });
      return;
    }

    const text = msg.text!.trim();

    // ── Bot commands ──────────────────────────────────────────────────
    if (text.startsWith("/")) {
      const spaceIdx = text.indexOf(" ");
      const command = spaceIdx === -1 ? text.toLowerCase() : text.slice(0, spaceIdx).toLowerCase();
      // Strip @botname from command (e.g. /status@ClawdyPaperclipBot)
      const cleanCommand = command.split("@")[0];
      const args = spaceIdx === -1 ? "" : text.slice(spaceIdx + 1);

      await handleCommand(ctx, config, cleanCommand, args);

      await ctx.activity.log({
        companyId: "",
        message: `Telegram: received bot command ${cleanCommand}`,
        entityType: "plugin",
        entityId: PLUGIN_ID,
        metadata: { command: cleanCommand, from: msg.from?.username ?? "unknown" },
      });
      return;
    }

    // ── Reply-to-notification routing ─────────────────────────────────
    if (msg.reply_to_message) {
      const replyToId = String(msg.reply_to_message.message_id);
      const map = await loadMessageMap(ctx);
      const entry = map[replyToId];

      if (entry) {
        try {
          await ctx.issues.createComment(entry.issueId, text, entry.companyId);

          await sendTelegramMessage(ctx, config.botToken, config.chatId,
            `Comment added to ${entry.identifier}`);

          await ctx.activity.log({
            companyId: entry.companyId,
            message: `Telegram: reply routed as comment on ${entry.identifier}`,
            entityType: "issue",
            entityId: entry.issueId,
            metadata: { from: msg.from?.username ?? "unknown" },
          });
        } catch (err) {
          ctx.logger.warn("Failed to route Telegram reply as issue comment", {
            error: String(err),
            issueId: entry.issueId,
          });
          await sendTelegramMessage(ctx, config.botToken, config.chatId,
            `Failed to add comment to ${entry.identifier}: ${String(err)}`);
        }
      } else {
        // Reply to a message we don't have mapped — could be old or from before tracking started
        await sendTelegramMessage(ctx, config.botToken, config.chatId,
          "Could not find the issue for that notification. Try using /status <issue-id> instead.");
      }
      return;
    }

    // ── Plain messages (not commands, not replies) ────────────────────
    // Just acknowledge — we don't process free-form messages
    await sendTelegramMessage(ctx, config.botToken, config.chatId,
      "Use /help to see available commands, or reply to a notification to add a comment.");
  },

  async onHealth() {
    return { status: "ok", message: "Telegram plugin is healthy" };
  },
});

export default plugin;
runWorker(plugin, import.meta.url);
