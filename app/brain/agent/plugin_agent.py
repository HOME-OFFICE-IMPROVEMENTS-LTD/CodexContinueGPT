# app/brain/agent/plugin_agent.py

from app.plugins.register_all import register_all_plugins

class PluginAgent:
    def __init__(self):
        self.registry = register_all_plugins()

    def maybe_execute(self, prompt: str) -> dict | None:
        if not prompt.startswith("/run "):
            return None

        try:
            _, plugin_name, *input_parts = prompt.split()
            input_text = " ".join(input_parts)
            plugin = self.registry.get(plugin_name)
            if not plugin:
                return {"error": f"🔌 Plugin '{plugin_name}' not found."}
            plugin.initialize()
            result = plugin.run(input_text)
            plugin.shutdown()
            return result
        except Exception as e:
            return {"error": f"💥 Execution failed: {str(e)}"}
