# app/services/model_router.py

from app.config import MODEL_PROVIDER, OPENAI_API_KEY
from app.chat_memory import memory
from openai import AsyncOpenAI
from typing import List, Dict

class ModelRouter:
    def __init__(self):
        self.provider = MODEL_PROVIDER.lower()

        if self.provider == "openai":
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        elif self.provider == "azure":
            # Placeholder for Azure setup
            self.client = None
        elif self.provider == "ollama":
            # Placeholder for local LLM setup
            self.client = None
        else:
            raise ValueError(f"Unknown MODEL_PROVIDER: {self.provider}")

    async def chat(self, session_id: str, messages: List[Dict]) -> str:
        """Route the chat to the selected LLM."""
        if self.provider == "openai":
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            return response.choices[0].message.content
        
        elif self.provider == "azure":
            # TODO: Add Azure OpenAI call
            return "Azure OpenAI not implemented yet."
        
        elif self.provider == "ollama":
            # TODO: Add Ollama call
            return "Ollama model not implemented yet."
        
        else:
            return "Invalid model provider configuration."

# Global instance
model_router = ModelRouter()
