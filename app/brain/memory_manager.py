# backend/app/brain/memory_manager.py

from typing import List, Dict
from app.brain.storage import MemoryStorage

class MemoryManager:
    def __init__(self):
        self.storage = MemoryStorage()

    def add_message(self, session_id: str, role: str, content: str):
        """Add a new message to the session."""
        messages = self.storage.load_session(session_id)
        messages.append({"role": role, "content": content})
        self.storage.save_session(session_id, messages)

    def get_messages(self, session_id: str) -> List[Dict[str, str]]:
        """Retrieve all messages for a session."""
        return self.storage.load_session(session_id)

    def clear_session(self, session_id: str):
        """Clear all messages for a session."""
        self.storage.clear_session(session_id)

    def list_sessions(self) -> List[str]:
        """List all active session IDs."""
        return self.storage.list_sessions()
