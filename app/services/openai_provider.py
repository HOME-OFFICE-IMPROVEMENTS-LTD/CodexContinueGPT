# app/services/openai_provider.py

from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY
from app.services.base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def chat(self, messages: list, model: str = "gpt-3.5-turbo"):
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
