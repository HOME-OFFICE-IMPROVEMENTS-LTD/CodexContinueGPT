# app/plugins/tools/memory_plugin.py

from app.brain.core.base import CodexTool
from app.memory.manager import MemoryManager
from datetime import datetime
import asyncio

class MemoryPlugin(CodexTool):
    name = "memory"
    description = "List short memory for a given session"
    author = "CodexContinueGPT"
    version = "1.0"
    updated_at = datetime.utcnow().isoformat()
    category = "Utility"
    requirements = []
    parameters = {}
    example = "run memory <session_id>"

    def initialize(self):
        print("MemoryPlugin initialized")

    def run(self, input: str) -> dict:
        return self.execute(input)

    def execute(self, session_id: str) -> dict:
        try:
            memory = MemoryManager(session_id.strip())
            loop = asyncio.get_event_loop()
            messages = loop.run_until_complete(memory.get_messages("short"))
            return {
                "session": session_id,
                "messages": messages,
                "count": len(messages)
            }
        except Exception as e:
            return {"error": str(e)}

plugin = MemoryPlugin()
