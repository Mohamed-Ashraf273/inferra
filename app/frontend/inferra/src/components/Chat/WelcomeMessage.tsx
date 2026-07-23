import { Hand } from "lucide-react";
import { useMemo } from "react";

type WelcomeMessageProps = {
  hasSession: boolean;
};
export function WelcomeMessage({ hasSession }: WelcomeMessageProps) {
  const welcomeContent = useMemo(
    () => (hasSession ? "Ready to chat!" : "Welcome to Inferra Chat"),
    [hasSession],
  );
  const detailsContent = useMemo(
    () =>
      hasSession
        ? "Type your message below."
        : "Click 'New Chat' to start a conversation.",
    [hasSession],
  );
  return (
    <div className="m-auto flex flex-col items-center gap-2 px-6 py-16 text-center text-neutral-500">
      <Hand />
      <p className="text-base font-medium text-neutral-700">{welcomeContent}</p>
      <p className="text-sm">{detailsContent}</p>
    </div>
  );
}
