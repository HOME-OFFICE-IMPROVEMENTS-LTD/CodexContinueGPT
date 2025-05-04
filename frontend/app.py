# frontend/app.py
import streamlit as st
import requests
import uuid
from datetime import datetime
import json

# Configuration
BACKEND_BASE_URL = "http://localhost:8000"  # Move to config file/environment variables
ENDPOINTS = {
    "chat": f"{BACKEND_BASE_URL}/chat",
    "plugins": f"{BACKEND_BASE_URL}/plugins",
    "plugin_exec": f"{BACKEND_BASE_URL}/plugins/execute",
    "sessions": f"{BACKEND_BASE_URL}/sessions",
    "memory_audit": f"{BACKEND_BASE_URL}/memory/audit"
}

# Session Management
def init_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.session_start = datetime.now().isoformat()
        st.session_state.chat_history = []

# UI Configuration
def configure_ui():
    st.set_page_config(
        page_title="CodexContinueGPT Pro",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("🧠 CodexContinueGPT Pro Assistant")
    st.markdown("""
        <style>
            .stTextArea [data-baseweb=textarea] { background-color: #f8f9fa; }
            .stButton>button { width: 100%; }
            .stMarkdown { padding: 0.5rem; }
        </style>
    """, unsafe_allow_html=True)

# API Helpers
def safe_api_call(url, method="GET", payload=None):
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Sidebar Components
def render_sidebar():
    with st.sidebar:
        st.title("🔐 Session & Configuration")
        
        # API Key Management
        api_key = st.text_input("OpenAI API Key", type="password", 
                              help="Your OpenAI API key is never stored on our servers")
        
        # Session Management
        sessions = safe_api_call(ENDPOINTS["sessions"]) or {"sessions": []}
        selected = st.selectbox(
            "🗂️ Active Session",
            options=sessions["sessions"] + [st.session_state.session_id],
            index=0
        )
        st.session_state.session_id = selected
        
        # System Status
        st.markdown("---")
        st.markdown("**System Status**")
        col1, col2 = st.columns(2)
        col1.metric("Session ID", st.session_state.session_id[:8])
        col2.metric("Started", st.session_state.session_start.split("T")[0])
        
        # Debug Info (hidden by default)
        if st.checkbox("Show debug info"):
            st.json({
                "session": st.session_state.session_id,
                "backend": BACKEND_BASE_URL,
                "last_updated": datetime.now().isoformat()
            })

# Main Chat Interface
def render_chat_interface():
    st.markdown("---")
    mode = st.radio(
        "Interaction Mode:",
        ["🤖 Chat", "🧩 Plugin", "🧠 Audit Timeline"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    user_input = st.text_area(
        "Your message or input", 
        height=100,
        placeholder="Type your message or query here...",
        key="user_input"
    )
    
    if mode == "🤖 Chat":
        if st.button("💬 Send Message", use_container_width=True):
            handle_chat_submission(user_input)
    
    elif mode == "🧩 Plugin":
        render_plugin_interface(user_input)
    
    elif mode == "🧠 Audit Timeline":
        if st.button("📜 Load Memory Timeline", use_container_width=True):
            render_memory_timeline()

# Chat Mode Handler
def handle_chat_submission(user_input):
    with st.spinner("Generating response..."):
        payload = {
            "session_id": st.session_state.session_id,
            "message": user_input,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "source": "web_ui"
            }
        }
        
        response = safe_api_call(ENDPOINTS["chat"], "POST", payload)
        if response:
            st.session_state.chat_history.append({
                "user": user_input,
                "assistant": response.get("reply"),
                "timestamp": datetime.now().isoformat()
            })
            display_chat_history()

# Plugin Mode Handler
def render_plugin_interface(user_input):
    plugins = safe_api_call(ENDPOINTS["plugins"]) or {"plugins": []}
    plugin = st.selectbox(
        "Select Plugin",
        options=plugins.get("plugins", []),
        help="Choose a plugin to execute"
    )
    
    if st.button("🔌 Execute Plugin", use_container_width=True):
        with st.spinner(f"Executing {plugin}..."):
            response = safe_api_call(
                ENDPOINTS["plugin_exec"],
                "POST",
                {"plugin": plugin, "data": user_input}
            )
            if response:
                st.json(response)

# Memory Timeline Handler
def render_memory_timeline():
    with st.spinner("Auditing memory..."):
        response = safe_api_call(
            f"{ENDPOINTS['memory_audit']}/{st.session_state.session_id}"
        )
        if response:
            render_memory_visualization(response)

def display_chat_history():
    for msg in st.session_state.chat_history[-5:]:  # Show last 5 messages
        with st.chat_message("user"):
            st.markdown(msg["user"])
        with st.chat_message("assistant"):
            st.markdown(msg["assistant"])

def render_memory_visualization(data):
    tab1, tab2 = st.tabs(["🗂️ Short-Term Memory", "📚 Long-Term Memory"])
    
    with tab1:
        for m in data.get("short", []):
            with st.expander(f"{m['role'].capitalize()} - {m.get('timestamp', '')}"):
                st.markdown(m["content"])
    
    with tab2:
        for m in data.get("full", []):
            with st.expander(f"{m['role'].capitalize()} - {m.get('timestamp', '')}"):
                st.markdown(m["content"])

# Main App Flow
def main():
    init_session()
    configure_ui()
    render_sidebar()
    render_chat_interface()

if __name__ == "__main__":
    main()