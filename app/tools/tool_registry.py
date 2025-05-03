# app/tools/tool_registry.py

from typing import Dict, Type
from app.tools.tool import Tool
from app.tools.hello_tool import HelloTool

# Register tools here
registered_tools: Dict[str, Type[Tool]] = {
    "hello": HelloTool
}

def get_tool(name: str) -> Tool:
    if name not in registered_tools:
        raise ValueError(f"Tool '{name}' not found.")
    return registered_tools[name]()
