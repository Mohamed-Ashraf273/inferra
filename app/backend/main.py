from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.backend.api.sessions import router as sessions_router
from app.backend.core.session_manager import session_manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)


@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        try:
            session = session_manager.get_session(session_id)
        except ValueError:
            await websocket.send_text(
                "[ERROR] Session not found. Please create a new session."
            )
            await websocket.close()
            return

        while True:
            data = await websocket.receive_text()
            session_manager.update_session_title(session_id, data)
            response = session.generate_reply(data)

            for char in response:
                await websocket.send_text(char)

            await websocket.send_text("[DONE]")

    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
