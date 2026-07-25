export interface ChatSession {
  session_id: string;
  title: string;
  message_count: number;
}
export interface ChatSessionsResponse {
  sessions: ChatSession[];
}

export type MessageRole = "user" | "assistant" | "system";

export interface PersistedMessage {
  role: MessageRole;
  content: string;
}
export interface SessionMessagesResponse {
  messages: PersistedMessage[];
}
export type DisplayRole = MessageRole;
export type MessageStatus = "sent" | "streaming" | "complete" | "error";

export interface ChatMessage {
  id: string;
  role: DisplayRole;
  content: string;
  status: MessageStatus;
}

export interface UploadAudioResponse {
  filename: string;
  error?: string;
}
export type ConnectionStatus =
  | "idle"
  | "connecting"
  | "connected"
  | "disconnected"
  | "error";
