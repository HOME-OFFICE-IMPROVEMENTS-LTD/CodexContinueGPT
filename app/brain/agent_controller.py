# app/brain/agent_controller.py

from app.brain.llm_interface import get_llm_response
from app.brain.tools.search import search_web

class CodexContinueAgent:
    def __init__(self):
        self.name = "CodexContinueGPT v1"

    async def run(self, query: str, context: dict = {}):
        # Optionally use tools here, like search_web(query)
        context_str = "\\n".join(f"{k}: {v}" for k, v in context.items())
        prompt = f"Question: {query}\\nContext: {context_str}\\nAnswer:"
        return await get_llm_response(prompt)
