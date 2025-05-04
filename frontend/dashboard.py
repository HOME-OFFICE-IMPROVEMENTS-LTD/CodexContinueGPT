# frontend/dashboard.py

import streamlit as st
import requests
import uuid

BACKEND_CHAT_URL = "http://localhost:8000/chat"
BACKEND_PLUGIN_LIST_URL = "http://localhost:8000/tools"
BACKEND_PLUGIN_EXEC_URL = "http://localhost:8000/plugins/execute"
BACKEND_MEMORY_AUDIT_URL = "http://localhost:8000/memory/audit"

# Set session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.set_page_config(page_title="CodexContinue Dashboard", layout="wide")
st.title("🧠 CodexContinue Developer Dashboard")

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🧩 Tools", "📜 Memory"])

with tab1:
    st.header("💬 Chat with Assistant")
    user_input = st.text_input("Message:", key="chat_input")

    if st.button("Send", key="send_button") and user_input:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(BACKEND_CHAT_URL, json={
                    "session_id": st.session_state.session_id,
                    "message": user_input
                })
                reply = response.json().get("reply", "⚠️ No reply")
                st.success(reply)
            except Exception as e:
                st.error(f"Request failed: {e}")

with tab2:
    st.header("🧩 Available Tools")
    try:
        tool_list = requests.get(BACKEND_PLUGIN_LIST_URL).json().get("tools", [])
        for tool in tool_list:
            with st.expander(f"{tool['name']}"):
                st.write(tool['description'])
                tool_input = st.text_input(f"Input for {tool['name']}:", key=f"{tool['name']}_input")
                if st.button(f"Run {tool['name']}", key=f"{tool['name']}_run"):
                    with st.spinner(f"Running {tool['name']}..."):
                        response = requests.post(BACKEND_PLUGIN_EXEC_URL, json={
                            "plugin": tool["name"],
                            "data": tool_input
                        })
                        st.json(response.json())
    except Exception as e:
        st.error(f"Failed to load tools: {e}")

with tab3:
    st.header("📜 Memory Audit")
    try:
        mem_response = requests.get(f"{BACKEND_MEMORY_AUDIT_URL}/{st.session_state.session_id}")
        if mem_response.status_code == 200:
            mem_data = mem_response.json()
            st.subheader("Short-Term Memory")
            st.json(mem_data.get("short", []))
            st.subheader("Full Memory")
            st.json(mem_data.get("full", []))
        else:
            st.warning("No memory found for session.")
    except Exception as e:
        st.error(f"Memory fetch failed: {e}")
