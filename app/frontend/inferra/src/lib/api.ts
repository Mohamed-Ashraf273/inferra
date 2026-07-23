import type {
  ChatSessionsResponse,
  SessionMessagesResponse,
  UploadAudioResponse,
} from "../types/chat";

// TODO: Add Types for .env
export const API_URL = import.meta.env.VITE_API_URL;
export const WS_URL = import.meta.env.VITE_WS_URL;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, init);
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(
      body.error ?? `Request failed with status ${response.status}`,
    );
  }
  return response.json() as Promise<T>;
}

export function fetchSessions(): Promise<ChatSessionsResponse> {
  return request<ChatSessionsResponse>("/sessions");
}

export function createSession(): Promise<{ sessionId: string }> {
  return request<{ sessionId: string }>("/sessions", { method: "POST" });
}

export function deleteSession(sessionId: string): Promise<void> {
  return request<void>(`/sessions/${sessionId}`, { method: "DELETE" });
}
export function deleteAllSessions(): Promise<void> {
  return request<void>("/sessions", { method: "DELETE" });
}
export function uploadAudio(
  sessionId: string,
  file: File,
): Promise<UploadAudioResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return request<UploadAudioResponse>(`/sessions/${sessionId}/upload-audio`, {
    method: "POST",
    body: formData,
  });
}
export function fetchSessionMessages(
  sessionId: string,
): Promise<SessionMessagesResponse> {
  return request<SessionMessagesResponse>(`/sessions/${sessionId}/messages`);
}
