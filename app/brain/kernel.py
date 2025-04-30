# app/brain/kernel.py

from app.config import OPENAI_API_KEY
from openai import AsyncOpenAI
from typing import List, Dict

# 🧠 Init clients (extend later with Azure/Ollama)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class Kernel:
    def __init__(self):
        self.model = "gpt-3.5-turbo"  # 🔁 Can be changed dynamically

    async def run(self, messages: List[Dict], model: str = None) -> str:
        try:
            response = await openai_client.chat.completions.create(
                model=model or self.model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Kernel error: {str(e)}"

kernel = Kernel()
