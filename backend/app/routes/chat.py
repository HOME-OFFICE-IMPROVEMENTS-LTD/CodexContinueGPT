from fastapi import APIRouter
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are CodexContinue, a brilliant developer assistant."},
                {"role": "user", "content": request.message},
            ],
            temperature=0.3,
            max_tokens=500,
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    return ChatResponse(reply=bot_reply)















