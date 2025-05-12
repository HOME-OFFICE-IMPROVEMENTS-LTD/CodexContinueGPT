import streamlit as st

# Page configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="API Keys | CodexContinueGPT",
    page_icon="��",
    layout="wide",
)

# Now we can import other libraries
import requests
import json
import os
import sys
from datetime import datetime, timedelta

# Page header
st.title("🔑 API Key Management")
st.markdown("Create and manage API keys for accessing CodexContinueGPT programmatically")

# Simple API key demonstration UI
st.header("OpenAI API Key Setup")

# API key input form
with st.form("api_key_form"):
    api_key = st.text_input("Enter your OpenAI API key", type="password", 
                          help="Get your API key from https://platform.openai.com/account/api-keys")
    save_location = st.radio("Save location", 
                          options=[".env file (recommended)", "Environment variable", "Session only"])
    submitted = st.form_submit_button("Save API Key")
    
    if submitted and api_key:
        if save_location == ".env file (recommended)":
            st.success("API key will be saved to .env file")
            st.info("Run the following command to apply changes:\n\n`docker-compose restart backend`")
        elif save_location == "Environment variable":
            st.code(f"export OPENAI_API_KEY={api_key}")
            st.info("Add this to your shell profile or run before starting the app")
        else:
            # Just for the current session
            st.session_state["api_key"] = api_key
            st.success("API key saved for this session")
