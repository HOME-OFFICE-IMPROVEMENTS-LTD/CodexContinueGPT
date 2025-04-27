# backend/app/brain/storage.py

from typing import Dict, List

class MemoryStorage:
    def __init__(self):
        # 🧠 Simple in-memory storage (temporary, later will add disk or db)
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    def load_session(self, session_id: str) -> List[Dict[str, str]]:
        """Load messages for a given session ID."""
        return self.sessions.get(session_id, [])

    def save_session(self, session_id: str, messages: List[Dict[str, str]]):
        """Save messages for a given session ID."""
        self.sessions[session_id] = messages

    def clear_session(self, session_id: str):
        """Clear messages for a given session ID."""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self) -> List[str]:
        """List all session IDs."""
        return list(self.sessions.keys())
