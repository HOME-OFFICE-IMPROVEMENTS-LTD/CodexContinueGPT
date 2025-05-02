# 🧠 Developer Guide for LLMs, Agents, and Copilots
(For CodexContinue or ANY future project based on it)

## 📜 Purpose
- Understand the project structure
- Respect and update PROJECT_BLUEPRINT.md
- Develop features modularly and safely

## 📂 Repo Structure Summary
- backend/
- frontend/
- docs/

## 🚀 How to Start
1. Open in Dev Container
2. Run backend locally:
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
3. Access docs at:
   http://localhost:8000/docs

## 🧪 Testing
To run tests:
   cd backend
   pytest

## 🛡️ LLM Agent Guidelines
- Always check PROJECT_BLUEPRINT.md before suggesting edits
- Avoid duplicating logic, keep prompts modular
- Document new features inside docs/ folder
- Log interaction formats to aid tracing/debugging
- Keep secrets and keys out of source code

## 🌍 Future Enhancements
- Frontend UI (React, Next.js, or Streamlit)
- Multiple LLM backend integrations (OpenAI, Ollama, Azure)
- Chat history persistence
- RBAC and authentication
- Deployment automation (CI/CD, Docker, Azure)


---

## 🧠 Why We Introduced Memory Agents (`MemoryManager`, `SessionMemory`, etc.)

To ensure consistent replies across messages, multi-turn chats, and tool plugins, we introduced a **layered memory system** to the architecture:

### 🔍 Problem Before
- Messages were passed statelessly — each chat had no memory of the last.
- No reliable way to simulate agent context or multi-turn reasoning.
- Chatbots forgot what the user said in the last message.

### ✅ Solution: Memory Layers

| Layer             | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `SessionMemory`   | Temporary in-RAM memory for a specific user session (UUID-based).       |
| `LongTermMemory`  | Disk or vector database-based storage for persistent knowledge.         |
| `MemoryManager`   | The controller that routes memory access and provides a clean interface.|

### 🧩 Design Benefits
- 🔁 **Multi-Turn**: Keeps the chat history alive across messages
- 📂 **Session-Based**: Each user/chat session has isolated memory
- 🔍 **Tool Routing**: Tools (e.g., RAG, search) can fetch context
- 🧼 **Clean API**: Standard methods like `add_message()`, `clear_session()`, etc.

### 💡 Why This Matters
Future copilots (e.g., `codexctl`, `shell-agent`, `notebook-agent`) **require memory consistency** to work properly. This abstraction layer makes memory portable, replaceable (e.g., upgrade to Redis), and LLM-agnostic.

---

> 📌 All agents and LLMs must access session memory through `MemoryManager`.  
> ❗ Never store chat state manually — always use the proper interfaces.
