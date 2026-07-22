export function TypingIndicator() {
  return (
    <div className="flex max-w-[80%] items-end gap-3 self-start">
      <div className="flex size-9 shrink-0 items-center justify-center rounded-full bg-navy-100 text-base text-navy-700">
        {/** TODO: Add Model Icon here... */}
      </div>
      <div className="flex items-center gap-1.5 rounded-message border border-neutral-200 bg-white px-4 py-3.5 shadow-sm">
        {Array.from({ length: 3 }).map((_, index) => (
          <span
            className="animate-typing-bounce size-2 rounded-full bg-neutral-400"
            style={{ animationDelay: ` ${index * 200}ms` }}
          />
        ))}
      </div>
    </div>
  );
}
