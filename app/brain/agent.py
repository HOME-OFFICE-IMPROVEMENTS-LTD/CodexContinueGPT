# app/brain/agent.py

from app.chat_memory import memory
from app.config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

async def process_user_message(session_id: str, message: str) -> str:
    # Save the user's message to memory
    memory.add_message(session_id, "user", message)

    # Retrieve conversation history
    history = memory.get_messages(session_id)

    # Call OpenAI for response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )

    reply = response.choices[0].message.content.strip()

    # Save the assistant reply to memory
    memory.add_message(session_id, "assistant", reply)

    return reply
