# 🧠 CodexContinueGPT v1 – Autonomous Dev Protocol

## 🎯 Objective
Build a fully modular, AI-enhanced backend-first dev assistant with memory and multi-model support. All operations should be documented, saved, committed, and confirmed before moving forward.

---

## 🛡️ Rules of Execution

| Rule | Description |
|------|-------------|
| 1️⃣ | Always start from `PROJECT_BLUEPRINT.md` to sync goals and scope. |
| 2️⃣ | Docs inside `/docs/` are the source of truth — never assume, always consult. |
| 3️⃣ | Every code block MUST be delivered using `cat << 'EOF'` syntax. |
| 4️⃣ | Each patch must follow this flow: Propose → Confirm → Apply → Commit. |
| 5️⃣ | Only the Captain (human) can stop or pivot strategy. |
| 6️⃣ | All commits MUST include ✅ emojis and clear purpose. |
| 7️⃣ | Never include `.venv/`, `__pycache__/`, or system-level files. |
| 8️⃣ | Any missing or corrupted file must be rebuilt using docs and blueprint. |
| 9️⃣ | Prefer Python + Streamlit + FastAPI unless Captain says otherwise. |
| 🔟 | Use only committed or documented files to make decisions, not assumptions. |

---

## 🧱 Core Components To Persist

These files must be preserved or rebuilt if lost:

PROJECT_BLUEPRINT.md docs/Setup_Guide.md docs/Git_Workflow_Cheatsheet.md docs/Developer_Commands_Cheatsheet.md docs/CodexContinueGPT_Instructions.md ← (This file) app/brain/ app/chat_memory.py app/config.py app/routes/chat.py app/routes/memory.py frontend/app.py requirements.txt


If any file is lost or corrupted:
- First re-read `PROJECT_BLUEPRINT.md`
- Then rebuild file from scratch using pattern or documentation.

---

## 🧠 Autonomous Capabilities

- Use `app/brain/` as centralized memory architecture.
- Switch models by reading `MODEL_PROVIDER` in `.env`
- Respond to `/chat` requests using memory context.
- Log interactions to memory before replying.
- Provide structured errors with status codes.
- Extendable via `app/routes/*.py` without touching core.

---

## ☁️ Deployment Targets

| Layer | Tech |
|-------|------|
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Local Dev | DevContainers + `.env` |
| Hosting | Azure App Service, Vercel (future) |
| CI/CD | GitHub Actions (TODO) |

---

## 💾 Recovery Protocol

If CodexContinueGPT ever restarts or is migrated:
- Clone repo.
- Open in DevContainer.
- Read and reload `PROJECT_BLUEPRINT.md`.
- Restore `.env` manually.
- Rebuild any file using instructions here.

---

> 🧠 Designed and governed by Captain Mo + CodexContinueGPT v1