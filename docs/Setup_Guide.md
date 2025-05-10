# 🛠️ Developer Setup Guide for CodexContinue

📅 Date: 2025-05-09 (Updated)  
👨‍✈️ Maintainer: Captain MO + CodexContinue Assistant

This document helps new contributors spin up the project fast!

---

## 🖥️ Prerequisites
- VSCode (with DevContainers extension)
- Docker Desktop installed and running
- Git + GitHub Account
- Python 3.10+ (for non-Docker setup)
- Node.js 18+ (for frontend development)
- (Optional) Azure, AWS account for deployment testing

---

## 🧱 Local Setup (First Time)

1. **Clone the Repo**
    ```bash
    git clone https://github.com/YOUR-ORG/CodexContinue.git
    cd CodexContinue
    ```

2. **Option 1: Using VS Code Dev Container (Recommended)**
    - Open in VS Code
    - Install the Dev Containers extension if not already installed
    - Click "Reopen in Container" or run the "Dev Containers: Reopen in Container" command
    - Wait for the container to build (this will install all dependencies automatically)

3. **Option 2: Using Docker Compose**
    ```bash
    # For development environment
    ./scripts/switch_env.sh dev
    docker-compose build
    docker-compose up -d
    
    # For production environment
    ./scripts/switch_env.sh prod
    docker-compose build
    docker-compose up -d
    ```
    
4. **Option 3: Manual Setup (Without Docker)**
    ```bash
    # Create and activate virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install backend dependencies
    pip install -r requirements.txt
    
    # Initialize the database
    python app/db/init_db.py
    
    # Set PYTHONPATH
    export PYTHONPATH=$PYTHONPATH:$(pwd)  # On Windows: set PYTHONPATH=%PYTHONPATH%;%CD%
    
    # Run FastAPI Server
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    
    # In another terminal, run Streamlit frontend
    cd frontend
    pip install -r requirements.txt
    streamlit run app.py
    ```

---

## ☁️ Deployment Preview

When ready to deploy:
- **Backend**: Docker build + push or use Azure WebApp
- **Frontend**: Deploy Streamlit app to Streamlit Cloud or Azure Static WebApps
- **CI/CD**: GitHub Actions (test + deploy)

### Quick Azure Deployment

```bash
# Login to Azure
az login

# Create resource group
az group create --name codex-continue-rg --location eastus

# Deploy container app
az containerapp up \
  --name codex-continue \
  --resource-group codex-continue-rg \
  --environment codex-continue-env \
  --source . \
  --ingress external \
  --target-port 8000 \
  --env-vars PYTHONPATH=/app MODEL_PROVIDER=azure
```

See [DOCKER.md](/DOCKER.md) for more deployment options and configurations.

---

## 🌐 Environment Variables

### Core Variables
- `OPENAI_API_KEY` (required if using OpenAI)
- `AZURE_OPENAI_ENDPOINT` (optional, for Azure support)
- `AZURE_OPENAI_API_KEY` (optional, for Azure support)
- `MODEL_PROVIDER` (e.g., "openai", "ollama", "azure")

### Docker Variables (Added: 2025-05-09)
- `ENV` - Sets the environment mode (development/production)
- `DOCKERFILE_PATH` - Which Dockerfile to use
- `MOUNT_CODE` - Whether to mount code into container
- `RELOAD` - Enable/disable hot reload
- `PYTHONPATH` - Set to /app for proper module imports
- `REDIS_URL` - Connection string for Redis (default: redis://redis:6379)
- `SQLITE_DB_PATH` - Path to SQLite database (default: /app/app/db/chat_memory.db)
- `OLLAMA_BASE_URL` - URL for Ollama LLM server (default: http://ollama:11434)

**Put them inside `.env` files locally, or use provided `.env.development` and `.env.production` files.**

## 🐳 Docker Configuration (Added: 2025-05-09)

For Docker-based development and deployment, refer to [DOCKER.md](/DOCKER.md) with comprehensive information on:

- Development vs Production environments
- Environment switching with `./scripts/switch_env.sh`
- Container structure and configuration
- Redis and Ollama integration
- VS Code tasks for Docker operations

---

## 🧪 Testing

Run the test suite to verify your setup:

```bash
# Using Docker
docker-compose exec backend pytest

# Without Docker
pytest
```

### Key Test Files
- `tests/test_plugin_manager.py` - Tests for plugin loading and execution
- `tests/test_memory_audit.py` - Memory system tests
- `tests/test_planner_agent.py` - Agent planning tests

## 🔍 Troubleshooting

### Common Issues

1. **Module Import Errors**
   - Ensure PYTHONPATH includes the project root
   - For Docker: PYTHONPATH is set in docker-compose.yml
   - For manual setup: export PYTHONPATH=$PYTHONPATH:$(pwd)

2. **Redis Connection Issues**
   - Check that Redis is running: `docker ps | grep redis`
   - Verify connection URL in environment variables

3. **Ollama Model Loading**
   - Ensure models are pulled: `docker-compose exec ollama ollama pull codellama`
   - Check Ollama logs: `docker-compose logs ollama`

4. **DevContainer Not Building**
   - Check Docker daemon is running
   - Try rebuilding: `Dev Containers: Rebuild Container`

## 📚 Optional Useful Resources

- [🛠️ Git Workflow Cheatsheet](Git_Workflow_Cheatsheet.md)
- [🛠️ Developer Commands Cheatsheet](Developer_Commands_Cheatsheet.md)
- [🔌 Plugin API Integration Guide](Plugin_API_Integration_Guide.md)
- [🧠 Brain Architecture Spec](Brain_Architecture_Spec.md)

---

> 🚀 Happy hacking, Captain!
