# app/brain/kernel.py

from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from app.brain.core.base import CodexTool, CodexResponse
from openai import AsyncOpenAI
from typing import List
import logging

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class CodexKernel:
    def __init__(self, tools: List[CodexTool] = []):
        self.tools = tools

    async def run(self, message: str, session_id: str) -> CodexResponse:
        logger.info(f"🧠 [CodexKernel] Running for session: {session_id}")

        memory.add_message(session_id, "user", message)

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=memory.get_messages(session_id)
        )
        reply = response.choices[0].message.content

        memory.add_message(session_id, "assistant", reply)
        return CodexResponse(reply=reply)
