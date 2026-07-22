import { useEffect, useRef } from "react";
import type { ChatMessage } from "../../types/chat";

type ChatWindowProps = {
  messages: ChatMessage[];
  isBotTyping: boolean;
  isLoading: boolean;
  hasSession: boolean;
};
export function ChatWindow({
  messages,
  isBotTyping,
  isLoading,
  hasSession,
}: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    bottomRef?.current?.scrollIntoView({ block: "end" });
  }, [messages, isBotTyping]);
  const isEmpty = messages.length === 0 && !isLoading;
  const windowContent = (() => {
    if (isLoading)
      return (
        <p className="m-auto text-sm text-neutral-400">Loading messages...</p>
      ); // TODO: Add Loading Spinner
    if (isEmpty) return <WelcomeMessage hasSession={hasSession} />;
    return (
      <>
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isBotTyping && <TypingIndicator />}
      </>
    );
  })();
  return (
    <div>
      {windowContent}
      <div ref={bottomRef} />
    </div>
  );
}
