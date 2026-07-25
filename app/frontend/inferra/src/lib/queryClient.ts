import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 10_000,
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});

export const queryKeys = {
  sessions: ["sessions"] as const,
  sessionMessages: (sessionId: string) =>
    ["sessions", sessionId, "messages"] as const,
};
