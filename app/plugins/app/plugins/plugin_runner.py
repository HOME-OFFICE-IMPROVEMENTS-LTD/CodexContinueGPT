# app/plugins/plugin_runner.py

from app.plugins.manager import PluginManager
from app.plugins.registry import PluginRegistry

plugin_manager = PluginManager()
plugin_registry = PluginRegistry()

# Auto-register all plugins
for name in plugin_manager.list_plugins():
    plugin_instance = plugin_manager.plugins[name]
    plugin_registry.register(name, plugin_instance)

def run_plugin(name: str, data: str):
    plugin = plugin_registry.get(name)
    if not plugin:
        raise ValueError(f"Plugin '{name}' is not registered.")
    plugin.initialize()
    result = plugin.execute(data)
    plugin.shutdown()
    return result
