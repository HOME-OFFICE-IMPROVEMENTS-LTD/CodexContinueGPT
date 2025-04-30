# 🧠 CodexContinueGPT v1 – System Architecture (Alpha Blueprint)

CodexContinueGPT is the intelligence layer for CodexContinue — a full-stack AI IDE assistant platform inspired by Continue.dev and Cursor.com.

---

## 🧠 Core Brain Components

### 1. Memory Engine (✅ Done)
- Session memory + multi-turn
- Routes per `session_id`
- MemoryManager handles history + clearing

### 2. Model Router (🔜 Step 15)
- Supports: `openai`, `azure`, `ollama`, `tabbyml`
- Dynamically switches based on config or input
- Will use a pluggable class structure (`BaseModelProvider`)

### 3. Skill Tools (🔜 Future)
- Built-in toolkits (e.g., terminal agent, file browser, code runner)
- Tools registered dynamically
- Skills are exposed via `/skills` endpoint (LLM accessible)

---

## 🛠️ Frontend Assistant UX (Streamlit)

- Real-time streaming replies
- Sidebar model selector
- Token usage display
- Save/export chat logs

---

## 💡 Future Goals

- VSCode plugin
- SaaS user dashboard
- RAG + Semantic Search (LangChain-style agent)

---

> 📌 Anchored by CodexContinue Assistant — updated dynamically with every patch.
