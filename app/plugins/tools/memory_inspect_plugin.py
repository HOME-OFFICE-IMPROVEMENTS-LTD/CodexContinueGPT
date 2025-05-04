# app/plugins/tools/memory_inspect_plugin.py

from app.brain.core.base import CodexTool
from app.memory.manager import MemoryManager
import asyncio

class MemoryInspectPlugin(CodexTool):
    name = "memory_inspect"
    description = "Inspect full memory contents for a given session ID"

    def initialize(self):
        print("MemoryInspect plugin initialized")

    def execute(self, session_id: str) -> dict:
        try:
            memory = MemoryManager(session_id.strip())
            short = asyncio.run(memory.get_messages("short"))
            full = asyncio.run(memory.get_messages("long"))
            return {
                "session": session_id,
                "short": short,
                "full": full,
                "count": {
                    "short": len(short),
                    "full": len(full)
                }
            }
        except Exception as e:
            return {"error": str(e)}

    def run(self, input_text: str) -> dict:
        return self.execute(input_text)

    def shutdown(self):
        print("MemoryInspect plugin shutdown")

plugin = MemoryInspectPlugin()
