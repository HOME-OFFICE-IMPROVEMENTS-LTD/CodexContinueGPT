FROM mcr.microsoft.com/devcontainers/python:3.11

# Install Uvicorn + FastAPI deps
RUN pip install --upgrade pip && pip install fastapi uvicorn openai python-dotenv

# Optional: expose port for API
EXPOSE 8000
