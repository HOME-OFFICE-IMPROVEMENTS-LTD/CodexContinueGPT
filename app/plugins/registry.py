from typing import Dict
from app.plugins.interface import CodexTool

class PluginRegistry:
    def __init__(self):
        self._registry: Dict[str, CodexTool] = {}

    def register(self, plugin: CodexTool):
        self._registry[plugin.name] = plugin
        plugin.initialize()

    def get(self, name: str) -> CodexTool:
        return self._registry[name]

    def all(self) -> Dict[str, CodexTool]:
        return self._registry

    def shutdown_all(self):
        for plugin in self._registry.values():
            plugin.shutdown()
