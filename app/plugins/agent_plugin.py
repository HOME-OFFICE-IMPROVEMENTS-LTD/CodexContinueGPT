# app/plugins/agent_plugin.py

from app.plugins.register_all import register_all_plugins

class AgentPlugin:
    def __init__(self):
        self.registry = register_all_plugins()

    def handle(self, message: str, session_id: str = "default") -> str:
        if message.startswith("/run "):
            parts = message.split(" ", 2)
            if len(parts) < 3:
                return "⚠️ Invalid /run format. Use: /run <plugin> <input>"

            _, plugin_name, input_data = parts
            plugin = self.registry.get(plugin_name)

            if not plugin:
                return f"❌ Plugin '{plugin_name}' not found"

            try:
                plugin.initialize()
                result = plugin.run(input_data)
                plugin.shutdown()
                return str(result)
            except Exception as e:
                return f"🔥 Error running plugin '{plugin_name}': {str(e)}"
        
        return None  # Not a plugin message — fallback to model
