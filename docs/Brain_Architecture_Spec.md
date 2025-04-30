# 🧠 CodexContinueGPT v1 - Brain Architecture

This document defines the core design of the AI assistant "brain" for CodexContinueGPT.

---

## 🔍 Purpose

CodexContinueGPT is an intelligent, pluggable assistant engine built to:

- Retain and route memory across conversations
- Support different memory strategies (short-term, long-term, hybrid)
- Switch between LLMs (OpenAI, Azure, Ollama, TabbyML)
- Prepare for RAG + embedding search
- Run across sessions and users

---

## 🧱 Memory Layer Design

### 1. `SessionMemory` (Short-Term)
- Stores active session history in RAM
- Clears per-session or on request
- Used for quick prompt replay

### 2. `LongTermMemory` (Disk or Vector DB)
- Persists across sessions
- Optional file-based or vector-based memory
- Integrates with future RAG engines

### 3. `MemoryManager`
- Central controller
- Routes reads/writes to short/long memory
- Offers methods like:
    ```python
    memory.add_message(session_id, role, message)
    memory.get_messages(session_id)
    memory.clear_session(session_id)
    memory.list_sessions()
    ```

---

## 🔄 Memory Flow

```text
           +----------------------+
Input ---> | MemoryManager        |
           +----------------------+
                  |      |
          .-------'      '--------.
          |                        |
  +---------------+      +----------------+
  | SessionMemory |      | LongTermMemory |
  +---------------+      +----------------+
          |                        |
       (chat replay)       (RAG / history / journaling)
