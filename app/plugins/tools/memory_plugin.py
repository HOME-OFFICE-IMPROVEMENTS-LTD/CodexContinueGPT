# app/plugins/tools/memory_plugin.py

from app.brain.core.base import CodexTool
from app.chat_memory import get_short_memory

class MemoryPlugin(CodexTool):
    name = "memory"
    description = "List short memory for a given session"

    def initialize(self):
        print("Memory plugin initialized")

    def execute(self, session_id: str) -> dict:
        import asyncio
        try:
            messages = asyncio.run(get_short_memory(session_id.strip()))
            return {
                "session": session_id,
                "messages": messages
            }
        except Exception as e:
            return {"error": str(e)}

    def run(self, input_text: str):
        return self.execute(input_text)

    def shutdown(self):
        print("Memory plugin shutdown")

plugin = MemoryPlugin()
