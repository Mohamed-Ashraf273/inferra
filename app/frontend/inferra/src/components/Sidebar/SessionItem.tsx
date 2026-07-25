import { Trash } from "lucide-react";
import { useMemo, type MouseEvent } from "react";
import type { ChatSession } from "../../types/chat";
import { Button } from "../ui/Button";

type SessionItemProps = {
  session: ChatSession;
  isActive: boolean;
  onSelect: (sessionId: string) => void;
  onDelete: (sessionId: string) => void;
};
const activeStyles = {
  p: "text-text-inverse",
  div: "bg-secondary-active text-text-inverse ",
};
const nonActiveStyles = {
  p: "text-text-muted",
  div: "bg-surface-2 hover:text-white",
};
export function SessionItem({
  session,
  isActive,
  onSelect,
  onDelete,
}: SessionItemProps) {
  const handleDeleteSession = (e: MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    onDelete(session.session_id);
  };
  const styles = useMemo(
    () => (isActive ? activeStyles : nonActiveStyles),
    [isActive],
  );
  return (
    <div
      className={`flex items-center gap-2 w-full rounded-lg p-2.5  cursor-pointer ${styles.div}`}
      onClick={() => onSelect(session.session_id)}
    >
      <div className="min-w-0 flex-1 flex items-center justify-between text-left px-2">
        <p className="truncate text-sm font-medium text-white">
          {session.title}
        </p>
        <p className={`text-xs ${styles.p}`}>
          {session.message_count} messages
        </p>
      </div>

      <Button
        aria-label={`delete ${session.title}`}
        variant="danger"
        onClick={(e) => {
          e.stopPropagation();
          handleDeleteSession(e);
        }}
        className="p-2 shrink-0 rounded-md mr-2"
      >
        <Trash />
      </Button>
    </div>
  );
}
