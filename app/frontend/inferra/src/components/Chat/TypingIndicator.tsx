import { Bot } from "lucide-react";

export function TypingIndicator() {
  return (
    <div className="flex max-w-[80%] items-end gap-3 self-start">
      <div className="flex size-9 shrink-0 items-center justify-center rounded-full bg-surface-2 text-secondary">
        <Bot />
      </div>
      <div className="flex items-center gap-1.5 rounded-message border border-border bg-surface px-4 py-3.5 shadow-sm">
        {Array.from({ length: 3 }).map((_, index) => (
          <span
            className="animate-typing-bounce size-2 rounded-full bg-text-light"
            style={{ animationDelay: ` ${index * 200}ms` }}
          />
        ))}
      </div>
    </div>
  );
}
