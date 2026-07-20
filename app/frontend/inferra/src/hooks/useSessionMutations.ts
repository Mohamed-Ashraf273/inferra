import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  createSession,
  deleteAllSessions,
  deleteSession,
  uploadAudio,
} from "../lib/api";
import { queryKeys } from "../lib/queryClient";

export function useCreateSession() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.sessions });
    },
  });
}
export function useDeleteSession() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (sessionId: string) => deleteSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.sessions });
    },
  });
}

export function useDeleteAllSessions() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteAllSessions,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.sessions });
    },
  });
}

export function useUploadAudio(sessionId: string | null) {
  return useMutation({
    mutationFn: (file: File) => {
      if (!sessionId) {
        return Promise.reject(new Error("No active session"));
      }
      return uploadAudio(sessionId, file);
    },
  });
}
