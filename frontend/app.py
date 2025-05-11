# frontend/app.py
import streamlit as st
# Configure page first - this MUST be the first streamlit command
st.set_page_config(
    page_title="CodexContinueGPT",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

import requests
import uuid
import json
import os
from datetime import datetime
import time
import re
import random

# Configuration
# Try to connect to local development server if running outside Docker
BACKEND_HOST = os.environ.get("BACKEND_HOST", "localhost") 
BACKEND_PORT = os.environ.get("BACKEND_PORT", "8000")  
BACKEND_BASE_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# API endpoints
ENDPOINTS = {
    "chat": f"{BACKEND_BASE_URL}/chat",
    "plugins": f"{BACKEND_BASE_URL}/plugins",
    "plugin_exec": f"{BACKEND_BASE_URL}/plugins/execute",
    "sessions": f"{BACKEND_BASE_URL}/sessions",
    "memory_audit": f"{BACKEND_BASE_URL}/memory/audit",
    "health": f"{BACKEND_BASE_URL}/health",
    "models": f"{BACKEND_BASE_URL}/models",  # For multi-LLM support
    "status": f"{BACKEND_BASE_URL}/status",  # Backend status
    "auth": {
        "login": f"{BACKEND_BASE_URL}/auth/login",
        "register": f"{BACKEND_BASE_URL}/auth/register",
        "verify": f"{BACKEND_BASE_URL}/auth/verify",
        "profile": f"{BACKEND_BASE_URL}/auth/profile"
    }
}

# User subscription tiers
SUBSCRIPTION_TIERS = {
    "free": {
        "name": "Free",
        "models": ["gpt-3.5-turbo"],
        "features": ["Chat", "Basic plugins", "Documentation search"],
        "limits": {"messages_per_day": 20, "plugins": 3}
    },
    "pro": {
        "name": "Pro",
        "models": ["gpt-3.5-turbo", "gpt-4", "llama3", "codellama"],
        "features": ["Chat", "All plugins", "Code generation", "Local models (Ollama)"],
        "limits": {"messages_per_day": 100, "plugins": -1}  # -1 means unlimited
    },
    "business": {
        "name": "Business",
        "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4o", "llama3", "codellama", "custom-ollama"],
        "features": ["Chat", "All plugins", "Code generation", "Local models", "Team dashboard", "API access"],
        "limits": {"messages_per_day": -1, "plugins": -1}  # -1 means unlimited
    }
}

# Available LLM models - Will be populated from backend or defaults
AVAILABLE_MODELS = []

