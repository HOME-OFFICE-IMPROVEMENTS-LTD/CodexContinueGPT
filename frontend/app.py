# frontend/app.py

import streamlit as st
import requests
import uuid

BACKEND_URL = "http://localhost:8000/chat"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("🧠 CodexContinue Assistant")

user_input = st.text_input("Your message:")

if st.button("Send") and user_input:
    with st.spinner("Thinking..."):
        try:
            res = requests.post(BACKEND_URL, json={
                "session_id": st.session_state.session_id,
                "message": user_input
            })
            if res.status_code == 200:
                st.success(res.json()["reply"])
            else:
                st.error(f"❌ {res.status_code}: {res.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Failed to connect: {str(e)}")


# Insert API Key at the start
action = 'start'

# Request API key input
if action == 'start':
    st.sidebar.title('API Configuration')
    openai_api_key = st.sidebar.text_input('Enter OpenAI API Key:', type='password')

    # Store the API key in session state
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
    