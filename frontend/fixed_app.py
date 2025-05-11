# Streamlit chat interface with proper input handling
import streamlit as st
import requests
import uuid
import os
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="CodexContinueGPT",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
BACKEND_HOST = os.environ.get("BACKEND_HOST", "localhost") 
BACKEND_PORT = os.environ.get("BACKEND_PORT", "8000")  
BACKEND_BASE_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# API endpoints
ENDPOINTS = {
    "chat": f"{BACKEND_BASE_URL}/chat",
    "health": f"{BACKEND_BASE_URL}/health",
    "models": f"{BACKEND_BASE_URL}/models",
}

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-3.5-turbo"

# App header
st.title("🧠 CodexContinueGPT")
st.caption("Your AI-powered development assistant with multi-model support")

# Layout with sidebar
col1, col2 = st.columns([1, 3])

# Sidebar
with col1:
    st.sidebar.title("⚙️ Configuration")
    
    # Model selection
    st.sidebar.subheader("🤖 AI Model")
    models = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
    selected_model = st.sidebar.selectbox(
        "Select Model:",
        models,
        index=models.index(st.session_state.selected_model) if st.session_state.selected_model in models else 0
    )
    st.session_state.selected_model = selected_model
    
    # Backend status
    st.sidebar.subheader("🛠️ System")
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ Backend Connected")
        else:
            st.sidebar.error("❌ Backend Error")
    except Exception as e:
        st.sidebar.error(f"❌ Connection Error: {str(e)}")
    
    # Check if API key is configured
    try:
        models_response = requests.get(f"{BACKEND_BASE_URL}/models", timeout=5).json()
        api_key_configured = models_response.get("api_key_configured", False)
        if api_key_configured:
            st.sidebar.success("✅ OpenAI API key configured")
        else:
            api_key = st.sidebar.text_input("OpenAI API Key", type="password")
            if api_key:
                st.session_state.api_key = api_key
    except Exception:
        st.sidebar.warning("⚠️ Could not check API key status")

# Main chat container
with col2:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input - using Streamlit's chat_input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to state and display it
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Prepare the backend request
        payload = {
            "session_id": st.session_state.session_id,
            "message": prompt,
            "model": st.session_state.selected_model
        }
        
        # Include API key if needed
        if not api_key_configured and "api_key" in st.session_state:
            payload["api_key"] = st.session_state.api_key
        
        # Send request to backend
        with st.spinner("AI is thinking..."):
            try:
                response = requests.post(f"{BACKEND_BASE_URL}/chat", json=payload)
                if response.status_code == 200:
                    reply = response.json().get("reply", "Error: No reply received")
                else:
                    reply = f"Error {response.status_code}: Failed to get response"
            except Exception as e:
                reply = f"Connection Error: {str(e)}"
        
        # Display AI response
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
