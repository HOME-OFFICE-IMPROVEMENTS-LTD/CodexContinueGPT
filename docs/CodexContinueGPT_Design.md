# 🧠 CodexContinueGPT v1 – Architecture Blueprint

## 🧭 Project Vision

CodexContinueGPT is a modular AI assistant framework, acting as a backend brain for developer tools like editors, terminals, SaaS dashboards, and agents. It integrates:

- 🤖 LLMs (OpenAI, Azure, Ollama, TabbyML)
- 🧠 Memory (Session + Vector Store)
- 🛠️ Plugin System (tools, APIs, agents)
- 📚 Prompt + System Context Libraries
- 🔌 OpenAPI & API-first interactions

---

## 🧱 Key Modules

| Module         | Purpose                                             |
|----------------|-----------------------------------------------------|
| `brain/`       | Memory management (RAM/Vector stores)               |
| `plugins/`     | Tools + APIs (search, shell, docs, GitHub)          |
| `prompts/`     | Prompt engineering + system messages                |
| `router/`      | FastAPI endpoints (LLM/chat/tools/stream)           |
| `frontend/`    | Streamlit dashboard (chat + UI playground)          |
| `runtime/`     | Execution queue, event loop, agent interface        |

---

## 🔄 LLM Agent Flow

1. Receive message input
2. Retrieve memory context
3. Match tools/plugins
4. Construct prompt (system + memory + user)
5. Call LLM via AsyncOpenAI or Ollama
6. Store memory + reply
7. Return assistant response

---

## 📊 Data Layer

- **SessionMemory:** In-RAM dict (by user/session)
- **Vector Store:** For long-term memory (Future: FAISS, Weaviate)
- **Logging + Tracing:** Persist conversations per agent

---

## 🚦 LLM Providers

| Provider    | SDK           | Notes                             |
|-------------|---------------|-----------------------------------|
| OpenAI      | `openai`      | Already integrated (GPT-3.5/4)    |
| Azure OpenAI| `openai`      | Just add endpoint in `.env`       |
| Ollama      | REST API      | Local fallback support            |
| TabbyML     | REST / socket | Self-hosted autocomplete (TBD)    |

---

## 📜 Environment Setup (Recap)

- `.env` for LLM keys, models, endpoints
- Devcontainer already supports Python 3.10, FastAPI, Streamlit

---

## 🧩 Future Modules

- `codexctl` – CLI assistant with memory
- `github-agent` – PR reviewer bot
- `notebook-agent` – Jupyter-enhanced assistant
- `shell-agent` – Terminal-native Codex bot
- `metrics/` – Logging, analytics, rate-limiting
- `test/` – Unit, integration, memory tests

---

> 🎙️ Lead Architect: CodexContinue Assistant v1  
> 📅 Generated: [$(date "+%Y-%m-%d")]  
> 🔒 Anchored for every future step

