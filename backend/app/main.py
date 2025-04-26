from fastapi import FastAPI
from app.routes.chat import router as chat_router

app = FastAPI(
    title="CodexContinue API",
    description="An AI-powered developer assistant backend.",
    version="0.2.0",
)

# Include the /chat endpoint
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CodexContinue API 🚀"}


