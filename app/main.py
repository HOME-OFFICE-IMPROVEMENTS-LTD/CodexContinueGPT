# app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from app.routes.memory import router as memory_router
from datetime import datetime

app = FastAPI(
    title="CodexContinue API",
    description="An AI-powered developer assistant backend.",
    version="0.2.0",
)

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers properly
app.include_router(chat_router)
app.include_router(memory_router)

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
