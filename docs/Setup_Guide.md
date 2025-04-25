# 🛠️ Developer Setup Guide for CodexContinue

This document helps new contributors spin up the project fast!

---

## 🖥️ Prerequisites
- VSCode (with DevContainers extension)
- Docker Desktop installed and running
- Git + GitHub Account
- (Optional) Azure, AWS account for deployment testing

---

## 🧱 Local Setup (First Time)

1. **Clone the Repo**
    ```bash
    git clone https://github.com/YOUR-ORG/CodexContinue.git
    cd CodexContinue
    ```

2. **Open in VSCode**
    - Reopen in container (Dev Container will automatically build)
  
3. **Install Backend Requirements**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

4. **Run FastAPI Server**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

5. **(Future) Run Frontend**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---

## ☁️ Deployment Preview

When ready to deploy:
- **Backend**: Docker build + push or use Azure WebApp
- **Frontend**: Vercel, Netlify, Azure Static WebApps
- **CI/CD**: GitHub Actions (test + deploy)

---

## 🌐 Environment Variables

- `OPENAI_API_KEY` (required)
- `AZURE_OPENAI_ENDPOINT` (optional, for Azure support)
- `MODEL_PROVIDER` (e.g., "openai" or "ollama")

**Put them inside `.env` files locally and in the cloud.**

---

> 🚀 Happy hacking, Captain!
