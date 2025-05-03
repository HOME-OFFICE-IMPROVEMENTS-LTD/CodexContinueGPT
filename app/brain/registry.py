# app/brain/registry.py

from app.brain.tools.base_tool import BaseTool
from typing import Dict

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool

    def get(self, tool_name: str) -> BaseTool:
        return self.tools.get(tool_name)

    def list_tools(self):
        return list(self.tools.keys())

# Singleton pattern for shared registry instance
tool_registry = ToolRegistry()
