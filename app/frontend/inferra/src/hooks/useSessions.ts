import { useQuery } from "@tanstack/react-query";
import { fetchSessions } from "../lib/api";
import { queryKeys } from "../lib/queryClient";

export function useSessions() {
  return useQuery({
    queryKey: queryKeys.sessions,
    queryFn: fetchSessions,
    select: (data) => data.sessions,
  });
}
