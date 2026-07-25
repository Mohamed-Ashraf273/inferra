import { Bot, User } from "lucide-react";
import type { ChatMessage } from "../../types/chat";

type MessageBubbleProps = {
  message: ChatMessage;
};
export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const messageStyle = isUser
    ? "bg-primary text-text-inverse"
    : "border border-border bg-surface text-text";
  const icon = isUser ? <User /> : <Bot />;
  const iconStyle = isUser
    ? "bg-primary text-text-inverse"
    : "bg-surface-2 border border-neutral-400 shadow-sm text-secondary";
  const messageWrapperStyle = isUser
    ? "ml-auto flex-row-reverse self-end"
    : "self-start";
  if (message.role == "system") {
    const messageStyle =
      message.status === "error"
        ? "bg-danger/10 text-danger"
        : "bg-surface-2 text-secondary";
    return (
      <div className="animate-message-in flex justify-center">
        <div
          className={`max-w-[90%] rounded-lg px-4 py-2 text-sm ${messageStyle}`}
        >
          {message.content}
        </div>
      </div>
    );
  }
  return (
    <div
      className={`animate-message-in flex max-w-[80%] items-end gap-3 ${messageWrapperStyle}`}
    >
      <div
        className={`flex size-9 shrink-0 items-center justify-center rounded-full text-base ${iconStyle}`}
      >
        {icon}
      </div>
      <div
        className={`rounded-message px-4 py-2.5 text-sm leading-relaxed shadow-sm ${messageStyle}`}
      >
        <span className="whitespace-pre-wrap wrap-break-word">
          {message.content}
        </span>
      </div>
    </div>
  );
}
