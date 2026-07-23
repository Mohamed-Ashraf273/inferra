import { useQueryClient } from "@tanstack/react-query";
import { useCallback, useEffect, useRef, useState } from "react";
import { WS_URL } from "../lib/api";
import { queryKeys } from "../lib/queryClient";
import type { ChatMessage, ConnectionStatus } from "./../types/chat";
import { useSessionMessages } from "./useSessionMessages";
let localIdCounter = 0;
function nextLocalId(prefix: string) {
  localIdCounter += 1;
  return `${prefix}-${localIdCounter}`;
}
type UseChatResult = {
  messages: ChatMessage[];
  status: ConnectionStatus;
  isBotTyping: boolean;
  isHistoryLoading: boolean;
  sendMessage: (text: string) => void;
  addSystemMessage: (text: string) => void;
};
export function useChat(sessionId: string | null): UseChatResult {
  const queryClient = useQueryClient();
  const { data: history, isLoading: isHistoryLoading } =
    useSessionMessages(sessionId);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [status, setStatus] = useState<ConnectionStatus>("idle");
  const [isBotTyping, setIsBotTyping] = useState<boolean>(false);

  const wsRef = useRef<WebSocket | null>(null);
  const streamingMessageId = useRef<string | null>(null);

  useEffect(() => {
    setMessages(history ?? []);
  }, [sessionId, history]);
  useEffect(() => {
    if (!sessionId) {
      setStatus("idle");
      return;
    }
    setStatus("connecting");
    const socket = new WebSocket(`${WS_URL}/ws/chat/${sessionId}`);
    wsRef.current = socket;
    socket.onopen = () => setStatus("connected");
    socket.onmessage = (event: MessageEvent<string>) => {
      const data = event.data;
      if (data === "[DONE]") {
        setIsBotTyping(false);
        streamingMessageId.current = null;
        setMessages((prev) =>
          prev.map((m) =>
            m.status === "streaming" ? { ...m, status: "complete" } : m,
          ),
        );
        queryClient.invalidateQueries({ queryKey: queryKeys.sessions });
        return;
      }
      if (data.startsWith("[ERROR]")) {
        setIsBotTyping(false);
        streamingMessageId.current = null;
        setMessages((prev) => [
          ...prev,
          {
            id: nextLocalId("error"),
            role: "system",
            content: data.replace("[ERROR]", "").trim(),
            status: "error",
          },
        ]);
        return;
      }
      setIsBotTyping(false);
      setMessages((prev) => {
        if (streamingMessageId.current) {
          return prev.map((m) =>
            m.id === streamingMessageId.current
              ? { ...m, content: m.content + data }
              : m,
          );
        }
        const id = nextLocalId("assistant");
        streamingMessageId.current = id;
        return [
          ...prev,
          { id, role: "assistant", content: data, status: "streaming" },
        ];
      });
      socket.onerror = () => setStatus("error");
      socket.onclose = () => setStatus("disconnected");
      return () => {
        socket.close();
        wsRef.current = null;
        streamingMessageId.current = null;
      };
    };
  }, [sessionId, queryClient]);

  const sendMessage = useCallback((text: string) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    const socket = wsRef.current;
    if (!socket || socket.readyState !== WebSocket.OPEN) return;
    streamingMessageId.current = null;
    setMessages((prev) => [
      ...prev,
      {
        id: nextLocalId("user"),
        role: "user",
        content: trimmed,
        status: "sent",
      },
    ]);
    setIsBotTyping(true);
    socket.send(trimmed);
  }, []);
  const addSystemMessage = useCallback((text: string) => {
    setMessages((prev) => [
      ...prev,
      {
        id: nextLocalId("system"),
        role: "system",
        content: text,
        status: "complete",
      },
    ]);
  }, []);
  return {
    messages,
    status,
    isBotTyping,
    isHistoryLoading,
    sendMessage,
    addSystemMessage,
  };
}
