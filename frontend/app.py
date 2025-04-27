# backend/frontend/app.py

import streamlit as st
import requests
import uuid

# Backend API URL
BACKEND_URL = "http://localhost:8000/chat"

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("🧠 CodexContinue Assistant")

# Text input for user
user_input = st.text_input("Your message:", key="user_input")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        # Send request to backend
        try:
            response = requests.post(
                BACKEND_URL,
                json={
                    "session_id": st.session_state.session_id,
                    "message": user_input
                }
            )
            if response.status_code == 200:
                data = response.json()
                assistant_reply = data.get("reply", "")
                st.success(f"🤖 Assistant: {assistant_reply}")
            else:
                st.error(f"Backend error: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
