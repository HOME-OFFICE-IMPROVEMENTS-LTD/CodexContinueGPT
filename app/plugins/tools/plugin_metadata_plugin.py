# app/plugins/tools/plugin_metadata_plugin.py

from app.brain.core.base import CodexTool

class PluginMetadataPlugin(CodexTool):
    name = "plugin_metadata"
    description = "List metadata about all available plugins"

    def initialize(self):
        print("PluginMetadata plugin initialized")

    def execute(self, _input: str = "") -> dict:
        from app.plugins.register_all import register_all_plugins
        registry = register_all_plugins()
        result = []
        for name, tool in registry.all().items():
            result.append({
                "name": name,
                "description": getattr(tool, "description", "No description"),
                "author": getattr(tool, "author", "CodexContinueGPT"),
                "example": getattr(tool, "example", f"run {name} <input>")
            })
        return {"plugins": result}

    def run(self, input_text: str):
        return self.execute(input_text)

    def shutdown(self):
        print("PluginMetadata plugin shutdown")

plugin = PluginMetadataPlugin()
