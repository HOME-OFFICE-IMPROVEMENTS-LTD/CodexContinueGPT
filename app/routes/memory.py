from fastapi import APIRouter
from app.chat_memory import memory  # ✅ Correct memory import

router = APIRouter(
    prefix="/memory",   # ✅ Correct prefix
    tags=["Memory"]     # ✅ Nice grouping in Swagger
)

@router.get("/sessions")
async def list_sessions():
    """List all active session IDs."""
    sessions = memory.list_sessions()
    return {"sessions": sessions}

@router.post("/clear/{session_id}")
async def clear_session_memory(session_id: str):
    """Clear all memory for a given session."""
    memory.clear_memory(session_id)
    return {"message": f"Memory cleared for session: {session_id}"}
