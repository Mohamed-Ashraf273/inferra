from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.backend.models.chat_model import ChatModel
from app.backend.models.session_manager import session_manager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Inferra Chat API"}


@app.post("/sessions")
async def create_session():
    session_id = session_manager.create_session()
    return {"session_id": session_id}


@app.get("/sessions")
async def list_sessions():
    return {"sessions": session_manager.list_sessions()}


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    try:
        session_manager.delete_session(session_id)
        return {"message": "Session deleted"}
    except ValueError as e:
        return JSONResponse(status_code=404, content={"error": str(e)})


@app.delete("/sessions")
async def delete_all_sessions():
    """Delete all sessions"""
    session_manager.delete_all_sessions()
    return {"message": "All sessions deleted"}


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

        chat_model = ChatModel(session.agent)

        while True:
            data = await websocket.receive_text()

            session_manager.update_session_title(session_id, data)

            response = chat_model.generate_reply(data)

            for char in response:
                await websocket.send_text(char)

            await websocket.send_text("[DONE]")

    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
