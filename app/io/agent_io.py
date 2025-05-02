# app/io/agent_io.py

from app.chat_memory import memory
import httpx
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

class CodexContinueIO:

    def __init__(self):
        self.session_id = "default"

    async def ask_backend(self, message: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{BACKEND_URL}/chat",
                    json={"session_id": self.session_id, "message": message},
                    timeout=20
                )
                response.raise_for_status()
                return response.json().get("reply", "⚠️ No reply received")
            except Exception as e:
                return f"🔥 Backend error: {e}"

    def remember(self, role: str, message: str):
        memory.add_message(self.session_id, role, message)

    def history(self):
        return memory.get_messages(self.session_id)

    def clear(self):
        memory.clear_session(self.session_id)

    def introspect(self):
        return {
            "session_id": self.session_id,
            "message_count": len(memory.get_messages(self.session_id)),
        }

IO = CodexContinueIO()
