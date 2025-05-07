# app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.routes.chat import router as chat_router
from app.routes.memory import router as memory_router
from app.routes.plugin_routes import router as plugin_router
from app.routes.sessions import router as sessions_router
from app.routes.tools import router as tools_router
from app.routes.memory_audit import router as memory_audit_router
from app.routes.tools import router as tools_router
from app.routes import plugin_logs

app = FastAPI(
    title="CodexContinue API",
    description="An AI-powered developer assistant backend.",
    version="0.2.0",
)

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register all API routes
app.include_router(chat_router)
app.include_router(memory_router)
app.include_router(plugin_router)
app.include_router(sessions_router)
app.include_router(tools_router)
app.include_router(memory_audit_router)
app.include_router(tools_router)
app.include_router(plugin_logs.router)

# ✅ Register all plugins

# ✅ Base endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to CodexContinue API 👋"}

@app.get("/health")
def health_check():
    return {
        "status": "API is healthy",
        "server_time": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/version")
def get_version():
    return {"version": app.version}

@app.get("/openapi")
def get_openapi():
    return app.openapi()
