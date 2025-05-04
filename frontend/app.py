# frontend/app.py

import streamlit as st
import requests
import uuid

BACKEND_CHAT_URL = "http://localhost:8000/chat"
BACKEND_PLUGIN_LIST_URL = "http://localhost:8000/plugins"
BACKEND_PLUGIN_EXEC_URL = "http://localhost:8000/plugins/execute"

# Session ID for conversation continuity
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Title
st.title("🧠 CodexContinue Assistant")

# Sidebar for API key entry
st.sidebar.title("🔐 API Configuration")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")

# Execution mode selector
mode = st.radio("Choose interaction mode:", ["🤖 Chat", "🧩 Run Plugin"])

# Load plugins dynamically
plugin_options = []
if mode == "🧩 Run Plugin":
    try:
        res = requests.get(BACKEND_PLUGIN_LIST_URL)
        plugin_options = res.json().get("plugins", [])
    except Exception as e:
        st.error(f"⚠️ Failed to load plugins: {e}")

# Plugin selector (if applicable)
selected_plugin = None
if plugin_options:
    selected_plugin = st.selectbox("Select a plugin to run:", plugin_options)

# User input
user_input = st.text_input("Your message or input:")

# Submission button
if st.button("Send") and user_input:
    with st.spinner("Processing..."):
        try:
            if mode == "🤖 Chat":
                res = requests.post(BACKEND_CHAT_URL, json={
                    "session_id": st.session_state.session_id,
                    "message": user_input
                })
                if res.status_code == 200:
                    st.success(res.json()["reply"])
                else:
                    st.error(f"❌ {res.status_code}: {res.json().get('detail', 'Unknown error')}")
            else:
                if not selected_plugin:
                    st.warning("Please select a plugin first.")
                else:
                    res = requests.post(BACKEND_PLUGIN_EXEC_URL, json={
                        "plugin": selected_plugin,
                        "data": user_input
                    })
                    if res.status_code == 200:
                        st.json(res.json())
                    else:
                        st.error(f"❌ {res.status_code}: {res.json().get('detail', 'Unknown plugin error')}")

        except Exception as e:
            st.error(f"❌ Failed to connect: {str(e)}")


"""
🎛️ Milestone Recorded — 2025-05-04
- Streamlit frontend now supports dual mode:
  1. 🤖 Normal chat via `/chat`
  2. 🧩 Plugin execution via `/plugins/execute`
- Plugin list loaded dynamically from `/plugins`
- Unified session state maintained.
"""
