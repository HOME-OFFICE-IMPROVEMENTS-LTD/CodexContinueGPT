# app/plugins/tools/plugin_metadata_plugin.py

from app.brain.core.base import CodexTool
from datetime import datetime

class PluginMetadataPlugin(CodexTool):
    name = "plugin_metadata"
    description = "List metadata about all available plugins"
    author = "CodexContinueGPT"
    version = "1.0"
    updated_at = datetime.utcnow().isoformat()

    def initialize(self):
        print("PluginMetadata plugin initialized")

    def execute(self, _input: str = "") -> dict:
        from app.plugins.register_all import register_all_plugins
        registry = register_all_plugins()
        result = []

        for name, tool in registry.all().items():
            result.append({
                "name": name,
                "description": getattr(tool, "description", "No description provided"),
                "author": getattr(tool, "author", "CodexContinueGPT"),
                "version": getattr(tool, "version", "1.0"),
                "updated_at": getattr(tool, "updated_at", datetime.utcnow().isoformat()),
                "requirements": getattr(tool, "requirements", []),
                "parameters": getattr(tool, "parameters", {}),
                "example": getattr(tool, "example", f"run {name} <input>"),
                "category": getattr(tool, "category", "Utility")
            })

        return {"plugins": result}

    def run(self, input: str) -> str:
        return str(self.execute(input))

    def shutdown(self):
        print("PluginMetadata plugin shutdown")

plugin = PluginMetadataPlugin()
