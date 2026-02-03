from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import JSONResponse

from app.backend.core.session_manager import session_manager
from app.backend.database import db

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Inferra Chat API"}


@router.post("/sessions")
async def create_session():
    session_id = session_manager.create_session()
    return {"session_id": session_id}


@router.post("/sessions/{session_id}/upload-audio")
async def upload_audio(session_id: str, file: UploadFile = File(...)):
    try:
        audio_data = await file.read()

        session = session_manager.get_session(session_id)
        session.update_audio(audio_data)

        return {
            "message": "Audio uploaded successfully",
            "filename": file.filename,
            "content_type": file.content_type,
        }
    except ValueError as e:
        return JSONResponse(status_code=404, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Upload failed: {str(e)}"})


@router.get("/sessions")
async def list_sessions():
    return {"sessions": session_manager.list_sessions()}


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    """Get all messages for a session"""
    try:
        messages = db.get_messages(session_id)
        return {"messages": messages}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    try:
        session_manager.delete_session(session_id)
        return {"message": "Session deleted"}
    except ValueError as e:
        return JSONResponse(status_code=404, content={"error": str(e)})


@router.delete("/sessions")
async def delete_all_sessions():
    session_manager.delete_all_sessions()
    return {"message": "All sessions deleted"}
