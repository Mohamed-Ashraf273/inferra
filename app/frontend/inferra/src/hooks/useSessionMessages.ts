import { useQuery } from "@tanstack/react-query";
import { fetchSessionMessages } from "../lib/api";
import { queryKeys } from "../lib/queryClient";
import type { ChatMessage } from "../types/chat";

export function useSessionMessages(sessionId: string | null) {
  return useQuery({
    queryKey: queryKeys.sessionMessages(sessionId ?? ""),
    queryFn: () => fetchSessionMessages(String(sessionId)),
    enabled: sessionId !== null,
    select: (data): ChatMessage[] =>
      data.messages.map((msg, index) => ({
        id: `history-${index}`,
        role: msg.role,
        content: msg.content,
        status: "complete",
      })),
  });
}
