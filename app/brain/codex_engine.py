# app/brain/codex_engine.py

from app.chat_memory import memory
from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class CodexContinueGPT:
    def __init__(self):
        self.model = "gpt-3.5-turbo"  # Can later switch per user plan

    async def generate_reply(self, session_id: str, user_input: str) -> str:
        # 1. Save user input to memory
        memory.add_message(session_id, "user", user_input)

        # 2. Retrieve conversation history
        messages = memory.get_messages(session_id)

        # 3. Query OpenAI
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        assistant_reply = response.choices[0].message.content

        # 4. Save assistant reply to memory
        memory.add_message(session_id, "assistant", assistant_reply)

        return assistant_reply
