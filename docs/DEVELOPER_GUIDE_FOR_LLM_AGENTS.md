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

