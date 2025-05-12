from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import asyncio
import os

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
    # Check if OpenAI API key is configured
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    invalid_keys = [
        "",
        "your-openai-api-key",
        "your-openai-api-key-here",
        "your_openai_api_key_here",
        "sk-your-api-key-here",
        "your_api_key_here"
    ]
    api_key_configured = bool(openai_api_key and openai_api_key not in invalid_keys)
    
    # Dictionary mapping model names to their details, including availability based on API key configuration
    model_details = {
        "gpt-4o": {
            "available": api_key_configured, 
            "name": "GPT-4o", 
            "description": "OpenAI's most advanced multi-modal model for text, code, and reasoning",
            "type": "openai"
        },
        "gpt-4-turbo": {
            "available": api_key_configured, 
            "name": "GPT-4 Turbo", 
            "description": "OpenAI's advanced model for text and code", 
            "type": "openai"
        }, 
        "gpt-3.5-turbo": {
            "available": api_key_configured, 
            "name": "GPT-3.5 Turbo", 
            "description": "OpenAI's efficient model for most tasks", 
            "type": "openai"
        }
    }
    
    return {
        "models": model_details,
        "default": None,
        "api_key_configured": api_key_configured
    }
