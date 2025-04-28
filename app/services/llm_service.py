# app/services/llm_service.py

import os
from openai import AsyncOpenAI, AsyncAzureOpenAI
from typing import List, Dict

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")

class LLMService:
    def __init__(self):
        if MODEL_PROVIDER == "openai":
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif MODEL_PROVIDER == "azure":
            self.client = AsyncAzureOpenAI(
                api_key=OPENAI_API_KEY,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                azure_deployment="gpt-35-turbo",  # Customize your Azure deployment name
            )
        else:
            raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")

    async def chat(self, messages: List[Dict]) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
