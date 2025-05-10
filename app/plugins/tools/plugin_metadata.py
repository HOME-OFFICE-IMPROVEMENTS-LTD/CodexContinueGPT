from app.brain.core.base import CodexTool

class PluginMetadata(CodexTool):
    name = "plugin_metadata"
    description = "Returns metadata for all registered plugins"

    def initialize(self):
        print("PluginMetadata plugin initialized")

    def execute(self, input_text: str = "") -> dict:
        from app.plugins.registry import PluginRegistry  # late import to avoid circular import
        return {
            name: {
                "description": plugin.description,
                "methods": [method for method in dir(plugin) if not method.startswith("_")]
            }
            for name, plugin in PluginRegistry.get_all().items()
        }

    def run(self, input_text: str = "") -> dict:
        return self.execute(input_text)

    def shutdown(self):
        print("PluginMetadata plugin shutdown")

tool = PluginMetadata()
