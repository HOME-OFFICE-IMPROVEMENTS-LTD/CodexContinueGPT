from app.plugins.registry import PluginRegistry
from app.plugins.register_all import register_all_plugins

class PlannerAgent:
    def __init__(self):
        self.registry = register_all_plugins()

    async def route(self, user_input: str, session_id: str) -> dict:
        # Try matching a plugin name in the input
        for name, plugin in self.registry.all().items():
            if name in user_input.lower():
                return plugin.run(user_input)

        # Fallback to Ollama if no match
        try:
            fallback = self.registry.get("ollama_fallback")
            return fallback.run(user_input)
        except Exception as e:
            return {"error": f"Plugin fallback failed: {str(e)}"}
