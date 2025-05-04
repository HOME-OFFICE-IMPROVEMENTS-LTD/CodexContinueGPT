# app/plugins/tools/memory.py

from app.plugins.base import CodexTool
from app.chat_memory import get_short_memory

class MemoryPlugin(CodexTool):
    name = "memory"
    description = "List short memory messages for a session"

    def initialize(self):
        print("Memory plugin initialized")

    def execute(self, input_text: str) -> dict:
        import asyncio
        session_id = input_text.strip() or "default"
        messages = asyncio.run(get_short_memory(session_id))
        return {
            "session": session_id,
            "messages": messages
        }

    def run(self, input_text: str) -> dict:
        return self.execute(input_text)

    def shutdown(self):
        print("Memory plugin shutdown")

tool = MemoryPlugin()

