from fastapi import FastAPI
from app.routes import assistant

app = FastAPI(title="CodexContinue Backend", version="0.2.0")

# Register routes
app.include_router(assistant.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CodexContinue API 🚀"}
