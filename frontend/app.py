# frontend/app.py

import streamlit as st
import requests
import uuid

BACKEND_CHAT_URL = "http://localhost:8000/chat"
BACKEND_PLUGIN_LIST_URL = "http://localhost:8000/plugins"
BACKEND_PLUGIN_EXEC_URL = "http://localhost:8000/plugins/execute"
BACKEND_SESSIONS_URL = "http://localhost:8000/sessions"
BACKEND_MEMORY_AUDIT_URL = "http://localhost:8000/memory/audit"

# Session ID state
if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

# Get available sessions
def fetch_sessions():
    try:
        res = requests.get(BACKEND_SESSIONS_URL)
        if res.status_code == 200:
            return res.json().get("sessions", [])
    except:
        return []
    return []

# Title
st.title("🧠 CodexContinue Assistant")

# Sidebar
st.sidebar.title("Session Control")
available_sessions = fetch_sessions()
selected = st.sidebar.selectbox("Select a session", options=available_sessions or ["default"])
st.session_state.session_id = selected

# Sidebar: API Key input
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if openai_api_key:
    st.session_state.openai_api_key = openai_api_key

# Main interface
mode = st.radio("Choose interaction mode:", ["🤖 Chat", "🧩 Run Plugin"])

if mode == "🤖 Chat":
    user_input = st.text_input("Your message:")
    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            try:
                res = requests.post(BACKEND_CHAT_URL, json={
                    "session_id": st.session_state.session_id,
                    "message": user_input
                })
                if res.status_code == 200:
                    st.success(res.json()["reply"])
                else:
                    st.error(f"❌ {res.status_code}: {res.json().get('detail')}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

elif mode == "🧩 Run Plugin":
    try:
        plugins_res = requests.get(BACKEND_PLUGIN_LIST_URL)
        plugins = plugins_res.json().get("plugins", [])
        selected_plugin = st.selectbox("Select a plugin", options=plugins)
        plugin_input = st.text_input("Your message or input:")
        if st.button("Run Plugin") and selected_plugin:
            with st.spinner("Running..."):
                res = requests.post(BACKEND_PLUGIN_EXEC_URL, json={
                    "plugin": selected_plugin,
                    "data": plugin_input
                })
                if res.status_code == 200:
                    st.json(res.json())
                else:
                    st.error("Plugin execution failed.")
    except:
        st.error("Failed to load plugins.")

# Audit Panel
st.subheader("📜 Memory Timeline")
try:
    audit_url = f"{BACKEND_MEMORY_AUDIT_URL}/{st.session_state.session_id}"
    audit_res = requests.get(audit_url)
    if audit_res.status_code == 200:
        data = audit_res.json()
        for msg in data.get("full", []):
            st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")
except:
    st.warning("Unable to load memory audit.")
