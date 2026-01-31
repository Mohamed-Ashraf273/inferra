import uuid
from datetime import datetime
from typing import Dict

from inferra.src.core.agent import Agent


class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = "New Chat"
        self.agent = Agent()
        self.message_count = 0

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message_count": self.message_count,
        }


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = ChatSession(session_id)
        return session_id

    def get_session(self, session_id: str) -> ChatSession:
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        return self.sessions[session_id]

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def delete_all_sessions(self):
        self.sessions.clear()

    def list_sessions(self):
        return [
            session.to_dict()
            for session in sorted(
                self.sessions.values(),
                key=lambda x: x.updated_at,
                reverse=True,
            )
        ]

    def update_session_title(self, session_id: str, first_message: str):
        session = self.get_session(session_id)
        if session.message_count == 0:
            session.title = (
                first_message[:50] + "..."
                if len(first_message) > 50
                else first_message
            )
        session.message_count += 1
        session.updated_at = datetime.now()


session_manager = SessionManager()
