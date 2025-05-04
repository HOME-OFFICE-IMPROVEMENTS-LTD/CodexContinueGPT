# app/brain/planner_agent.py

from app.plugins.register_all import register_all_plugins
from app.services.model_loader import ModelLoader
from app.chat_memory import get_short_memory

class PlannerAgent:
    def __init__(self):
        self.registry = register_all_plugins()
        self.model = ModelLoader()

    async def route(self, message: str, session_id: str) -> str:
        if message.strip().lower().startswith("run "):
            parts = message.strip().split(maxsplit=2)
            if len(parts) < 3:
                return "⚠️ Usage: run <plugin> <input>"
            plugin_name, input_text = parts[1], parts[2]
            plugin = self.registry.get(plugin_name)
            if not plugin:
                return f"⚠️ Plugin '{plugin_name}' not found"
            plugin.initialize()
            result = plugin.run(input_text)
            plugin.shutdown()
            return str(result)

        # ✅ Fallback: use LLM
        messages = await get_short_memory(session_id)
        return await self.model.chat(messages)
