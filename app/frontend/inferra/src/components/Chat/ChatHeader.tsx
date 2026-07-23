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
    <header className="flex items-center justify-between bg-navy-700 px-5 py-4">
      <div className="flex items-center gap-4">
        <Button
          aria-label="Toggle sidebar"
          onClick={onToggleSidebar}
          // variant="ghost"
          className="flex size-10 items-center justify-center rounded-lg bg-white/10 text-white transition-colors duration-150 hover:bg-white/20"
        >
          <Menu className="size-8" />
        </Button>
        <h1 className="text-lg font-semibold text-white">Inferra Chat Agent</h1>
      </div>
      <StatusBadge status={status} />
    </header>
  );
}
