import { useMemo } from "react";

type WelcomeMessageProps = {
  hasSession: boolean;
};
export function WelcomMessage({ hasSession }: WelcomeMessageProps) {
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
    <div>
      <span>{/** TODO: Add waving hand icon here */}</span>
      <p className="text-base font-medium text-neutral-700">{welcomeContent}</p>
      <p className="text-sm">{detailsContent}</p>
    </div>
  );
}
