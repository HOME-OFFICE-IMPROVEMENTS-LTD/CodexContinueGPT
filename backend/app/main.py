from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes.memory import router as memory_router

app = FastAPI(
    title="CodexContinue API",
    description="An AI-powered developer assistant backend.",
    version="0.2.0",
)

# ✅ Include routers properly
app.include_router(chat_router)
app.include_router(memory_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CodexContinue API 🚀"}

@app.get("/health")
def health_check():
    return {"status": "API is healthy"}

@app.get("/version")
def get_version():
    return {"version": app.version}

@app.get("/openapi")
def get_openapi():
    return app.openapi()
