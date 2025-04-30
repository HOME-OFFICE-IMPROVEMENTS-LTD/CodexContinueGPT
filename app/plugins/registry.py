# app/plugins/registry.py

from typing import Dict
from app.brain.core.base import CodexTool

class PluginRegistry:
    def __init__(self):
        self._tools: Dict[str, CodexTool] = {}

    def register(self, name: str, tool: CodexTool):
        self._tools[name] = tool

    def get(self, name: str) -> CodexTool:
        return self._tools.get(name)

    def all(self) -> Dict[str, CodexTool]:
        return self._tools
