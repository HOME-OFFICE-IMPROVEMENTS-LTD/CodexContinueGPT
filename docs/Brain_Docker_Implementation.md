# 🐳 CodexContinueGPT - Brain Docker Implementation

This document details how the Brain Architecture is implemented in Docker environments.

📅 Date: 2025-05-09  
👨‍✈️ Maintainer: Captain MO + CodexContinue Assistant  

---

## 🔍 Overview

This document extends [Brain_Architecture_Spec.md](Brain_Architecture_Spec.md) with Docker-specific implementation details.

---

## 🐳 Docker Brain Architecture

### Container Brain Architecture

```
+----------------------+       +----------------------+
| FastAPI Container    |       | Redis Container      |
| - Brain Service      |<----->| - Session State      |
| - Memory Manager     |       | - Message Cache      |
+----------------------+       +----------------------+
          |                              |
          v                              |
+----------------------+                 |
| SQLite/File Storage  |<----------------+
| - Long Term Memory   |
| - Configuration      |
+----------------------+
          |
          v
+----------------------+
| Ollama Container     |
| - Local LLM Models   |
| - Embeddings         |
+----------------------+
```

### Brain Components in Docker

| Component | Docker Implementation | Configuration |
|-----------|----------------------|---------------|
| Memory Manager | Backend container | Configurable via environment variables |
| Session Memory | Redis container | `REDIS_URL=redis://redis:6379` |
| Long Term Memory | Volume-mounted SQLite | `SQLITE_DB_PATH=/app/app/db/chat_memory.db` |
| LLM Gateway | Backend with external API calls | `MODEL_PROVIDER`, `OPENAI_API_KEY`, etc. |
| Ollama Integration | Dedicated container | `OLLAMA_BASE_URL=http://ollama:11434` |

---

## 🔄 Memory Flow in Docker

```text
Client Request
      |
      v
 +----------+     +---------+     +------------+
 | Frontend |---->| Backend |---->| Redis      |
 | (UI)     |<----| (API)   |<----| (Session)  |
 +----------+     +---------+     +------------+
                     |  |
              .------'  '-----.
              |               |
              v               v
      +------------+    +-----------+
      | SQLite DB  |    | Ollama    |
      | (Disk)     |    | (LLM)     |
      +------------+    +-----------+
```

---

## 📋 Development vs Production Mode

### Development Mode
- Hot code reloading
- Debug logs enabled
- Code mounted directly from host
- Redis persistence optionally disabled

### Production Mode
- Optimized container build
- Containerized code (no mounts)
- Redis persistence enabled
- Proper resource limits

---

## 🧠 Brain Environment Configuration

```python
# Example of environment-aware brain initialization
class BrainService:
    def __init__(self):
        self.env = os.getenv("ENV", "development")
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
        self.sqlite_path = os.getenv("SQLITE_DB_PATH", "/app/app/db/chat_memory.db")
        self.model_provider = os.getenv("MODEL_PROVIDER", "openai")
        
        # Initialize memory with Redis if available
        if self.redis_url:
            self.memory_manager = RedisMemoryManager(self.redis_url)
        else:
            self.memory_manager = InMemoryManager()
            
        # Initialize LLM gateway based on provider
        if self.model_provider == "ollama":
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
            self.llm = OllamaLLMGateway(ollama_url)
        else:
            self.llm = OpenAIGateway()
```

---

## 🚀 Implementation Notes

### Redis Memory Manager
- Uses Redis Hash sets for message storage
- Each session is a dedicated Hash key
- Messages serialized as JSON
- TTL set based on environment

### SQLite Long-term Storage
- Mounted as volume to persist across container restarts
- Schema includes tables for:
  - Sessions
  - Messages
  - Configuration
  - Metadata

### Ollama Integration
- Dedicated container for serving models
- Communicates over HTTP API
- Models downloaded on first use
- Cached for subsequent requests

## 🔧 Critical Configuration Details

### PYTHONPATH Configuration
- Set `PYTHONPATH=/app` in .env files
- Explicitly set in command execution: `PYTHONPATH=/app python app/db/init_db.py`
- Ensures proper module resolution for imports like `from app.db.models import Base`

### Dependency Management
- Development container needs explicit requirements.txt installation
- Added to .devcontainer/Dockerfile: `COPY requirements.txt . && pip install -r requirements.txt`
- Critical dependencies include:
  - SQLAlchemy for database access
  - FastAPI for web framework
  - Redis for session data
  - Uvicorn for ASGI server

### Container Build Process
- Development: Uses .devcontainer/Dockerfile with dev tools and requirements
- Production: Uses main Dockerfile with optimized dependencies
- Both standardized on Python 3.11 for consistency

---

> 🛡️ This implementation guide ensures the Brain architecture works seamlessly in both development and production Docker environments.
