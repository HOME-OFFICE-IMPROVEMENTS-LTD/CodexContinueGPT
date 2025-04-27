# frontend/app.py

import streamlit as st
import requests
import uuid

# Backend API URL
BACKEND_URL = "http://localhost:8000/chat"

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.set_page_config(page_title="CodexContinueGPT", page_icon="🧠")
st.title("🧠 CodexContinueGPT Assistant")

# Message History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if user_input := st.chat_input("How can I assist you today?"):
    # Append user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.spinner("Thinking..."):
            response = requests.post(
                BACKEND_URL,
                json={
                    "session_id": st.session_state.session_id,
                    "message": user_input
                },
                timeout=30,
            )
        if response.status_code == 200:
            reply = response.json().get("reply", "No reply received.")
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
        else:
            st.error(f"Backend Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {str(e)}")

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.experimental_rerun()
