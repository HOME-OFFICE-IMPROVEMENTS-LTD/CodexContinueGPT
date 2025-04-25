from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    # Simple logic for now (replace later with real AI call)
    user_message = request.message
    if "capital of france" in user_message.lower():
        bot_reply = "The capital of France is Paris. 🇫🇷"
    else:
        bot_reply = "I'm still learning! 🤖"

    return ChatResponse(reply=bot_reply)
