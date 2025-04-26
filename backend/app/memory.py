# backend/app/memory.py

class ChatMemory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []
# This class manages the chat memory, allowing to add messages, retrieve them, and clear the memory.
# It can be used to maintain the context of the conversation in a session.
# The `add_message` method adds a new message to the memory.
# The `get_messages` method retrieves all messages stored in the memory.
# The `clear` method clears the memory, resetting it to an empty state.
# This is useful for managing the conversation history in a chat application.
# The class can be instantiated and used in the chat endpoint to keep track of the conversation context.
# The `ChatMemory` class can be used in the FastAPI application to manage the conversation history.
# It can be instantiated in the chat endpoint and used to add user and assistant messages to the memory.
# This allows the application to maintain context across multiple interactions.
# The `get_messages` method can be used to retrieve the conversation history when needed.