# backend/app/routes/memory.py

from fastapi import APIRouter
from app.memory import memory  # Reuse the same memory instance

router = APIRouter()

@router.post("/memory/clear/{session_id}")
async def clear_session_memory(session_id: str):
    """Clear all memory for a given session."""
    memory.clear_memory(session_id)
    return {"message": f"Memory cleared for session: {session_id}"}

@router.get("/memory/sessions")
async def list_sessions():
    """List all active session IDs."""
    sessions = memory.list_sessions()
    return {"sessions": sessions}
@router.get("/memory/summary/{session_id}")
async def get_session_summary(session_id: str):
    """Get a summary of user messages for a given session."""
    summary = memory.get_summary(session_id)
    return {"summary": summary}
@router.get("/memory/{session_id}")
async def get_session_memory(session_id: str):
    """Get all messages for a given session."""
    messages = memory.get_messages(session_id)
    return {"messages": messages}
@router.post("/memory/{session_id}")
async def add_message_to_session(session_id: str, role: str, content: str):
    """Add a new message to the memory for a given session."""
    memory.add_message(session_id, role, content)
    return {"message": f"Message added to session: {session_id}"}
@router.delete("/memory/{session_id}")
async def delete_session_memory(session_id: str):
    """Delete all messages for a given session."""
    memory.clear_memory(session_id)
    return {"message": f"All messages deleted for session: {session_id}"}
@router.get("/memory")
async def get_all_sessions():
    """Get all sessions and their messages."""
    all_sessions = memory.sessions
    return {"sessions": all_sessions}
@router.get("/memory/health")
async def health_check():
    """Health check for the memory module."""
    return {"status": "Memory module is healthy"}