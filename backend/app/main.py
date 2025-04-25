from fastapi import FastAPI
from app.routes import chat

app = FastAPI(title="CodexContinue Backend", version="0.1.0")

# Register routes
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CodexContinue API 🚀"}
