# app/plugins/plugin_runner.py

from app.plugins.registry import PluginRegistry
from app.plugins.tools.shell import ShellPlugin
from app.plugins.tools.memory_plugin import MemoryPlugin

# Optional fallback plugin
class AgentPlugin:
    def __init__(self):
        pass

    def initialize(self):
        print("Agent plugin initialized")

    def execute(self, data):
        return {"agent_response": f"🧠 Agent plugin processed: {data}"}

    def shutdown(self):
        print("Agent plugin shutdown")

# Create registry and register default tools
registry = PluginRegistry()
registry.register("shell", ShellPlugin())
registry.register("memory", MemoryPlugin())
registry.register("agent_plugin", AgentPlugin())

def run_plugin(name: str, data):
    tool = registry.get(name)
    if not tool:
        raise ValueError(f"Plugin '{name}' not found in registry")
    tool.initialize()
    result = tool.execute(data)
    tool.shutdown()
    return result
