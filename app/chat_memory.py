# app/chat_memory.py

from app.memory.manager import MemoryManager

async def add_message(session_id: str, role: str, content: str):
    memory = MemoryManager(session_id)
    await memory.save_message(role, content)

async def get_short_memory(session_id: str, limit: int = 5):
    memory = MemoryManager(session_id)
    return await memory.get_messages(mode="short", limit=limit)
