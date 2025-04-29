# app/plugins/manager.py

import importlib
import pkgutil
from app.plugins.base import Tool

TOOL_REGISTRY = {}

def load_plugins():
    from app.plugins import tools
    for _, modname, _ in pkgutil.iter_modules(tools.__path__):
        mod = importlib.import_module(f"app.plugins.tools.{modname}")
        if hasattr(mod, "tool") and isinstance(mod.tool, Tool):
            TOOL_REGISTRY[mod.tool.name] = mod.tool

async def run_tool(tool_name: str, input_text: str) -> str:
    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        return f"Tool '{tool_name}' not found."
    return await tool.run(input_text)
