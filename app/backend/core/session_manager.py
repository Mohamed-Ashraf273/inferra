import uuid
from datetime import datetime
from typing import Dict

from app.backend.core.chat_session import Session


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = Session(session_id)
        return session_id

    def get_session(self, session_id: str) -> Session:
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
