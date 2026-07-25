import { Menu } from "lucide-react";
import type { ConnectionStatus } from "../../types/chat";
import { Button } from "../ui/Button";
import { StatusBadge } from "../ui/StatusBadge";
type ChatHeaderProps = {
  status: ConnectionStatus;
  onToggleSidebar: () => void;
};

export function ChatHeader({ status, onToggleSidebar }: ChatHeaderProps) {
  return (
    <header className="flex items-center justify-between bg-secondary px-5 py-4">
      <div className="flex items-center gap-4">
        <Button
          aria-label="Toggle sidebar"
          onClick={onToggleSidebar}
          className="flex size-10 items-center justify-center rounded-lg bg-surface/10 text-text-inverse transition-colors duration-150 hover:bg-surface/20"
        >
          <Menu className="size-8" />
        </Button>
        <h1 className="text-lg font-semibold text-text-inverse">
          Inferra Chat Agent
        </h1>
      </div>
      <StatusBadge status={status} />
    </header>
  );
}
