import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Streamlit app
st.title("Chat with OpenAI 🤖")
st.write("Ask anything and get a response from OpenAI's GPT model!")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# User input
user_input = st.text_input("Your message:", key="user_input")

if st.button("Send"):
    if user_input:
        # Add user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )

        # Add assistant response to conversation history
        assistant_message = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# Display conversation history
st.write("### Conversation")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Assistant:** {message['content']}")




















