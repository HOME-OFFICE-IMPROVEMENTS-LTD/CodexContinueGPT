# app/brain/codex_router.py

from app.chat_memory import memory
from app.config import MODEL_PROVIDER
from openai import AsyncOpenAI
from typing import List, Dict

class CodexContinueRouter:
    def __init__(self, openai_api_key: str):
        self.provider = MODEL_PROVIDER
        self.client = AsyncOpenAI(api_key=openai_api_key)

    async def route(
        self, session_id: str, user_message: str
    ) -> Dict[str, str]:
        # 1. Save user input
        memory.add_message(session_id, "user", user_message)

        # 2. Fetch memory for this session
        messages: List[Dict[str, str]] = memory.get_messages(session_id)

        # 3. Route to the correct model
        if self.provider == "openai":
            completion = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            reply = completion.choices[0].message.content

        elif self.provider == "ollama":
            # TODO: Implement Ollama local inference
            reply = "⚠️ Ollama not yet implemented"

        else:
            reply = f"❌ Unknown provider: {self.provider}"

        # 4. Save assistant reply
        memory.add_message(session_id, "assistant", reply)
        return {"reply": reply}
