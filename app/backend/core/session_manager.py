import uuid
from datetime import datetime
from typing import Dict

from app.backend.core.chat_session import Session
from app.backend.database import db


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = Session(session_id)
        db.save_session(session_id, self.sessions[session_id].title)
        return session_id

    def get_session(self, session_id: str) -> Session:
        if session_id in self.sessions:
            return self.sessions[session_id]

        session_data = db.get_session(session_id)
        if session_data is None:
            raise ValueError(f"Session {session_id} not found in database")

        session = Session(session_id)

        # Restore session metadata
        if session_data:
            session.title = session_data.get("title", "New Chat")
            session.message_count = session_data.get("msg_cnt", 0)
            if session_data.get("created_at"):
                session.created_at = datetime.fromisoformat(session_data["created_at"])
            if session_data.get("updated_at"):
                session.updated_at = datetime.fromisoformat(session_data["updated_at"])

        # Restore chat history from database
        messages = db.get_messages(session_id)
        for msg in messages:
            if msg["role"] == "user":
                session.agent.memory.chat_memory.add_user_message(msg["content"])
            elif msg["role"] == "assistant":
                session.agent.memory.chat_memory.add_ai_message(msg["content"])

        # Restore audio if exists
        audio_data = db.get_audio(session_id)
        if audio_data and audio_data.get("audio_data"):
            session.update_audio(audio_data["audio_data"])

        self.sessions[session_id] = session
        return session

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        else:
            session_data = db.get_session(session_id)
            if session_data is None:
                raise ValueError(f"Session {session_id} not found in database")

            db.delete_session(session_id)

    def delete_all_sessions(self):
        self.sessions.clear()
        db.delete_all_sessions()

    def list_sessions(self):
        """List all sessions from database"""
        return db.get_all_sessions()

    def update_session_title(self, session_id: str, first_message: str):
        session = self.get_session(session_id)
        if session.message_count == 0:
            session.title = first_message[:50] + "..." if len(first_message) > 50 else first_message
        session.message_count += 1
        session.updated_at = datetime.now()
        db.save_session(session_id, session.title, msg_cnt=session.message_count)

    def save_message(self, session_id: str, role: str, content: str):
        """Save a message to the database"""
        db.save_message(session_id, role, content)


session_manager = SessionManager()
