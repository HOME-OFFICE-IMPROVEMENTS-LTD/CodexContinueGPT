# frontend/app.py

import streamlit as st
import requests
import uuid

# Backend API URL
BACKEND_URL = "http://localhost:8000/chat"

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("🧠 CodexContinue Assistant")

# Text Input
user_message = st.text_input("Your message:")

if st.button("Send"):
    if user_message.strip():
        payload = {
            "session_id": st.session_state.session_id,
            "message": user_message,
        }
        try:
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                assistant_reply = response.json().get("reply", "No reply received.")
                st.success(f"�� Assistant: {assistant_reply}")
            else:
                st.error(f"Backend error: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
    else:
        st.warning("Please enter a message before sending.")
