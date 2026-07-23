import { Music, Send } from "lucide-react";
import { useRef, useState, type KeyboardEvent } from "react";
import { useUploadAudio } from "../../hooks/useSessionMutations";
import { Button } from "../ui/Button";

type ChatInputProps = {
  disabled: boolean;
  sessionId: string | null;
  onSend: (text: string) => void;
  onAudioUploaded: (filename: string) => void;
};
export function ChatInput({
  disabled,
  sessionId,
  onSend,
  onAudioUploaded,
}: ChatInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const uploadAudio = useUploadAudio(sessionId);
  const SendIcon = <Send />;

  const resizeTextarea = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.width = `${el.scrollHeight}px`;
  };
  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue("");
    requestAnimationFrame(resizeTextarea);
  };
  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };
  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file || !sessionId) return;
    try {
      const result = await uploadAudio.mutateAsync(file);
      onAudioUploaded(result.filename);
    } catch {
      alert("Failed to upload audio file"); // TODO: Replace Alert with Toaster
    }
  };
  return (
    <div className="flex items-end gap-3 border-t border-neutral-200 bg-white p-4">
      <input
        ref={fileInputRef}
        type="file"
        accept="audio/*"
        className="hidden"
        onChange={handleFileChange}
      />
      <Button
        aria-label="Upload audio file"
        variant="secondary"
        disabled={disabled || uploadAudio.isPending}
        onClick={() => fileInputRef.current?.click()}
      >
        <Music />
      </Button>
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
          resizeTextarea();
        }}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder="Type your message here..."
        rows={1}
        className="max-h-32 flex-1 resize-none rounded-2xl border border-neutral-200 px-4 py-3 text-sm text-neutral-800 placeholder:text-neutral-400 focus:border-navy-400 focus:outline-none disabled:bg-neutral-500  disabled:text-neutral-400"
      />
      <Button
        aria-label="send message"
        disabled={disabled || value.trim().length === 0}
        onClick={handleSend}
      >
        {SendIcon}
      </Button>
    </div>
  );
}
