# 🚀 CodexContinue - AI Dev Assistant Platform Blueprint

## 🎯 Purpose

This repository is for building **CodexContinue**, your own self-hosted AI development assistant platform — inspired by **Continue.dev** and **Cursor.com**.

The backend and frontend combined will:

- Offer an **AI-powered in-editor assistant**
- Support **Free / Pro / Business** pricing plans
- Be completely containerized (via Dev Containers)
- Be suitable for **local development** and **cloud deployment** (Azure, AWS, VPS)
- Support multiple LLMs (OpenAI, Azure OpenAI, Ollama, TabbyML, etc.)

---

## 📂 Full Project Structure (Detailed)

\`\`\`
CodexContinue/
├── .devcontainer/                     # VSCode Remote Container config
│   └── devcontainer.json              # - Defines container setup
├── .vscode/                           # VSCode tasks and debugger
│   ├── launch.json                    # - Debugger config
│   └── tasks.json                     # - CLI tasks
├── .github/workflows/                 # CI/CD Workflows (GitHub Actions)
│   ├── deploy-backend.yml             # - Deployment workflow (coming soon)
│   └── test.yml                       # - Run lint/tests on PRs
├── backend/                           # FastAPI Application (LLM Gateway)
│   ├── app/                           #   - Core FastAPI source code
│   │   ├── main.py                    #     - App root & router includes
│   │   ├── routes/                    #     - API endpoints (chat, auth...)
│   │   ├── services/                  #     - GPT, LLM service wrappers
│   │   └── utils/                     #     - Helper functions
│   ├── requirements.txt               #   - Python dependencies
│   ├── Dockerfile                     #   - Optional containerization
│   └── tests/                         #   - Unit & integration tests
├── frontend/                          # Frontend Web Interface (TBD)
│   └── README.md                      # Placeholder (React, Streamlit, etc.)
├── docs/                              # Internal docs & business strategy
│   ├── SaaS_Plans.md                  # Pricing model: Free, Pro, Business
│   └── Setup_Guide.md                 # Dev onboarding / architecture
├── README.md                          # General readme
└── PROJECT_BLUEPRINT.md               # 🔥 Permanent memory anchor (this file)
\`\`\`

---

## 🌐 Deployment Options

- Azure App Service (Python or Docker)
- AWS EC2 / Lightsail
- Fly.io / Railway.app / Render
- Docker Compose for local testing
- GitHub Codespaces or Dev Container

---

## 💳 SaaS Tiers (From \`docs/SaaS_Plans.md\`)

| Plan     | Description                         | Features                                 |
| -------- | ----------------------------------- | ---------------------------------------- |
| Free     | Limited usage + OpenAI keys only    | Chat, Autocomplete, Docs                 |
| Pro      | Unlimited LLM access + local models | All features + local Ollama, TabbyML     |
| Business | Team support, APIs, telemetry       | Org dashboards, Azure OpenAI, API tokens |

---

## 🔥 Status Tracker

- Milestone achieved: Conversational shell agents supported as of 2025-05-03.

- [x] Devcontainer Setup
- [x] Backend running with FastAPI
- [ ] Frontend UI starter (TBD)
- [ ] CI/CD pipelines (GitHub Actions)
- [ ] Multi-LLM integration (Azure OpenAI, Ollama)
- [ ] Billing Integration (Stripe/Fake API)
- [ ] Full SaaS Launch

---

## 💡 Long-Term Goals

- Real-time chat UI (Next.js or Streamlit)
- Workspace memory + chat history per user
- Multi-model routing (e.g., GPT-4, Mistral, Claude)
- Local LLM fallback (Ollama, TabbyML)
- VSCode Extension integration
- Full telemetry, analytics, and monitoring

---

## 🧠 Developer Notes

- This blueprint is **always up to date** with your real intent
- It is the single source of truth for current progress
- Any LLM reading this file will instantly know your project direction
- All copilots (GitHub Copilot, Cursor, TabbyML, Ollama) will **read this first** when helping.

---

> 🛡️ Saved by Captain Mo + Copilot. Updated: 2025

🧠 Milestone — 2025-05-04
- Real-time `/chat` plugin dispatch enabled via PluginAgent.
- Chat endpoint parses `/run <plugin> <input>` before calling LLM.
- Memory logging and plugin middleware are now unified.