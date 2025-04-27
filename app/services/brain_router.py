# app/services/brain_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from openai import AsyncOpenAI, AsyncAzureOpenAI

class BrainRouter:
    def __init__(self):
        if MODEL_PROVIDER == "openai":
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif MODEL_PROVIDER == "azure":
            self.client = AsyncAzureOpenAI(api_key=OPENAI_API_KEY)
        else:
            raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")

    async def chat_completion(self, messages: list, model: str = "gpt-3.5-turbo"):
        if MODEL_PROVIDER == "openai":
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content

        elif MODEL_PROVIDER == "azure":
            response = await self.client.chat.completions.create(
                deployment_id=model,
                messages=messages,
            )
            return response.choices[0].message.content
