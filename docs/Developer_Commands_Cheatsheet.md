# 🛠️ CodexContinue Developer Commands Cheatsheet

This page contains all important backend, frontend, Open Interpreter, and devcontainer commands.

---

## 🚀 Backend (FastAPI)

| Command | Purpose |
| :------ | :------ |
| `cd backend` | Move to backend folder |
| `source .venv/bin/activate` | Activate Python virtual environment |
| `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` | Start FastAPI server locally |
| `pytest` | Run backend tests |

---

## 🧠 Open Interpreter IO

| Command | Purpose |
| :------ | :------ |
| `app/io/agent_io.py` | Contains `CodexContinueIO` agent for OI interaction |
| `IO.ask_backend(message)` | Send chat message to FastAPI backend |
| `IO.remember(role, message)` | Add message to memory |
| `IO.history()` | Retrieve conversation history |
| `IO.clear()` | Clear session memory |
| `IO.introspect()` | Show internal session state |

> ✅ OI should call `IO.ask_backend(...)` directly to interact with the brain.

---

## 🖥️ Frontend (Streamlit)

| Command | Purpose |
| :------ | :------ |
| `cd frontend` | Move to frontend folder |
| `source ../.venv/bin/activate` | Activate venv if not already active |
| `streamlit run app.py` | Start frontend UI (Streamlit) |

---

## 🐳 DevContainer

| Command | Purpose |
| :------ | :------ |
| Open VSCode | Reopen folder in **Dev Container** |
| Automatic | All setup happens automatically inside the container |

---

## ⚡ Miscellaneous Useful

| Command | Purpose |
| :------ | :------ |
| `tree -L 2` | View project structure (2 levels deep) |
| `cat <filename>` | View file contents |
| `ls -la` | List all files with details |
| `exit` | Exit Python shell or deactivate venv |
| `deactivate` | Deactivate virtual environment |

---

> �� Keep this cheatsheet handy when developing!
> 📜 Updated by Captain MO + CodexContinue Assistant
