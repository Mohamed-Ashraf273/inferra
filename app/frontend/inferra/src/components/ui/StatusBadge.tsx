import type { ConnectionStatus } from "../../types/chat";

const LABELS: Record<ConnectionStatus, string> = {
  idle: "No session",
  connecting: "Connecting...",
  connected: "Connected",
  disconnected: "Disconnected",
  error: "Connection error",
};
export function StatusBadge({ status }: { status: ConnectionStatus }) {
  const style = (() => {
    switch (status) {
      case "connected":
        return "bg-status-online";
      case "connecting":
        return "animate-pulse bg-neutral-100";
      default:
        return "bg-status-offline";
    }
  })();
  return (
    <div className="flex items-center gap-2 rounded-full bg-white/10 px-3.5 py-1.5 text-sm text-white">
      <span className={`size-2.5 rounded-full ${style}`} />
      <span>{LABELS[status]}</span>
    </div>
  );
}
