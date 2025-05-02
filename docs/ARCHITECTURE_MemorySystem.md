# 🧠 CodexContinueGPT v1 – Memory System Architecture

This document outlines the design of the hybrid memory system powering CodexContinueGPT v1.

---

## 📚 Memory Architecture Components

### 1. 🧠 Short-term Memory (In-Memory)
- Volatile, per-session data (e.g., user messages).
- Fastest access.
- Reset per session or on expiration.

### 2. 📦 Long-term Memory (Persistent)
- Stored on disk (SQLite/JSON) or via database.
- Used for structured knowledge, configs, agent memory.
- Accessible across sessions.

### 3. 🧠 External Memory (Vector DB)
- Used for similarity search via embeddings.
- Integrates Pinecone, ChromaDB, etc.
- Ideal for semantic memory or doc retrieval.

---

## 🧪 Python API Example

class MemorySystem:
    def __init__(self):
        self.short_term_memory = {}  # In-memory store
        self.long_term_storage = LongTermStorage()
        self.external_memory = ExternalMemoryService()

    def store_short_term(self, context_id, data):
        self.short_term_memory[context_id] = data

    def retrieve_short_term(self, context_id):
        return self.short_term_memory.get(context_id)

    def store_long_term(self, key, data):
        self.long_term_storage.save(key, data)

    def retrieve_long_term(self, key):
        return self.long_term_storage.load(key)

    def store_external_memory(self, vector, metadata):
        self.external_memory.store(vector, metadata)

    def retrieve_external_memory(self, query_vector):
        return self.external_memory.search(query_vector)

    def prioritize_context(self, query):
        context = []
        if st := self.retrieve_short_term(query):
            context.append((st, "short_term"))
        if lt := self.retrieve_long_term(query):
            context.append((lt, "long_term"))
        for item in self.retrieve_external_memory(query) or []:
            context.append((item, "external"))
        return self.custom_prioritization_logic(context)

    def custom_prioritization_logic(self, context_list):
        return sorted(
            context_list,
            key=lambda x: ("short_term", "long_term", "external").index(x[1])
        )
🧱 Stub Storage Interfaces
class LongTermStorage:
    def save(self, key, data): pass
    def load(self, key): return None

class ExternalMemoryService:
    def store(self, vector, metadata): pass
    def search(self, query_vector): return []

🧠 Prioritization Strategy
Recency / Session Relevance

Short-term memory first.

Persistence Importance

Long-term memory retains essential state/config.

Semantic Similarity

External memory handles similarity search.

Custom Rules

You define weights, thresholds, and heuristics.

✅ Architecture Anchored – Ready for Implementation Phase