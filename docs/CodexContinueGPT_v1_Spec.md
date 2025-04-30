# 🧠 CodexContinueGPT v1 - AI Brain Design Spec

This is the architectural blueprint for the **CodexContinueGPT v1** core engine — the brain that powers the assistant.

---

## 🧩 Component Overview

| Module               | Description |
|----------------------|-------------|
| `routes/chat.py`     | Chat endpoint that sends messages to LLMs |
| `chat_memory.py`     | Stores and retrieves messages per session |
| `brain/`             | Main memory manager and storage plugins |
| `memory/`            | Strategy modules: short, long, hybrid |
| `services/`          | Integrations (OpenAI, Azure, Ollama, RAG) |
| `models/chat_models.py` | Pydantic models for validation |
| `config.py`          | Secrets + dynamic provider configs |

---

## 🧠 Memory Strategy

We use **layered memory architecture**:

- 🧠 **ShortTermMemory**: volatile, recent messages (context window)
- 🗄️ **LongTermMemory**: searchable knowledge (embedding-based, DB)
- 🔄 **SessionMemory**: full history of active chat (persistable)
- 🎛️ **MemoryManager**: dynamic routing + session ID control

---

## 🔌 Model Routing Strategy

CodexContinueGPT supports **multi-provider LLM backend switching**.

### Supported Providers
| Provider      | Integration File       | Models                     |
|---------------|------------------------|----------------------------|
| `OpenAI`      | `services/openai.py`   | `gpt-3.5`, `gpt-4`         |
| `AzureOpenAI` | `services/azure.py`    | `deployment_name`, etc.   |
| `Ollama`      | `services/ollama.py`   | `llama2`, `codellama`, etc.|

**Auto-detects and uses correct handler** based on config or `MODEL_PROVIDER` env var.

---

## 🧪 Inference Pipeline (Simplified Flow)

```mermaid
graph TD
    A[User Input] --> B[chat.py]
    B --> C[ChatMemory.add()]
    B --> D[MemoryManager.get_context()]
    D --> E[Model Router: OpenAI/Azure/Ollama]
    E --> F[ChatCompletion.create()]
    F --> G[Response]
    G --> H[ChatMemory.add() assistant reply]
    H --> I[Return to frontend]

⚙️ Environment Variables
Put these in .env locally:
   OPENAI_API_KEY=sk-xxx
   MODEL_PROVIDER=openai
   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
   AZURE_DEPLOYMENT_NAME=gpt-4-deployment
   OLLAMA_HOST=http://localhost:11434


✅ Best Practices (Enforced by Design)
🔁 Stateless backend with session-based memory routing

✅ All routes must validate request data via chat_models.py

🔐 No secrets hardcoded — all via .env

🧱 Modular + extensible — easy to add Claude, Mistral, etc.

🔬 Ready for RAG, vector search, and agents in Phase 2

Built for developers, powered by memory, and designed to never forget again.
— CodexContinueGPT Team


   
    



