from fastapi import APIRouter
from app.memory.sqlite import get_sqlite_connection

router = APIRouter()

@router.get("/plugin-logs/{session_id}")
def get_plugin_logs(session_id: str):
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, plugin, input, output, log_message
        FROM plugin_logs
        WHERE session_id = ?
        ORDER BY timestamp DESC
    """, (session_id,))
    rows = cursor.fetchall()

    columns = ["id", "timestamp", "plugin", "input", "output", "log_message"]
    logs = [dict(zip(columns, row)) for row in rows]

    return {"logs": logs}
