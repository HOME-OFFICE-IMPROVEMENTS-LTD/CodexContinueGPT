from app.plugins.registry import PluginRegistry
from app.plugins.tools.shell import tool as shell_tool
from app.plugins.tools.memory_plugin import plugin as memory_tool
from app.plugins.tools.memory_inspect_plugin import plugin as memory_inspect_tool
from app.plugins.tools.plugin_metadata_plugin import plugin as metadata_tool
from app.plugins.tools.ollama_fallback import tool as ollama_tool

def register_all_plugins() -> PluginRegistry:
    registry = PluginRegistry()
    registry.register(shell_tool)
    registry.register(memory_tool)
    registry.register(memory_inspect_tool)
    registry.register(metadata_tool)
    registry.register(ollama_tool)
    return registry
