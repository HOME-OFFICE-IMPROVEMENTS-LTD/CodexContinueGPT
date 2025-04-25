from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import asyncio

router = APIRouter()

# Mock models available (for now, real later)
AVAILABLE_MODELS = ["gpt-4o", "gpt-4", "llama3", "codellama", "custom-ollama"]

@router.post("/chat")
async def chat_endpoint(payload: dict):
    message = payload.get("message", "")
    reply = f"You said: '{message}'. (Simulated AI Response)"
    return {"reply": reply}

@router.post("/chatstream")
async def chatstream_endpoint(payload: dict):
    async def event_generator():
        message = payload.get("message", "")
        for word in message.split():
            yield f"data: {word}\n\n"
            await asyncio.sleep(0.3)
        yield "data: [END]\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/health")
async def health_check():
    return {"status": "ok", "detail": "Backend is alive and healthy"}

@router.get("/status")
async def status_check():
    return {
        "status": "online",
        "available_models": AVAILABLE_MODELS,
        "default_model": "gpt-4o"
    }

@router.get("/models")
async def models_list():
    return {"models": AVAILABLE_MODELS}
