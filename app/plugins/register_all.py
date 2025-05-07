# app/plugins/register_all.py

from app.plugins.registry import PluginRegistry
from app.plugins.tools.shell import tool as shell_tool
from app.plugins.tools.memory_plugin import plugin as memory_tool
from app.plugins.tools.memory_inspect_plugin import plugin as memory_inspect_tool
from app.plugins.tools.plugin_metadata_plugin import plugin as metadata_tool


def register_all_plugins() -> PluginRegistry:
    registry = PluginRegistry()
    registry.register("shell", shell_tool)
    registry.register("memory", memory_tool)
    registry.register("memory_inspect", memory_inspect_tool)
    registry.register("plugin_metadata", metadata_tool)
    return registry
