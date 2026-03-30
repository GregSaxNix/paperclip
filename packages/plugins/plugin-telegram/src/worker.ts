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

type TelegramConfig = {
  botToken: string;
  chatId: string;
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
): Promise<{ ok: boolean; description?: string }> {
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

  const result = (await response.json()) as { ok: boolean; description?: string };
  return result;
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

  // Keep only the last 5 messages
  if (messages.length > 5) {
    messages.length = 5;
  }

  await ctx.state.set(
    { scopeKind: "instance", stateKey: STATE_KEYS.recentMessages },
    { messages },
  );
}

/* -------------------------------------------------------------------------- */
/*  Plugin definition                                                         */
/* -------------------------------------------------------------------------- */

const plugin = definePlugin({
  async setup(ctx) {
    ctx.logger.info("Telegram plugin setup starting");

    // ── Event subscriptions ──────────────────────────────────────────────
    ctx.events.on("issue.updated", async (event) => {
      const config = await getConfig(ctx);
      if (!config) return;
      if (config.notifyOnIssueComplete === false) return;

      const payload = event.payload as Record<string, unknown>;
      if (payload.status === "done" || payload.status === "completed") {
        const issueTitle =
          (payload.title as string) ??
          (payload.identifier as string) ??
          event.entityId ??
          "Unknown issue";

        const message = `Issue completed: ${issueTitle}`;

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
              message: `Telegram: sent issue completion notification for ${issueTitle}`,
              entityType: "issue",
              entityId: event.entityId,
              metadata: { telegramOk: result.ok },
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

    ctx.logger.info("Telegram plugin setup complete");
  },

  async onHealth() {
    return { status: "ok", message: "Telegram plugin is healthy" };
  },
});

export default plugin;
runWorker(plugin, import.meta.url);
