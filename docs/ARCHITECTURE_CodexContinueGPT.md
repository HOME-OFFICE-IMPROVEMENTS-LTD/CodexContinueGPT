# 🧠 CodexContinueGPT v1 - Architecture Blueprint

📅 Date: 2025-04-30  
👨‍✈️ Maintainer: Captain MO + CodexContinue Assistant  

---

## 🎯 Purpose

CodexContinueGPT v1 is the intelligence core of the CodexContinue platform.  
It combines multi-LLM chat orchestration, memory routing, plugin/tool calling, and fast developer response generation.

---

## 🧩 System Overview

+---------------------+ | Streamlit UI | <--- User Input / Reply Stream +---------------------+ | v +---------------------+ | FastAPI Router | | (/chat, /memory) | +---------------------+ | v +-------------------------+ | 🧠 MemoryManager | --> Session and history control +-------------------------+ | v +-------------------------+ | 🤖 LLM Gateway (Brain) | | - OpenAI / Azure | | - Ollama / TabbyML | +-------------------------+ | v +-------------------------+ | 🔌 Tool/Plugin System | | - Shell Tools | | - File/Code Utils | | - Data Analysis Tools | +-------------------------+

yaml
Copy
Edit

---

## 📦 Core Modules

### 1. `app/brain/`
- `memory_manager.py`: Handles per-session message storage
- `storage.py`: Future DB/Redis swap backend

### 2. `app/routes/`
- `chat.py`: Central async router for all user input
- `memory.py`: Manual control over memory sessions

### 3. `app/services/`
- `llm_service.py`: Handles model-specific calls
- `tool_runner.py`: (Planned) Executes shell/file commands

---

## 🔁 LLM Flow (Async)

1. UI input triggers `/chat` POST
2. Message is stored in `MemoryManager`
3. LLM selected based on `MODEL_PROVIDER`
4. LLM response fetched and parsed
5. Reply saved into memory and returned

---

## 🚀 Roadmap Features

- [ ] LLM selector from `.env`: `openai`, `azure`, `ollama`, `tabbyml`
- [ ] Streaming response support (via SSE or WebSocket)
- [ ] User-uploaded file tools (e.g., CSV summary, file Q&A)
- [ ] Tool-calling (plugin-style structure)
- [ ] Memory export/import (JSON)

---

## 🧠 Memory Options

| Type        | Description                       |
|-------------|-----------------------------------|
| Short-term  | In-memory dict (current default)  |
| Long-term   | File-based or Redis (TBD)         |
| Session     | One per user (UUID from Streamlit)|

---

> 🛡️ This architecture will grow with you.  
> All future agents, copilots, and codexes will respect this contract.

