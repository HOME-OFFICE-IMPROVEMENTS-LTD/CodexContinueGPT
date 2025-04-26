# backend/app/chat_memory.py

class ChatMemory:
    def __init__(self):
        # 🧠 In-memory storage per session
        self.sessions = {}

    def add_message(self, session_id: str, role: str, content: str):
        """Add a new message to the memory for a given session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({"role": role, "content": content})

    def get_messages(self, session_id: str):
        """Retrieve all messages from memory for a given session."""
        return self.sessions.get(session_id, [])

    def clear_memory(self, session_id: str):
        """Clear all memory for a given session."""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self):
        """List all active session IDs."""
        return list(self.sessions.keys())

# ✅ Create the single shared memory instance
memory = ChatMemory()
