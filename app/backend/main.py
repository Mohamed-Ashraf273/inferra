from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.backend.services.chat import get_ai_response

app = FastAPI()


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()

            response = await get_ai_response(data)

            for char in response:
                await websocket.send_text(char)

    except WebSocketDisconnect:
        print("Client disconnected")
