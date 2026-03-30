import { useState } from "react";
import {
  usePluginData,
  usePluginAction,
  type PluginWidgetProps,
} from "@paperclipai/plugin-sdk/ui";

/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */

type BotStatusData = {
  connected: boolean;
  botId?: number;
  botName?: string;
  botUsername?: string;
  error?: string;
};

type SentMessage = {
  text: string;
  sentAt: string;
  success: boolean;
};

type RecentMessagesData = {
  messages: SentMessage[];
};

/* -------------------------------------------------------------------------- */
/*  Dashboard Widget                                                          */
/* -------------------------------------------------------------------------- */

export function TelegramDashboardWidget({ context }: PluginWidgetProps) {
  const [sending, setSending] = useState(false);
  const [sendResult, setSendResult] = useState<string | null>(null);

  const { data: botStatus, loading: statusLoading } =
    usePluginData<BotStatusData>("bot-status", {});

  const { data: recentData, loading: messagesLoading } =
    usePluginData<RecentMessagesData>("recent-messages", {});

  const sendTest = usePluginAction("send-test");

  const handleSendTest = async () => {
    setSending(true);
    setSendResult(null);
    try {
      const result = await sendTest({});
      if (result && typeof result === "object" && "message" in result) {
        setSendResult(String((result as { message: string }).message));
      } else if (result && typeof result === "object" && "error" in result) {
        setSendResult(String((result as { error: string }).error));
      }
    } catch {
      setSendResult("Failed to send test message");
    } finally {
      setSending(false);
    }
  };

  const recentMessages = recentData?.messages ?? [];

  return (
    <section
      aria-label="Telegram"
      style={{
        padding: "1rem",
        display: "flex",
        flexDirection: "column",
        gap: "0.75rem",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <strong style={{ fontSize: "0.875rem" }}>Telegram</strong>
        <button
          type="button"
          onClick={handleSendTest}
          disabled={sending}
          style={{
            fontSize: "0.75rem",
            padding: "0.25rem 0.5rem",
            borderRadius: "4px",
            border: "1px solid var(--border)",
            background: "var(--primary)",
            color: "var(--primary-foreground)",
            cursor: sending ? "wait" : "pointer",
            opacity: sending ? 0.6 : 1,
          }}
        >
          {sending ? "Sending..." : "Send Test Message"}
        </button>
      </div>

      {/* Send result feedback */}
      {sendResult && (
        <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
          {sendResult}
        </div>
      )}

      {/* Bot status */}
      {statusLoading && (
        <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
          Checking bot status...
        </div>
      )}

      {botStatus && (
        <div
          style={{
            padding: "0.5rem",
            borderRadius: "4px",
            border: "1px solid var(--border)",
            background: "var(--card)",
            fontSize: "0.8rem",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.4rem",
              marginBottom: "0.25rem",
            }}
          >
            <span
              style={{
                display: "inline-block",
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: botStatus.connected
                  ? "var(--primary)"
                  : "var(--destructive)",
              }}
            />
            <span style={{ fontWeight: 600 }}>
              {botStatus.connected ? "Connected" : "Disconnected"}
            </span>
          </div>
          {botStatus.connected && botStatus.botUsername && (
            <div style={{ color: "var(--muted-foreground)", fontSize: "0.75rem" }}>
              @{botStatus.botUsername} ({botStatus.botName})
            </div>
          )}
          {!botStatus.connected && botStatus.error && (
            <div style={{ color: "var(--destructive)", fontSize: "0.75rem" }}>
              {botStatus.error}
            </div>
          )}
        </div>
      )}

      {/* Recent messages */}
      <div>
        <div
          style={{
            fontSize: "0.75rem",
            fontWeight: 600,
            color: "var(--muted-foreground)",
            marginBottom: "0.35rem",
          }}
        >
          Recent Messages
        </div>

        {messagesLoading && (
          <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
            Loading messages...
          </div>
        )}

        {!messagesLoading && recentMessages.length === 0 && (
          <div style={{ fontSize: "0.8rem", color: "var(--muted-foreground)" }}>
            No messages sent yet.
          </div>
        )}

        {recentMessages.length > 0 && (
          <ul
            style={{
              listStyle: "none",
              margin: 0,
              padding: 0,
              display: "flex",
              flexDirection: "column",
              gap: "0.35rem",
            }}
          >
            {recentMessages.map((msg, i) => (
              <li
                key={`${msg.sentAt}-${i}`}
                style={{
                  padding: "0.35rem 0.5rem",
                  borderRadius: "4px",
                  border: "1px solid var(--border)",
                  background: "var(--card)",
                  fontSize: "0.75rem",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "0.15rem",
                  }}
                >
                  <span
                    style={{
                      fontSize: "0.65rem",
                      color: "var(--muted-foreground)",
                    }}
                  >
                    {new Date(msg.sentAt).toLocaleString()}
                  </span>
                  <span
                    style={{
                      fontSize: "0.65rem",
                      color: msg.success
                        ? "var(--primary)"
                        : "var(--destructive)",
                    }}
                  >
                    {msg.success ? "Sent" : "Failed"}
                  </span>
                </div>
                <div style={{ wordBreak: "break-word" }}>{msg.text}</div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