# Session Management
def init_session():
    """Initialize session state variables"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.session_start = datetime.now().isoformat()
        st.session_state.chat_history = []
        st.session_state.selected_model = "gpt-3.5-turbo"  # Default model
        st.session_state.user_tier = "free"  # Default tier
        st.session_state.theme_mode = "light"  # Default theme
        st.session_state.streaming = True  # Default streaming mode
        st.session_state.message_count = 0  # Track messages for limits
        st.session_state.show_model_selector = False  # For mobile UI
        st.session_state.plugin_mode = False  # Plugin mode toggle
        st.session_state.available_plugins = []  # Will be populated from backend
        
        # Token usage tracking
        st.session_state.total_tokens = 0
        st.session_state.token_usage_by_model = {}
        st.session_state.tokens_today = 0
        st.session_state.show_token_count = True
        
        # Authentication state
        if "auth" not in st.session_state:
            st.session_state.auth = {
                "logged_in": False,
                "user_id": None,
                "username": None,
                "email": None,
                "tier": "free",
                "token": None,
                "login_time": None,
                "error": None
            }
    
    # Load available models from backend or use defaults
    if "available_models" not in st.session_state:
        try:
            models_data = safe_api_call(ENDPOINTS["models"])
            if models_data and "models" in models_data:
                st.session_state.available_models = models_data["models"]
            else:
                # Fallback default models
                st.session_state.available_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
                st.session_state.backend_connected = False
        except Exception as e:
            # Default models if API fails
            st.session_state.available_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
            st.session_state.backend_connected = False
            st.session_state.backend_error = str(e)

# UI Configuration
def configure_ui():
    """Setup Streamlit UI configuration"""
    # Custom CSS for modern UI - page config is already set at the top of the file
    st.markdown("""
        <style>
            /* Main app styling */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            
            /* Chat message styling */
            .user-message {
                background-color: #4f46e5;
                color: white;
                border-radius: 15px 15px 0 15px;
                padding: 10px 15px;
                margin: 5px 0;
                text-align: right;
                margin-left: auto;
                max-width: 80%;
            }
            
            .assistant-message {
                background-color: #f3f4f6;
                color: #111827;
                border-radius: 15px 15px 15px 0;
                padding: 10px 15px;
                margin: 5px 0;
                text-align: left;
                margin-right: auto;
                max-width: 80%;
                border: 1px solid #e5e7eb;
            }
            
            /* Author indicators */
            .message-author {
                font-weight: 600;
                font-size: 0.9em;
                margin-bottom: 5px;
            }
            
            /* Models selector */
            .model-selector {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
                cursor: pointer;
            }
            
            .selected-model {
                background-color: #f3f4ff;
                border: 1px solid #4f46e5;
            }
            
            /* Tier badges */
            .tier-badge {
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.7em;
                font-weight: 600;
                margin-left: 5px;
            }
            
            .tier-free {
                background-color: #6b7280;
                color: white;
            }
            
            .tier-pro {
                background-color: #10b981;
                color: white;
            }
            
            .tier-business {
                background-color: #4f46e5;
                color: white;
            }
            
            /* Code blocks */
            pre {
                background-color: #1f2937;
                color: #f9fafb;
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
            }
            
            code {
                font-family: 'Courier New', monospace;
            }
            
            /* Fix Streamlit UI elements */
            .stTextArea textarea {
                border-radius: 8px;
                border-color: #e5e7eb;
                padding: 10px;
                font-size: 1rem;
            }
            
            .stButton button {
                border-radius: 8px;
                background-color: #4f46e5;
                color: white;
                font-weight: 600;
                border: none;
                padding: 0.5rem 1rem;
                width: 100%;
            }
            
            .stButton button:hover {
                background-color: #4338ca;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # App header
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <h1 style="margin: 0; margin-right: 10px;">🧠 CodexContinueGPT</h1>
            <div>
                <span style="background-color: #10b981; color: white; padding: 3px 8px; 
                      border-radius: 12px; font-size: 0.8em; font-weight: 600;">v0.2.0</span>
            </div>
        </div>
        <p style="margin-top: 0; color: #6b7280;">Your AI-powered development assistant with multi-model support</p>
    """, unsafe_allow_html=True)

# API Helpers
def safe_api_call(url, method="GET", payload=None, show_spinner=True, timeout=10):
    """
    Make an API call with error handling and spinner
    
    Args:
        url (str): API endpoint URL
        method (str): HTTP method (GET or POST)
        payload (dict): JSON payload for POST requests
        show_spinner (bool): Whether to show a loading spinner
        timeout (int): Request timeout in seconds
        
    Returns:
        dict or None: JSON response or None if request failed
    """
    spinner_text = f"Connecting to {url.split('/')[-1]} endpoint..."
    
    try:
        with st.spinner(spinner_text) if show_spinner else nullcontext():
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            else:
                response = requests.post(url, json=payload, timeout=timeout)
                
            response.raise_for_status()
            return response.json()
            
    except requests.exceptions.ConnectionError:
        show_connection_error(url)
        return None
        
    except requests.exceptions.Timeout:
        st.error(f"⏱️ Timeout: Backend did not respond within {timeout} seconds")
        st.info("The backend service might be overloaded or starting up")
        return None
        
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if hasattr(e.response, 'status_code') else "unknown"
        st.error(f"❌ HTTP Error {status_code}: {str(e)}")
        
        if hasattr(e.response, 'status_code'):
            if e.response.status_code == 401:
                st.warning("Authentication failed. Please check your API key or login.")
            elif e.response.status_code == 403:
                st.warning("You don't have permission to access this resource.")
            elif e.response.status_code == 404:
                st.info("The requested endpoint was not found. API might have changed.")
            elif e.response.status_code >= 500:
                st.warning("Backend server error. Please try again later.")
        return None
        
    except requests.exceptions.RequestException as e:
        st.error(f"🔄 Request Error: {str(e)}")
        return None
        
    except json.JSONDecodeError:
        st.error("Invalid JSON response from the backend")
        return None

def stream_chat_response(user_input, model=None):
    """
    Stream chat response with simulated typing effect
    
    Args:
        user_input (str): User message
        model (str): LLM model to use
    
    Returns:
        str: The full response text
    """
    payload = {
        "session_id": st.session_state.session_id,
        "message": user_input,
        "model": model or st.session_state.selected_model,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "source": "streamlit_ui",
            "tier": st.session_state.user_tier
        }
    }
    
    # Check if we need to send an API key
    models_response = safe_api_call(ENDPOINTS["models"], show_spinner=False) or {"api_key_configured": False}
    api_key_configured = models_response.get("api_key_configured", False)
    
    # Only send API key if not configured in backend
    if not api_key_configured and st.session_state.get("api_key"):
        payload["api_key"] = st.session_state.api_key
    
    with st.spinner("AI is thinking..."):
        try:
            # Send request to chat endpoint
            response = safe_api_call(ENDPOINTS["chat"], "POST", payload, show_spinner=False)
            
            if not response:
                st.error("Failed to get response from backend")
                return "I'm sorry, I'm having trouble connecting to the backend. Please try again."
                
            # Get the reply text
            reply_text = response.get("reply", "No response from the model")
            
            # Update chat history
            add_message_to_history("user", user_input)
            
            # Create a placeholder for streaming response
            message_placeholder = st.empty()
            full_response = ""
            
            # Simulate streaming by gradually revealing the response
            if st.session_state.streaming:
                # Split the reply into word tokens or keep sentences together
                tokens = re.findall(r'[^.,?!]+[.,?!]* ?| +', reply_text)
                
                for token in tokens:
                    full_response += token
                    # Add a blinking cursor while typing
                    message_placeholder.markdown(f"**Assistant**: {full_response}▌")
                    # Random delay between 0.01 and 0.1 seconds for realistic typing
                    time.sleep(random.uniform(0.01, 0.03))
                
            else:
                full_response = reply_text
                
            # Display the full message once streaming is complete
            message_placeholder.empty()
            add_message_to_history("assistant", full_response)
            
            return full_response
            
        except Exception as e:
            st.error(f"Error during streaming: {str(e)}")
            return f"Error during response generation: {str(e)}"

def show_connection_error(url):
    """Display formatted connection error with troubleshooting tips"""
    st.error("🔌 Connection Error")
    st.error(f"Could not connect to backend at {url}")
    
    # Show troubleshooting expandable section
    with st.expander("⚠️ Troubleshooting Tips"):
        st.markdown("### Connection Issues")
        st.markdown(f"- **Backend Host**: `{BACKEND_HOST}`")
        st.markdown(f"- **Backend Port**: `{BACKEND_PORT}`")
        st.markdown("### Checklist:")
        st.markdown("1. ✅ Check if backend container is running: `docker-compose ps`")
        st.markdown("2. ✅ Verify environment variables in `.env` file")
        st.markdown("3. ✅ In Docker, frontend should use `backend` as host, not `localhost`")
        st.markdown("4. ✅ Run diagnostics: `./scripts/test_docker_config.sh`")
        
        # Using a unique key for each retry button based on the URL
        if st.button("Retry Connection", key=f"retry_connection_{url.replace(':', '_').replace('/', '_')}"):
            with st.spinner("Retrying connection..."):
                try:
                    response = requests.get(ENDPOINTS["health"], timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Connection successful!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Connection failed with status code: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Connection retry failed: {str(e)}")

# Context manager for use with or without spinner
class nullcontext:
    def __enter__(self):
        return None
    def __exit__(self, *args):
        pass

# Calculate token usage estimation
def estimate_token_usage(text, model="gpt-3.5-turbo"):
    """
    Estimate token usage for a given text and model
    This is a simplified estimation, real token count depends on tokenizer used
    
    Args:
        text (str): Text to estimate token count for
        model (str): Model name for tokenization specifics
        
    Returns:
        int: Estimated token count
    """
    # Simplified estimation - actual tokenizers are more complex
    # GPT models use ~4 chars per token on average for English text
    if not text:
        return 0
        
    # Different models have different tokenization, this is an estimation
    if "gpt-4" in model:
        chars_per_token = 3.8  # GPT-4 is slightly more efficient
    elif "llama" in model.lower():
        chars_per_token = 4.2  # Approximation for LLama models
    else:  # Default for gpt-3.5-turbo and others
        chars_per_token = 4.0
        
    # Count tokens (very simplified)
    token_count = len(text) / chars_per_token
    
    # Round up to be conservative
    return int(token_count + 0.5)

def add_message_to_history(role, content):
    """Add a message to the chat history with token tracking"""
    timestamp = datetime.now().isoformat()
    
    if role == "user":
        st.session_state.message_count += 1
    
    # Initialize token tracking if not exists
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0
        st.session_state.token_usage_by_model = {}
        st.session_state.tokens_today = 0
    
    # Calculate token usage
    current_model = st.session_state.selected_model
    tokens = estimate_token_usage(content, current_model)
    
    # Update token tracking
    st.session_state.total_tokens += tokens
    
    # Update model-specific tracking
    if current_model not in st.session_state.token_usage_by_model:
        st.session_state.token_usage_by_model[current_model] = 0
    st.session_state.token_usage_by_model[current_model] += tokens
    
    # Update today's usage
    st.session_state.tokens_today += tokens
    
    # Add message with token info to history
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "timestamp": timestamp,
        "tokens": tokens,
        "model": current_model
    })

# Sidebar Components
def render_sidebar():
    """Render the sidebar with configuration options"""
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="margin-bottom: 5px;">⚙️ Configuration</h2>
                <span class="tier-badge tier-{tier}">{tier_name}</span>
            </div>
        """.format(
            tier=st.session_state.user_tier, 
            tier_name=SUBSCRIPTION_TIERS[st.session_state.user_tier]["name"]
        ), unsafe_allow_html=True)
        
        # LLM Model Selection Section
        st.subheader("🤖 AI Model")
        
        # Get available models based on user tier
        available_tier_models = SUBSCRIPTION_TIERS[st.session_state.user_tier]["models"]
        
        # Filter models from the backend that are available for the current tier
        if "available_models" in st.session_state:
            tier_models = [m for m in st.session_state.available_models if m in available_tier_models]
        else:
            tier_models = available_tier_models
        
        # Display model selection
        selected_model = st.radio(
            "Select Model:",
            tier_models,
            index=tier_models.index(st.session_state.selected_model) if st.session_state.selected_model in tier_models else 0,
            format_func=format_model_name
        )
        
        st.session_state.selected_model = selected_model
        
        # Show model info
        with st.expander("Model Information", expanded=False):
            st.markdown(get_model_info(selected_model))
        
        # Session Management
        st.subheader("🔐 Session")
        
        # Check if OpenAI API key is configured in backend
        models_response = safe_api_call(ENDPOINTS["models"], show_spinner=False) or {"api_key_configured": False}
        api_key_configured = models_response.get("api_key_configured", False)
        
        # Only show API key input if not configured in backend
        if st.session_state.user_tier == "free" and not api_key_configured:
            api_key = st.text_input(
                "OpenAI API Key", 
                type="password",
                value=st.session_state.get("api_key", ""),
                help="Your API key is required for the free tier"
            )
            st.session_state.api_key = api_key
        elif api_key_configured:
            st.success("✅ OpenAI API key configured in backend")
            
        # Session selector
        sessions_response = safe_api_call(ENDPOINTS["sessions"], show_spinner=False) or {"sessions": []}
        active_sessions = sessions_response.get("sessions", [])
        
        # Make sure current session is in the list
        if st.session_state.session_id not in active_sessions:
            active_sessions.append(st.session_state.session_id)
            
        selected_session = st.selectbox(
            "Active Session",
            options=active_sessions,
            index=active_sessions.index(st.session_state.session_id),
            format_func=lambda x: f"Session {x[:8]}..." if len(x) > 8 else x
        )
        
        # Update session ID if changed
        if selected_session != st.session_state.session_id:
            st.session_state.session_id = selected_session
            st.session_state.chat_history = []  # Clear chat history when switching sessions
            st.experimental_rerun()
        
        # New session button
        if st.button("🆕 New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.chat_history = []
            st.session_state.session_start = datetime.now().isoformat()
            st.experimental_rerun()
            
        # UI Options
        st.subheader("🎨 UI Options")
        
        col1, col2 = st.columns(2)
        with col1:
            theme = st.selectbox(
                "Theme",
                options=["light", "dark"],
                index=0 if st.session_state.theme_mode == "light" else 1
            )
            st.session_state.theme_mode = theme
            
        with col2:
            streaming = st.checkbox("Enable Streaming", value=st.session_state.streaming)
            st.session_state.streaming = streaming
        
        # Add token display toggle
        show_tokens = st.checkbox("Show Token Counts", value=st.session_state.get("show_token_count", True), 
                                help="Display token usage for each message")
        st.session_state.show_token_count = show_tokens
            
        # Debug & System Section
        st.markdown("---")
        st.subheader("🛠️ System")
        
        # Status and metrics
        col1, col2 = st.columns(2)
        col1.metric("Session ID", st.session_state.session_id[:8] + "...")
        
        # Check backend health
        backend_status = "Checking..."
        try:
            health_data = safe_api_call(ENDPOINTS["health"], show_spinner=False)
            if health_data:
                backend_status = "Online"
            else:
                backend_status = "Offline"
        except:
            backend_status = "Error"
            
        col2.metric("Backend", backend_status)
        
        # Backend connection details
        with st.expander("Backend Connection", expanded=False):
            st.markdown(f"**Host**: `{BACKEND_HOST}`")
            st.markdown(f"**Port**: `{BACKEND_PORT}`")
            st.markdown(f"**Base URL**: `{BACKEND_BASE_URL}`")
            
            # Health check button
            if st.button("🔄 Check Connection"):
                health_data = safe_api_call(ENDPOINTS["health"])
                if health_data:
                    st.success("✅ Connected to backend")
                    st.info(f"Server time: {health_data.get('server_time', 'N/A')}")
                    st.info(f"Status: {health_data.get('status', 'N/A')}")
                else:
                    st.error("❌ Connection failed")
                    
        # Show message usage for free/pro tiers
        if st.session_state.user_tier in ["free", "pro"]:
            daily_limit = SUBSCRIPTION_TIERS[st.session_state.user_tier]["limits"]["messages_per_day"]
            if daily_limit > 0:
                st.progress(min(st.session_state.message_count / daily_limit, 1.0))
                st.caption(f"Messages: {st.session_state.message_count}/{daily_limit} per day")
        
        # Show token usage tracking
        st.subheader("📈 Token Usage")
        
        # Initialize if not exists (for backwards compatibility)
        if "total_tokens" not in st.session_state:
            st.session_state.total_tokens = 0
            st.session_state.token_usage_by_model = {}
            st.session_state.tokens_today = 0
        
        # Display current token usage
        col1, col2 = st.columns(2)
        col1.metric("Today's Usage", f"{st.session_state.tokens_today:,}")
        col2.metric("Total Tokens", f"{st.session_state.total_tokens:,}")
        
        # Token usage by model
        if st.session_state.token_usage_by_model:
            st.subheader("By Model")
            for model, tokens in st.session_state.token_usage_by_model.items():
                st.caption(f"{format_model_name(model)}: {tokens:,} tokens")
        
        # Change subscription tier (demo only)
        with st.expander("🚀 Change Plan (Demo)", expanded=False):
            st.caption("This is a demo feature to switch between subscription tiers")
            
            selected_tier = st.radio(
                "Select Subscription Tier",
                options=list(SUBSCRIPTION_TIERS.keys()),
                index=list(SUBSCRIPTION_TIERS.keys()).index(st.session_state.user_tier),
                format_func=lambda x: SUBSCRIPTION_TIERS[x]["name"]
            )
            
            if selected_tier != st.session_state.user_tier:
                if st.button(f"Switch to {SUBSCRIPTION_TIERS[selected_tier]['name']}"):
                    st.session_state.user_tier = selected_tier
                    st.experimental_rerun()
                    
        # Debug info (hidden by default)
        with st.expander("🐞 Debug", expanded=False):
            st.json({
                "session_id": st.session_state.session_id,
                "backend": BACKEND_BASE_URL,
                "selected_model": st.session_state.selected_model,
                "user_tier": st.session_state.user_tier,
                "message_count": st.session_state.message_count,
                "session_start": st.session_state.session_start,
                "token_usage": {
                    "total": st.session_state.get("total_tokens", 0),
                    "today": st.session_state.get("tokens_today", 0),
                    "by_model": st.session_state.get("token_usage_by_model", {})
                }
            })
            
            if st.button("Clear Session State"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()
        
        # User authentication status
        st.divider()
        if st.session_state.get("auth", {}).get("logged_in", False):
            st.markdown(f"""
                ### 👤 Logged In
                **User:** {st.session_state.auth.get("username", "Unknown")}  
                **Plan:** {SUBSCRIPTION_TIERS[st.session_state.user_tier]["name"]}  
                
                [View Profile](pages/8_User_Authentication.py)
            """)
        else:
            st.markdown("""
                ### 👤 Not Logged In
                
                [Sign In / Register](pages/8_User_Authentication.py)
            """)

def format_model_name(model_name):
    """Format model name for display"""
    # Replace hyphens with spaces and capitalize words
    name = model_name.replace("-", " ").title()
    
    # Special formatting for known models
    if "gpt" in model_name.lower():
        if "4o" in model_name:
            return "GPT-4o" + model_name.split("4o")[-1].upper()
        elif "4" in model_name:
            return "GPT-4" + model_name.split("4")[-1].upper() 
        elif "3.5" in model_name:
            return "GPT-3.5" + model_name.split("3.5")[-1].title()
    
    return name

def get_model_info(model_name):
    """Get detailed information about a model"""
    model_info = {
        "gpt-4o": {
            "description": "GPT-4o is OpenAI's most advanced multi-modal model, capable of handling text, code, and images with high accuracy.",
            "context_length": "128,000 tokens",
            "strengths": "Complex reasoning, code generation, creative writing",
            "tier": "business"
        },
        "gpt-4": {
            "description": "GPT-4 is a powerful language model optimized for accuracy and reasoning.",
            "context_length": "8,192 tokens",
            "strengths": "Complex reasoning, expert knowledge, low hallucination",
            "tier": "pro"
        },
        "gpt-3.5-turbo": {
            "description": "Fast and cost-effective model with good general capabilities.",
            "context_length": "4,096 tokens",
            "strengths": "Quick responses, general knowledge, basic coding",
            "tier": "free"
        },
        "llama3": {
            "description": "Meta's Llama 3 open model with strong general capabilities.",
            "context_length": "8,192 tokens",
            "strengths": "Open source, local deployment, good reasoning",
            "tier": "pro"
        },
        "codellama": {
            "description": "Specialized language model optimized for code generation and understanding.",
            "context_length": "16,000 tokens",
            "strengths": "Code completion, debugging, technical documentation",
            "tier": "pro"
        },
        "custom-ollama": {
            "description": "Custom local model deployed through Ollama.",
            "context_length": "Varies by model",
            "strengths": "Full privacy, customization, no data sharing",
            "tier": "business"
        }
    }
    
    # Return info for the selected model or a generic message
    if model_name in model_info:
        info = model_info[model_name]
        return f"""
        ### {format_model_name(model_name)}
        
        {info['description']}
        
        **Context length**: {info['context_length']}  
        **Strengths**: {info['strengths']}  
        **Required tier**: {SUBSCRIPTION_TIERS[info['tier']]['name']}
        """
    else:
        return f"### {format_model_name(model_name)}\n\nBasic language model with general capabilities."

# Main Chat Interface
def render_chat_interface():
    """Render the main chat interface with mode selection and message input"""
    # Mode selection tabs
    mode_tabs = st.tabs(["💬 Chat", "🧩 Plugins", "🧠 Memory"])
    
    with mode_tabs[0]:  # Chat tab
        # Display chat history
        render_chat_history()
        
        # Add export options
        if st.session_state.chat_history and len(st.session_state.chat_history) > 0:
            with st.expander("Export Conversation"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📄 Export as Markdown", key="export_md"):
                        export_conversation("markdown")
                
                with col2:
                    if st.button("📝 Export as Text", key="export_txt"):
                        export_conversation("text")
                
                with col3:
                    if st.button("📊 Export as JSON", key="export_json"):
                        export_conversation("json")
        
        # Chat input area
        st.markdown("---")
        # Input column layout
        col1, col2 = st.columns([6, 1])            # Simplified chat input using Streamlit's chat_input
        
        # Get model short name for display
        model_short_name = format_model_name(st.session_state.selected_model).split()[0]
        
        # This properly handles the clearing of input after submission
        if user_input := st.chat_input(f"Message {model_short_name}..."):
            # Check message limit for free/pro tiers
            if st.session_state.user_tier in ["free", "pro"]:
                daily_limit = SUBSCRIPTION_TIERS[st.session_state.user_tier]["limits"]["messages_per_day"]
                if daily_limit > 0 and st.session_state.message_count >= daily_limit:
                    st.error(f"You've reached your daily message limit ({daily_limit}). Upgrade to continue chatting.")
                    st.info("Tip: This is a demo - you can switch plans in the sidebar.")
                else:
                    # Process the message
                    handle_chat_submission(user_input)
            else:
                # Process the message for business tier
                handle_chat_submission(user_input)
            
        with col1:
            # This section is now handled by st.chat_input above
            pass
            
        with col2:
            # Message count display for limited tiers
            if st.session_state.user_tier != "business":
                daily_limit = SUBSCRIPTION_TIERS[st.session_state.user_tier]["limits"]["messages_per_day"]
                if daily_limit > 0:
                    st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 10px;">
                            <span style="font-size: 0.8em; color: #6b7280;">
                                {st.session_state.message_count}/{daily_limit}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Model indicator display (no button needed as chat_input handles submission)
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 10px;">
                    <span style="font-size: 0.8em; color: #4f46e5; font-weight: bold;">
                        Using {format_model_name(st.session_state.selected_model)}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
    with mode_tabs[1]:  # Plugins tab
        render_plugin_interface()
        
    with mode_tabs[2]:  # Memory tab
        render_memory_audit()

def render_chat_history():
    """Display the chat history with styled messages"""
    # Create container for chat history
    chat_container = st.container()
    
    with chat_container:
        # Placeholder when no messages
        if not st.session_state.chat_history:
            st.markdown("""
                <div style="text-align: center; padding: 30px; color: #6b7280;">
                    <img src="https://via.placeholder.com/100x100.png?text=AI" style="border-radius: 50%; margin-bottom: 20px;">
                    <h3>Welcome to CodexContinueGPT!</h3>
                    <p>Start a conversation with your AI assistant.</p>
                </div>
            """, unsafe_allow_html=True)
            return
            
        # Show messages with proper styling
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = msg["content"]
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M")
            
            # Format code blocks in messages
            content = format_message_content(content)
            
            # Get token count if available
            token_count = msg.get("tokens", 0)
            msg_model = msg.get("model", st.session_state.selected_model)
            show_tokens = st.session_state.get("show_token_count", True)
            
            # Format token info
            token_info = f"• {token_count:,} tokens" if token_count > 0 and show_tokens else ""
            
            if role == "user":
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end;">
                        <div class="user-message">
                            <div class="message-author" style="text-align: right; color: #f3f4f6;">You</div>
                            {content}
                            <div style="font-size: 0.7em; color: #9ca3af; margin-top: 5px; text-align: right;">
                                {timestamp} {token_info}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                model_display = format_model_name(msg_model) if show_tokens else "AI Assistant"
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start;">
                        <div class="assistant-message">
                            <div class="message-author" style="color: #4f46e5;">{model_display}</div>
                            {content}
                            <div style="font-size: 0.7em; color: #6b7280; margin-top: 5px;">
                                {timestamp} {token_info}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

def format_message_content(content):
    """Format message content with code highlighting"""
    # Replace code blocks with styled HTML
    code_block_pattern = r"```(.*?)\n(.*?)```"
    
    def replace_code_block(match):
        language = match.group(1) or "text"
        code = match.group(2)
        return f"""<pre style="background-color: #1f2937; color: #f9fafb; padding: 10px; 
                border-radius: 8px; overflow-x: auto; font-family: 'Courier New', monospace;">
                <div style="font-size: 0.8em; color: #9ca3af; margin-bottom: 5px; border-bottom: 1px solid #374151; padding-bottom: 3px;">{language}</div>
                {code}</pre>"""
    
    content = re.sub(code_block_pattern, replace_code_block, content, flags=re.DOTALL)
    
    # Replace inline code with styled HTML
    inline_code_pattern = r"`(.*?)`"
    content = re.sub(inline_code_pattern, r'<code style="background-color: #e5e7eb; padding: 2px 4px; border-radius: 3px; font-family: \'Courier New\', monospace; color: #4f46e5;">\1</code>', content)
    
    # Add line breaks for newlines
    content = content.replace("\n", "<br>")
    
    return content

# Chat Mode Handler
def handle_chat_submission(user_input):
    """Process user input and get AI response"""
    # Store the input for processing
    processed_input = user_input
    
    # Simulate typing indicator
    with st.spinner("AI is thinking..."):
        # Use streaming response if enabled
        if st.session_state.streaming:
            # Stream the response
            stream_chat_response(processed_input)
        else:
            # Traditional response handling
            payload = {
                "session_id": st.session_state.session_id,
                "message": processed_input,
                "model": st.session_state.selected_model,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "source": "streamlit_ui",
                    "tier": st.session_state.user_tier
                }
            }
            
            # Check if backend has OpenAI API key configured
            models_response = safe_api_call(ENDPOINTS["models"], show_spinner=False) or {"api_key_configured": False}
            api_key_configured = models_response.get("api_key_configured", False)
            
            # Only include API key from user input if backend doesn't have one configured
            if not api_key_configured and st.session_state.get("api_key"):
                payload["api_key"] = st.session_state.api_key
            
            # Send API request
            response = safe_api_call(ENDPOINTS["chat"], "POST", payload)
            
            if response:
                # Add to chat history
                add_message_to_history("user", processed_input)
                add_message_to_history("assistant", response.get("reply", "Error: No reply received"))

# Plugin Mode Handler
def render_plugin_interface():
    """Render the plugin selection and execution interface"""
    st.subheader("🧩 Available Plugins")
    
    # Check plugin limits based on tier
    plugin_limit = SUBSCRIPTION_TIERS[st.session_state.user_tier]["limits"]["plugins"]
    
    # Fetch plugins from backend
    plugins_response = safe_api_call(ENDPOINTS["plugins"]) or {"plugins": []}
    available_plugins = plugins_response.get("plugins", [])
    
    # Apply plugin limits for free tier
    if plugin_limit > 0 and len(available_plugins) > plugin_limit:
        limited_plugins = available_plugins[:plugin_limit]
        st.warning(f"⚠️ Free tier limited to {plugin_limit} plugins. Upgrade for full access.")
    else:
        limited_plugins = available_plugins
    
    if not limited_plugins:
        st.info("No plugins available. Check back later!")
        return
    
    # Plugin selection and description
    plugin_cols = st.columns(2)
    
    # Create two columns of plugins
    for i, plugin_data in enumerate(limited_plugins):
        col_idx = i % 2
        
        # Extract plugin details
        plugin_name = plugin_data if isinstance(plugin_data, str) else plugin_data.get("name", "Unknown")
        plugin_desc = plugin_data.get("description", "No description available") if isinstance(plugin_data, dict) else ""
        
        # Create a card for each plugin
        with plugin_cols[col_idx]:
            with st.container():
                st.markdown(f"""
                    <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                        <h4 style="margin-top: 0;">{plugin_name}</h4>
                        <p style="color: #6b7280; font-size: 0.9em;">{plugin_desc}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    # Plugin execution section
    st.subheader("Execute Plugin")
    
    # Select plugin
    selected_plugin = st.selectbox(
        "Select a plugin to execute:",
        options=[""] + limited_plugins,
        format_func=lambda x: x if x else "Select a plugin...",
        index=0
    )
    
    if selected_plugin:
        # Plugin input
        plugin_input = st.text_area(
            f"Input for {selected_plugin}:",
            height=100,
            placeholder=f"Enter data for the {selected_plugin} plugin..."
        )
        
        # Execute button
        if st.button("🚀 Execute Plugin", use_container_width=True) and plugin_input:
            with st.spinner(f"Executing {selected_plugin}..."):
                # Send plugin execution request
                response = safe_api_call(
                    ENDPOINTS["plugin_exec"],
                    "POST",
                    {
                        "plugin": selected_plugin, 
                        "data": plugin_input,
                        "session_id": st.session_state.session_id
                    }
                )
                
                if response:
                    # Show plugin output
                    st.success(f"Plugin {selected_plugin} executed successfully!")
                    
                    # Display output in styled container
                    st.markdown("""
                        <div style="background-color: #f8fafc; border: 1px solid #e5e7eb; 
                             border-radius: 8px; padding: 15px; margin-top: 10px;">
                            <h4 style="margin-top: 0;">Plugin Output</h4>
                    """, unsafe_allow_html=True)
                    
                    # Format output based on type
                    output = response.get("output", "No output returned")
                    
                    # Handle different output types
                    if isinstance(output, (dict, list)):
                        st.json(output)
                    else:
                        st.code(str(output))
                        
                    st.markdown("</div>", unsafe_allow_html=True)

# Memory Audit Handler
def render_memory_audit():
    """Render the memory audit visualization"""
    st.subheader("🧠 Memory Timeline")
    
    # Get session memory
    memory_data = safe_api_call(f"{ENDPOINTS['memory_audit']}/{st.session_state.session_id}")
    
    if not memory_data:
        st.info("No memory data available for this session.")
        return
        
    # Extract memory data
    short_memory = memory_data.get("short", [])
    full_memory = memory_data.get("full", [])
    
    # Memory metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Short-term Messages", len(short_memory))
    col2.metric("Full Memory Messages", len(full_memory))
    col3.metric("Session ID", st.session_state.session_id[:8] + "...")
    
    # Tabs for different memory views
    memory_tabs = st.tabs(["Timeline View", "Raw Data"])
    
    with memory_tabs[0]:
        # Timeline visualization
        st.subheader("Conversation Timeline")
        
        # Create timeline visualization
        for i, msg in enumerate(full_memory):
            # Extract message data
            content = msg.get("content", "")
            role = msg.get("role", "unknown")
            
            # Format timestamp if available
            if "timestamp" in msg:
                try:
                    timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
                except:
                    timestamp = msg["timestamp"]
            else:
                timestamp = f"Step {i+1}"
                
            # Determine message style based on role
            if role == "user":
                icon = "👤"
                color = "#4f46e5"
            elif role == "assistant":
                icon = "🤖"
                color = "#10b981"
            elif role == "system":
                icon = "⚙️"
                color = "#6b7280"
            else:
                icon = "❓"
                color = "#9ca3af"
                
            # Create timeline entry
            st.markdown(f"""
                <div style="display: flex; margin-bottom: 15px;">
                    <div style="background-color: {color}; color: white; width: 30px; height: 30px; 
                         border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                         margin-right: 15px; flex-shrink: 0;">
                        {icon}
                    </div>
                    <div style="border-left: 2px solid {color}; padding-left: 15px; flex-grow: 1;">
                        <div style="display: flex; justify-content: space-between;">
                            <div style="font-weight: 600;">{role.capitalize()}</div>
                            <div style="color: #6b7280; font-size: 0.8em;">{timestamp}</div>
                        </div>
                        <div style="margin-top: 5px;">
                            {content[:100] + '...' if len(content) > 100 else content}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    with memory_tabs[1]:
        # Raw memory data
        st.json(memory_data)

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
    """Main application entry point"""
    # Initialize session state
    init_session()
    
    # Configure the UI
    configure_ui()
    
    # Check backend status at startup
    check_backend_status()
    
    # Display backend connection warning if needed
    if hasattr(st.session_state, "backend_connected") and st.session_state.backend_connected is False:
        st.error("⚠️ Cannot connect to backend service. Some features may not work properly.")
        st.info("Backend URL: " + BACKEND_BASE_URL)
        with st.expander("Troubleshooting Tips"):
            st.markdown("""
            1. Check if the backend service is running: `docker-compose ps`
            2. Check backend logs: `docker-compose logs backend`
            3. Try restarting the backend: `docker-compose restart backend`
            4. Make sure your API keys are properly configured if needed
            """)
        # Continue with limited functionality
    
    # Show landing page for first-time users
    if "first_visit" not in st.session_state:
        st.session_state.first_visit = True
        render_landing_page()
        return
        
    # Two-column layout
    col1, col2 = st.columns([1, 3])
    
    # Sidebar in left column
    with col1:
        render_sidebar()
    
    # Chat interface in right column
    with col2:
        # Show pricing page if requested
        if st.session_state.get("show_pricing", False):
            render_pricing_page()
            if st.button("Back to Chat"):
                st.session_state.show_pricing = False
                st.experimental_rerun()
        else:
            render_chat_interface()
        
    # Apply theme based on selection
    apply_theme(st.session_state.theme_mode)

def render_landing_page():
    """Show landing page for first-time visitors"""
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 1rem;">Welcome to CodexContinueGPT</h1>
            <p style="font-size: 1.2rem; color: #6b7280; margin-bottom: 2rem;">
                Your AI-powered development assistant with multi-model support
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("<h2 style='text-align: center; margin-bottom: 1.5rem;'>Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem;">
                <h3>🤖 Multiple AI Models</h3>
                <p>Choose from various LLM models based on your subscription tier</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem;">
                <h3>🧩 Extensible Plugins</h3>
                <p>Enhance capabilities with specialized tools and plugins</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem;">
                <h3>🧠 Advanced Memory</h3>
                <p>Persistent memory for longer conversations and context</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Quick start section
    st.markdown("<h2 style='text-align: center; margin: 2rem 0 1.5rem;'>Get Started</h2>", unsafe_allow_html=True)
    
    start_col1, start_col2 = st.columns([3, 1])
    
    with start_col1:
        st.markdown("""
            <div style="padding: 1rem; border-radius: 0.5rem; background-color: #f9fafb;">
                <p>CodexContinueGPT offers different subscription tiers to match your needs:</p>
                <ul>
                    <li><strong>Free tier</strong>: Basic chat with GPT-3.5</li>
                    <li><strong>Pro tier</strong>: Access to more models and plugins</li>
                    <li><strong>Business tier</strong>: Unlimited usage and all premium features</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with start_col2:
        if st.button("See Pricing", key="landing_pricing", use_container_width=True):
            st.session_state.show_pricing = True
            st.session_state.first_visit = False
            st.experimental_rerun()
            
        if st.button("Start Chatting", key="landing_start", use_container_width=True):
            st.session_state.first_visit = False
            st.experimental_rerun()

def apply_theme(theme_mode):
    """Apply the selected theme based on user preference"""
    if theme_mode == "dark":
        st.markdown("""
            <style>
                /* Dark theme for main UI */
                .main {
                    background-color: #1f2937;
                    color: #f9fafb;
                }
                
                /* Dark inputs */
                .stTextArea textarea {
                    background-color: #374151;
                    color: #f9fafb;
                    border-color: #4b5563;
                }
                
                /* Dark select boxes */
                .stSelectbox div[data-baseweb="select"] {
                    background-color: #374151;
                    color: #f9fafb;
                }
                
                /* Dark dropdowns */
                div[data-baseweb="popover"] div {
                    background-color: #374151;
                    color: #f9fafb;
                }
                
                /* Dark chat messages */
                .assistant-message {
                    background-color: #374151;
                    color: #f9fafb;
                    border-color: #4b5563;
                }
                
                /* Dark code elements */
                code {
                    background-color: #4b5563;
                    color: #10b981;
                }
                
                /* Dark chat container */
                .chat-container {
                    background-color: #111827;
                    border-color: #374151;
                }
                
                /* Dark sidebar */
                .sidebar .sidebar-content {
                    background-color: #111827;
                    color: #f9fafb;
                }
                
                /* Dark expanders */
                .streamlit-expanderHeader {
                    background-color: #374151 !important;
                    color: #f9fafb !important;
                }
                
                /* Dark buttons */
                .stButton>button {
                    border-color: #4b5563 !important;
                }
                
                /* Dark tabs */
                .stTabs [data-baseweb="tab-list"] {
                    background-color: #111827;
                }
                
                .stTabs [data-baseweb="tab"] {
                    color: #f3f4f6;
                }
                
                .stTabs [aria-selected="true"] {
                    background-color: #374151 !important;
                }
                
                /* Dark plugin cards */
                .plugin-card {
                    background-color: #374151;
                    border-color: #4b5563;
                    color: #f9fafb;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme (default)
        st.markdown("""
            <style>
                /* Light theme reset/overrides if needed */
                .main {
                    background-color: white;
                    color: #111827;
                }
                
                /* Fix any dark mode elements that might persist */
                .stTabs [data-baseweb="tab-list"] {
                    background-color: transparent;
                }
            </style>
        """, unsafe_allow_html=True)

def check_backend_status():
    """Check if backend is available and retrieve models"""
    try:
        # Try to get backend status
        status = safe_api_call(ENDPOINTS["status"], show_spinner=False)
        if status:
            st.session_state.backend_online = True
            if "available_models" in status:
                st.session_state.available_models = status["available_models"]
            if "default_model" in status:
                st.session_state.selected_model = status["default_model"]
        else:
            st.session_state.backend_online = False
    except:
        st.session_state.backend_online = False

# Marketing components for landing page
def render_pricing_page():
    """Render pricing information for subscription tiers"""
    st.subheader("📊 Subscription Plans")
    
    # Three-column layout for pricing
    cols = st.columns(3)
    
    # Generate pricing cards
    for i, (tier_id, tier_data) in enumerate(SUBSCRIPTION_TIERS.items()):
        with cols[i]:
            st.markdown(f"""
                <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; 
                      {f'border-color: #4f46e5;' if tier_id == st.session_state.user_tier else ''}">
                    <h3>{tier_data['name']}</h3>
                    <div style="font-size: 2rem; font-weight: 600; margin: 15px 0;">
                        {"Free" if tier_id == "free" else "$9.99" if tier_id == "pro" else "$29.99"}
                        <span style="font-size: 0.9rem; font-weight: normal; color: #6b7280;">
                            {"/month" if tier_id != "free" else ""}
                        </span>
                    </div>
                    <div style="margin-bottom: 20px; height: 2px; background-color: #e5e7eb;"></div>
                    <div style="text-align: left; margin-bottom: 20px;">
            """, unsafe_allow_html=True)
            
            # Features list
            for feature in tier_data["features"]:
                st.markdown(f"""
                    <div style="margin-bottom: 10px; display: flex;">
                        <div style="color: #10b981; margin-right: 10px;">✓</div>
                        <div>{feature}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Model access
            st.markdown("""
                <div style="margin-bottom: 10px; display: flex;">
                    <div style="color: #10b981; margin-right: 10px;">✓</div>
                    <div>Access to models:</div>
                </div>
            """, unsafe_allow_html=True)
            
            for model in tier_data["models"]:
                st.markdown(f"<div style='margin-left: 24px;'>- {format_model_name(model)}</div>", unsafe_allow_html=True)
                
            # Usage limits
            msg_limit = tier_data["limits"]["messages_per_day"]
            st.markdown(f"""
                <div style="margin: 15px 0; text-align: center; color: #6b7280;">
                    {f"{msg_limit} messages/day" if msg_limit > 0 else "Unlimited messages"}
                </div>
            """, unsafe_allow_html=True)
            
            # CTA button
            if tier_id == st.session_state.user_tier:
                st.markdown(f"""
                    <div style="text-align: center; margin-top: 20px;">
                        <button style="background-color: #10b981; color: white; border: none; 
                                border-radius: 4px; padding: 8px 16px; font-weight: 600; width: 100%;">
                            Current Plan
                        </button>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="text-align: center; margin-top: 20px;">
                        <button style="background-color: #4f46e5; color: white; border: none;
                                border-radius: 4px; padding: 8px 16px; font-weight: 600; width: 100%;">
                            {"Upgrade Now" if tier_id != "free" else "Get Started"}
                        </button>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div></div>", unsafe_allow_html=True)

# Export conversation to file
def export_conversation(export_format="markdown"):
    """Export the current conversation in the specified format"""
    if not st.session_state.chat_history:
        st.error("No conversation to export")
        return
    
    conversation_title = f"CodexContinueGPT Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    if export_format == "markdown":
        content = f"# {conversation_title}\n\n"
        for msg in st.session_state.chat_history:
            role = msg["role"].capitalize()
            content += f"## {role}\n\n{msg['content']}\n\n"
        
        filename = "conversation.md"
        mimetype = "text/markdown"
    
    elif export_format == "text":
        content = f"{conversation_title}\n\n"
        for msg in st.session_state.chat_history:
            role = msg["role"].capitalize()
            content += f"{role}:\n{msg['content']}\n\n"
        
        filename = "conversation.txt"
        mimetype = "text/plain"
    
    elif export_format == "json":
        # Create a structured JSON with metadata
        export_data = {
            "title": conversation_title,
            "timestamp": datetime.now().isoformat(),
            "model": st.session_state.selected_model,
            "session_id": st.session_state.session_id,
            "messages": st.session_state.chat_history
        }
        content = json.dumps(export_data, indent=2)
        
        filename = "conversation.json"
        mimetype = "application/json"
    
    else:
        st.error(f"Unsupported export format: {export_format}")
        return
    
    # Create download button
    st.download_button(
        label=f"Download as {export_format.capitalize()}",
        data=content,
        file_name=filename,
        mime=mimetype,
        key=f"download_{export_format}"
    )
    
    # Log the export action
    st.toast(f"Conversation exported as {export_format.capitalize()}", icon="✅")

# Execute main app when script runs
if __name__ == "__main__":
    main()