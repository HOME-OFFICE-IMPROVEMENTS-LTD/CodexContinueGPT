# app/plugins/tools/memory_inspect_plugin.py

from app.brain.core.base import CodexTool
from app.memory.manager import MemoryManager
from datetime import datetime
import asyncio

class MemoryInspectPlugin(CodexTool):
    name = "memory_inspect"
    description = "Inspect full memory contents for a given session ID"
    author = "CodexContinueGPT"
    version = "1.0"
    updated_at = datetime.utcnow().isoformat()
    category = "Utility"
    requirements = []
    parameters = {}
    example = "run memory_inspect <session_id>"

    def initialize(self):
        print("MemoryInspect plugin initialized")

    def run(self, input: str) -> dict:
        return self.execute(input)

    def execute(self, session_id: str) -> dict:
        try:
            memory = MemoryManager(session_id.strip())
            loop = asyncio.get_event_loop()
            short = loop.run_until_complete(memory.get_messages("short"))
            full = loop.run_until_complete(memory.get_messages("long"))
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

plugin = MemoryInspectPlugin()
