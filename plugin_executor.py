from app.plugins.register_all import register_all_plugins
from app.memory.sqlite import get_sqlite_connection
from datetime import datetime

class PluginExecutor:
    def __init__(self):
        self.registry = register_all_plugins()

    def list_plugins(self):
        return list(self.registry.all().keys())

    def execute_plugin(self, plugin_name: str, input_data: str, session_id: str) -> dict:
        plugin = self.registry.get(plugin_name)
        if not plugin:
            return {"error": f"Plugin '{plugin_name}' not found"}

        try:
            plugin.initialize()
            result = plugin.execute(input_data)
            plugin.shutdown()
        except Exception as e:
            result = {"error": str(e)}

        try:
            conn = get_sqlite_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO plugin_logs (plugin, input, output, session_id, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (
                plugin_name,
                input_data,
                str(result),
                session_id,
                datetime.utcnow().isoformat()
            ))
            conn.commit()
        except Exception as log_error:
            print(f"⚠️ Failed to log plugin execution: {log_error}")

        return result
