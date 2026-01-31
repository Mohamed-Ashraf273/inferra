from datetime import datetime

from inferra.src.core.agent import Agent


class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = "New Chat"
        self.agent = Agent()
        self.message_count = 0

    def update_audio(self, audio_data):
        self.agent.loaded_audio = audio_data
        self.agent.tools = self.agent._get_tools()
        self.agent.agent_executor = self.agent._create_agent_executor()

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message_count": self.message_count,
        }

    def generate_reply(self, message: str) -> str:
        result = self.agent.agent_executor.invoke({"input": message})
        return result.get("output", "No response generated")
