from app.memory.session_memory import SessionMemory
from app.memory.short_term_memory import ShortTermMemory
from app.memory.long_term_memory import LongTermMemory

class MemoryManager:
    def __init__(self):
        self.session = SessionMemory()
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()

    def reset_all(self):
        self.session.clear_memory()
        # Optionally clear short/long memory (advanced)
