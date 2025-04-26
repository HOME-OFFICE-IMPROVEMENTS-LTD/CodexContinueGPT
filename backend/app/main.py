from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes.memory import router as memory_router  # ✅ Import memory router

app = FastAPI(
    title="CodexContinue API",
    description="An AI-powered developer assistant backend.",
    version="0.2.0",
)

# ✅ Include routers
app.include_router(chat_router)
app.include_router(memory_router)

@app.get("/")
def read_root():
    """Root welcome page."""
    return {"message": "Welcome to CodexContinue API 🚀"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "API is healthy"}

@app.get("/version")
def get_version():
    """Get the current version of the API."""
    return {"version": app.version}

@app.get("/openapi")
def get_openapi():
    """Get the OpenAPI JSON schema."""
    return app.openapi()

@app.get("/docs")
def get_docs():
    """Get the Swagger UI documentation."""
    return {"docs": "/docs"}

@app.get("/redoc")
def get_redoc():
    """Get the ReDoc documentation."""
    return {"redoc": "/redoc"}

@app.get("/favicon.ico")
def get_favicon():
    """Get the favicon."""
    return {"favicon": "/favicon.ico"}



