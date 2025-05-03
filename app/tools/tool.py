# app/tools/tool.py

from typing import Any, Dict

class Tool:
    name: str
    description: str

    def run(self, input: Dict[str, Any]) -> str:
        raise NotImplementedError("Each tool must implement the 'run' method.")
