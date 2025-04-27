from typing import List

class SessionMemory:
    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_memory(self) -> List[dict]:
        return self.messages

    def clear_memory(self):
        self.messages = []
