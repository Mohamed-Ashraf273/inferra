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
  p: "text-navy-100",
  div: "bg-navy-700 text-white",
};
const nonActiveStyles = {
  p: "text-netural-500",
  div: "bg-netural-50 hover:bg-netural-100",
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
    <div>
      <Button
        variant="ghost"
        onClick={() => onSelect(session.session_id)}
        className={`min-w-0 flex-1 text-left ${styles["div"]}`}
      >
        <p className={`truncate text-sm font-medium`}>{session.title}</p>
        <p className={`text-xs styles["p"]`}>
          {session.message_count} messages
        </p>
      </Button>
      <Button
        aria-label={`delete ${session.title}`}
        variant="danger"
        onClick={handleDeleteSession}
        className="size-8 flex shrink-0 rounded-md "
      >
        <Trash /> {/** TOOD: Add <TrasTrashh/> Icon here */}
      </Button>
    </div>
  );
}
