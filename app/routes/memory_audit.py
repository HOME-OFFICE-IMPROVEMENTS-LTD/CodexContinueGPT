# app/routes/memory_audit.py

from fastapi import APIRouter
from app.memory.manager import MemoryManager

router = APIRouter()

@router.get("/memory/audit/{session_id}")
async def audit_memory(session_id: str):
    memory = MemoryManager(session_id)
    short = await memory.get_messages("short")
    full = await memory.get_messages("long")
    return {
        "session_id": session_id,
        "short": short,
        "full": full,
        "count": {
            "short": len(short),
            "full": len(full)
        }
    }
