# app/routes/memory.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.chat_memory import memory

router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)

class SessionListResponse(BaseModel):
    sessions: list[str]

class ClearSessionResponse(BaseModel):
    message: str

@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions():
    """
    List all active session IDs.
    """
    sessions = memory.list_sessions()
    return {"sessions": sessions}

@router.post("/clear/{session_id}", response_model=ClearSessionResponse)
async def clear_session_memory(session_id: str):
    """
    Clear all memory for a given session ID.
    """
    if session_id not in memory.list_sessions():
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found.")

    memory.clear_session(session_id)
    return {"message": f"Memory cleared for session: {session_id}"}
