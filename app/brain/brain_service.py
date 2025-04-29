# app/brain/brain_service.py

from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY
from app.chat_memory import memory

# Initialize OpenAI Client
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class CodexContinueGPT:
    def __init__(self):
        self.client = openai_client

    async def chat(self, session_id: str, user_input: str) -> str:
        # Save user message to memory
        memory.add_message(session_id, "user", user_input)

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=memory.get_messages(session_id),
            )
            assistant_reply = response.choices[0].message.content
        except Exception as e:
            assistant_reply = "⚠️ Sorry, there was a problem processing your request."

        # Save assistant reply
        memory.add_message(session_id, "assistant", assistant_reply)

        return assistant_reply

# Global Brain Instance
brain = CodexContinueGPT()
