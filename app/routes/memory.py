# app/routes/memory.py

from fastapi import APIRouter, HTTPException
from typing import Optional
from app.memory.manager import MemoryManager

router = APIRouter()

@router.get("/memory")
async def fetch_memory(session_id: Optional[str] = "default", mode: Optional[str] = "short"):
    try:
        memory = MemoryManager(session_id)
        messages = await memory.get_messages(mode=mode)
        return {"session_id": session_id, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch memory: {str(e)}")

@router.delete("/memory")
async def reset_memory(session_id: Optional[str] = "default"):
    try:
        memory = MemoryManager(session_id)
        await memory.reset()
        return {"message": f"Memory for session '{session_id}' has been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset memory: {str(e)}")
