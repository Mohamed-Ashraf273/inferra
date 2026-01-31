from app.backend.core.chat_session import Session


async def get_ai_response(message: str, chat: Session) -> str:
    """
    Handles the chat logic:
    - Can call multiple AI models
    - Can add preprocessing or postprocessing
    """
    reply = chat.generate_reply(message)
    return reply
