import { useMemo } from "react";
import {
  useCreateSession,
  useDeleteAllSessions,
  useDeleteSession,
} from "../../hooks/useSessionMutations";
import { useSessions } from "../../hooks/useSessions";
import { Button } from "../ui/Button";
import { SessionItem } from "./SessionItem";

type SidebarProps = {
  isOpen: boolean;
  activeSessionId: string | null;
  onSessionCreated: (sessionId: string) => void;
  onSessionSelected: (sessionId: string) => void;
  onActiveSessionDeleted: () => void;
};

export function Sidebar({
  isOpen,
  activeSessionId,
  onSessionCreated,
  onSessionSelected,
  onActiveSessionDeleted,
}: SidebarProps) {
  const { data: sessions = [], isLoading } = useSessions();
  const createSession = useCreateSession();
  const deleteSession = useDeleteSession();
  const deleteAllSessions = useDeleteAllSessions();
  const handleCreate = async () => {
    const result = await createSession.mutateAsync();
    onSessionCreated(result.sessionId);
  };
  const handleDelete = async (sessionId: string) => {
    // TODO: Handle confirmation of chat session deletion
    await deleteSession.mutateAsync(sessionId);
    if (sessionId === activeSessionId) onActiveSessionDeleted();
  };
  const handleDeleteAll = async () => {
    // TODO: Handle confirmation of chat session deletion
    await deleteAllSessions.mutateAsync();
    onActiveSessionDeleted();
  };
  const sidebarState = useMemo(
    () => (isOpen ? "flex" : "hidden md:flex"),
    [isOpen],
  );
  const sessionsLists = (() => {
    const pStyle = "p-6 text-center text-sm text-neutral-400";
    if (isLoading) {
      // TODO: Replace with a loader component
      return <p className={pStyle}>Loading Sessions ...</p>;
    }
    if (!sessions.length) {
      return <p className={pStyle}>No chat sessions yet</p>;
    }
    return (
      <div className="flex flex-col gap-2">
        {sessions.map((session) => (
          <SessionItem
            key={session.session_id}
            session={session}
            isActive={session.session_id === activeSessionId}
            onSelect={onSessionSelected}
            onDelete={handleDelete}
          />
        ))}
      </div>
    );
  })();
  return (
    <aside
      className={`flex w-full shrink-0 flex-col overflow-hidden border-r border-neutral-200 bg-white md:w-80 ${sidebarState}`}
    >
      <div className="bg-navy-800 p-5">
        <h2 className="text-lg font-semibold text-white">Chat Sessions</h2>
      </div>
      <div className="flex flex-col gap-2 border-b border-neutral-200 p-4">
        <Button
          variant="primary"
          icon={<span> {/** TODO: Add Plus Icon */}</span>}
          onClick={handleCreate}
          disabled={createSession.isPending}
        >
          New Chat
        </Button>
        <Button
          variant="danger"
          icon={<span>{/** TODO: Add Trash Icon */}</span>}
          onClick={handleDeleteAll}
          disabled={sessions.length === 0 || deleteAllSessions.isPending}
        >
          Delete All
        </Button>
      </div>
      <div className="scroll-thin flex-1 overflow-y-auto p-3">
        {sessionsLists}
      </div>
    </aside>
  );
}
