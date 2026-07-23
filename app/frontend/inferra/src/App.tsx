import { useState } from "react";
import { ChatHeader } from "./components/Chat/ChatHeader";
import { ChatInput } from "./components/Chat/ChatInput";
import { ChatWindow } from "./components/Chat/ChatWindow";
import { Sidebar } from "./components/Sidebar";
import { useChat } from "./hooks/useChat";

export default function App() {
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(true);
  const {
    messages,
    status,
    isBotTyping,
    isHistoryLoading,
    sendMessage,
    addSystemMessage,
  } = useChat(activeSessionId);

  const inputDisabled = activeSessionId == null || status != "connected";
  return (
    <div className="flex h-full w-full flex-col bg-neutral-100 md:flex-row md:p-6">
      <Sidebar
        isOpen={isSidebarOpen}
        activeSessionId={activeSessionId}
        onActiveSessionDeleted={() => setActiveSessionId(null)}
        onSessionCreated={setActiveSessionId}
        onSessionSelected={setActiveSessionId}
      />
      <div className="flex flex-1  flex-col bg-white justify-between">
        <ChatHeader
          status={status}
          onToggleSidebar={() => setIsSidebarOpen((open) => !open)}
        />
        <ChatWindow
          messages={messages}
          isBotTyping={isBotTyping}
          isLoading={isHistoryLoading}
          hasSession={activeSessionId !== null}
        />
        <ChatInput
          disabled={inputDisabled}
          sessionId={activeSessionId}
          onSend={sendMessage}
          onAudioUploaded={(filename) =>
            addSystemMessage(
              `Audio file '${filename}' uploaded and ready for analysis`,
            )
          }
        />
      </div>
    </div>
  );
}
