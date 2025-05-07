# app/plugins/agent_plugin.py

from app.plugins.register_all import register_all_plugins
from app.db.sqlite_conn import get_db
from datetime import datetime

class AgentPlugin:
    def __init__(self):
        self.registry = register_all_plugins()

    async def handle(self, message: str, session_id: str) -> str | None:
        if not message.lower().startswith("run "):
            return None

        parts = message.strip().split(maxsplit=2)
        if len(parts) < 3:
            return "⚠️ Usage: run <plugin> <input>"

        plugin_name, plugin_input = parts[1], parts[2]
        plugin = self.registry.get(plugin_name)

        if not plugin:
            return f"⚠️ Plugin '{plugin_name}' not found"

        plugin.initialize()
        result = plugin.execute(plugin_input)
        plugin.shutdown()

        # ✅ Async logging to plugin_logs
        try:
            from sqlalchemy import text
            insert_sql = text("""
                INSERT INTO plugin_logs (plugin, input, output, session_id)
                VALUES (:plugin, :input, :output, :session_id)
            """)
            async with get_db() as db:
                await db.execute(insert_sql, {
                    "plugin": plugin_name,
                    "input": plugin_input,
                    "output": str(result),
                    "session_id": session_id
                })
                await db.commit()
        except Exception as e:
            print(f"⚠️ Failed to log plugin execution: {e}")

        return result
