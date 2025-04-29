# app/plugins/tools/memory.py

from app.plugins.base import Tool
from app.chat_memory import memory

class MemoryTool(Tool):
    name = "memory"
    description = "List sessions and messages from memory"

    async def run(self, input_text: str) -> str:
        session_id = input_text.strip() or "default"
        messages = memory.get_messages(session_id)
        return f"Session: {session_id}\n" + "\n".join([f"{m['role']}: {m['content']}" for m in messages])

tool = MemoryTool()
