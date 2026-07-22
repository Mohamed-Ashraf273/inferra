import { useCallback } from "react";
import type { ChatMessage } from "../../types/chat";

type MessageBubbleProps = {
  message: ChatMessage;
};
export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const systemMessageBubble = useCallback(
    () =>
      (() => {
        const messageStyle =
          message.status === "error"
            ? "bg-red-50 text-status-offline"
            : "bg-navy-50 text-navy-700";
        return (
          <div className="animate-message-in flex justify-center">
            <div
              className={`max-w-[90%] rounded-lg px-4 py-2 text-sm ${messageStyle}`}
            >
              {message.content}
            </div>
          </div>
        );
      })(),
    [message.content, message.status],
  );
  const messageBubble = useCallback(
    () =>
      (() => {
        const messageStyle = isUser
          ? "bg-navy-700 text-white"
          : "border border-neutral-200 bg-white text-neutral-800";
        const icon = isUser ? "User" : "Model"; // TODO: Replace with real icons
        const iconStyle = isUser
          ? "bg-navy-700 text-white"
          : "bg-navy-100 text-navy-700";
        const messageWrapperStyle = isUser
          ? "ml-auto flex-row-reverse self-end"
          : "self-start";
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
              className={`rounded-[var(--radius-message) px-4 py-2.5 text-sm leading-relaxed shadow-sm ${messageStyle}]`}
            >
              <span className="whitespace-pre-wrap wrap-break-word">
                {message.content}
              </span>
            </div>
          </div>
        );
      })(),
    [isUser, message.content],
  );
  if (message.role == "system") return systemMessageBubble;
  return messageBubble;
}
