# app/brain/llm_gateway.py

from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY

class LLMGateway:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate_response(self, messages):
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            reply = response.choices[0].message.content
            return reply
        except Exception as e:
            # Fallback if LLM fails
            return "⚠️ Sorry, the brain is temporarily unavailable. Please try again later."
