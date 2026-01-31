from app.backend.models.chat_model import ChatModel
from inferra.src.core.agent import agent_init

agent = agent_init()
chat_model = ChatModel(agent)


async def get_ai_response(message: str) -> str:
    """
    Handles the chat logic:
    - Can call multiple AI models
    - Can add preprocessing or postprocessing
    """
    reply = chat_model.generate_reply(message)
    return reply
