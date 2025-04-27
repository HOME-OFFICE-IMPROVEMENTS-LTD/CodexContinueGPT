# 🛠️ CodexContinue Developer Commands Cheatsheet

This page contains all important backend, frontend, and devcontainer commands.

---

## 🚀 Backend (FastAPI)

| Command | Purpose |
| :------ | :------ |
| `cd backend` | Move to backend folder |
| `source .venv/bin/activate` | Activate Python virtual environment |
| `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` | Start FastAPI server locally |
| `pytest` | Run backend tests |

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

> 📚 Keep this cheatsheet handy when developing!
> 📜 Updated by Captain MO + CodexContinue Assistant
