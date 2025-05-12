import streamlit as st

# Page config MUST be the first Streamlit command
st.set_page_config(
    page_title="CodexContinueGPT Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import other libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import shared configuration
try:
    # Importing configuration without importing streamlit functions
    # that would conflict with our own st.set_page_config
    from app import BACKEND_HOST, BACKEND_PORT, BACKEND_BASE_URL, ENDPOINTS, SUBSCRIPTION_TIERS, safe_api_call
except ImportError:
    # Fallback if imports fail
    BACKEND_HOST = "localhost"
    BACKEND_PORT = "8000"
    BACKEND_BASE_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
    
    # Minimal implementation of safe_api_call for fallback
    def safe_api_call(url, method="GET", payload=None, show_spinner=True, timeout=10):
        try:
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            else:
                response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except:
            return None
    
    # Basic subscription tiers
    SUBSCRIPTION_TIERS = {
        "free": {"name": "Free"},
        "pro": {"name": "Pro"},
        "business": {"name": "Business"}
    }
    
    # Define minimal endpoints
    ENDPOINTS = {
        "analytics": f"{BACKEND_BASE_URL}/analytics"
    }

# Shared styles
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #4f46e5;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Session initialization
if "user_tier" not in st.session_state:
    st.session_state.user_tier = "free"

# Check access tier
def verify_dashboard_access():
    user_tier = st.session_state.get("user_tier", "free")
    if user_tier == "free":
        st.error("⚠️ Analytics Dashboard access requires a Pro or Business subscription")
        st.info("Please upgrade your subscription to access detailed analytics and insights.")
        
        # Show upgrade options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Upgrade to Pro", use_container_width=True):
                st.session_state.user_tier = "pro"
                st.experimental_rerun()
        with col2:
            if st.button("Upgrade to Business", use_container_width=True):
                st.session_state.user_tier = "business"
                st.experimental_rerun()
                
        # Sample view
        st.markdown("### Sample Dashboard Preview")
        st.image("https://via.placeholder.com/800x400.png?text=Analytics+Dashboard+Preview", use_column_width=True)
        return False
        
    return True

# Generate sample data
def generate_sample_data(days=30):
    # Sample conversation data for demo
    today = datetime.now()
    dates = [(today - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(days)]
    dates.reverse()
    
    # Generate synthetic data for charts based on selected time period
    chat_counts = [np.random.randint(5, 25) for _ in range(days)]
    token_counts = [count * np.random.randint(100, 500) for count in chat_counts]
    model_usage = {
        "gpt-3.5-turbo": np.random.randint(40, 60),
        "gpt-4": np.random.randint(20, 40),
        "codellama": np.random.randint(10, 20),
        "llama3": np.random.randint(5, 15),
        "gpt-4o": np.random.randint(1, 10),
    }
    
    # Adjust model percentages to total 100%
    total = sum(model_usage.values())
    if total > 0:
        model_usage = {k: round((v / total) * 100) for k, v in model_usage.items()}
    
    # Recent conversations - prioritize more recent dates based on selected period
    conversations = []
    for i in range(10):
        days_ago = np.random.randint(0, min(7, days))
        convo_date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M")
        conversations.append({
            "id": f"conv-{i+1}",
            "timestamp": convo_date,
            "model": np.random.choice(list(model_usage.keys())),
            "messages": np.random.randint(3, 15),
            "tokens": np.random.randint(500, 3000)
        })
    
    # Sort conversations by timestamp (most recent first)
    conversations.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "dates": dates,
        "chat_counts": chat_counts,
        "token_counts": token_counts,
        "model_usage": model_usage,
        "conversations": conversations
    }

# Dashboard components
def render_metrics_overview(data):
    st.subheader("📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-title">Total Conversations</div>
            </div>
        """.format(sum(data["chat_counts"])), unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-title">Total Tokens Used</div>
            </div>
        """.format(f"{sum(data['token_counts']):,}"), unsafe_allow_html=True)
        
    with col3:
        avg_messages = round(sum(data["chat_counts"]) / len(data["chat_counts"]), 1)
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-title">Avg Daily Conversations</div>
            </div>
        """.format(avg_messages), unsafe_allow_html=True)
        
    with col4:
        # Only business users can see cost estimates
        if st.session_state.user_tier == "business":
            token_cost = round(sum(data["token_counts"]) * 0.000002, 2)
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">${}</div>
                    <div class="metric-title">Estimated Cost</div>
                </div>
            """.format(token_cost), unsafe_allow_html=True)
        else:
            most_used_model = max(data["model_usage"].items(), key=lambda x: x[1])[0]
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-title">Most Used Model</div>
                </div>
            """.format(most_used_model), unsafe_allow_html=True)

def render_usage_charts(data):
    st.subheader("📊 Usage Analytics")
    
    tab1, tab2 = st.tabs(["Conversation Trends", "Model Usage"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        # Conversations per day
        with col1:
            fig = px.line(
                x=data["dates"], 
                y=data["chat_counts"],
                labels={"x": "Date", "y": "Conversations"},
                title="Daily Conversations"
            )
            fig.update_traces(line_color="#4f46e5")
            st.plotly_chart(fig, use_container_width=True)
        
        # Token usage per day
        with col2:
            fig = px.area(
                x=data["dates"], 
                y=data["token_counts"],
                labels={"x": "Date", "y": "Tokens"},
                title="Daily Token Usage"
            )
            fig.update_traces(line_color="#10b981", fill='tozeroy', fillcolor="rgba(16, 185, 129, 0.2)")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Model usage pie chart
        fig = px.pie(
            values=list(data["model_usage"].values()),
            names=list(data["model_usage"].keys()),
            title="Model Usage Distribution"
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        st.plotly_chart(fig, use_container_width=True)

def render_recent_conversations(data):
    st.subheader("💬 Recent Conversations")
    
    # Convert to dataframe for display
    df = pd.DataFrame(data["conversations"])
    
    # Display table
    st.dataframe(
        df[["timestamp", "model", "messages", "tokens"]].rename(columns={
            "timestamp": "Date & Time",
            "model": "Model",
            "messages": "# Messages",
            "tokens": "Tokens Used"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Allow export to CSV (Business tier only)
    if st.session_state.user_tier == "business":
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export Data to CSV",
            data=csv,
            file_name="conversations_export.csv",
            mime="text/csv",
        )

# Main function
st.title("📊 CodexContinueGPT Analytics Dashboard")

# Verify user has access
if not verify_dashboard_access():
    st.stop()

# Time period selector
time_period = st.selectbox(
    "Time Period",
    options=["Last 7 days", "Last 30 days", "Last 90 days"],
    index=1
)

# Map time period to days for data generation
days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
selected_days = days_map.get(time_period, 30)

# Fetch analytics data using proper endpoint
try:
    with st.spinner("Fetching analytics data..."):
        api_data = safe_api_call(f"{ENDPOINTS['analytics']}?days={selected_days}", timeout=5)
    
    if api_data:
        st.success("✅ Successfully connected to analytics API")
        
        # Convert API data to our expected format
        data = {
            "dates": list(api_data.get("daily_conversations", {}).keys()),
            "chat_counts": list(api_data.get("daily_conversations", {}).values()),
            "token_counts": [count * 300 for count in list(api_data.get("daily_conversations", {}).values())],
            "model_usage": api_data.get("model_usage", {}),
            "conversations": [{
                "id": convo.get("session_id", f"conv-{i}"),
                "timestamp": convo.get("timestamp", ""),
                "model": convo.get("model", ""),
                "messages": 5,  # Default value
                "tokens": 1500  # Default value
            } for i, convo in enumerate(api_data.get("recent_conversations", []))]
        }
    else:
        # Use sample data if API fails
        with st.expander("⚠️ Using Sample Data", expanded=True):
            st.info("""
            **Analytics API Note**: Using sample data because the analytics API returned no data.
            """)
        data = generate_sample_data(days=selected_days)
except Exception as e:
    # Fallback to sample data and show the error
    st.warning(f"Error connecting to analytics API: {str(e)}")
    with st.expander("⚠️ Using Sample Data", expanded=True):
        st.info("""
        **Analytics API Note**: Using sample data because there was an error connecting to the analytics API.
        """)
    
    # Use sample data as fallback
    data = generate_sample_data(days=selected_days)

# Display dashboard components
render_metrics_overview(data)
render_usage_charts(data)
render_recent_conversations(data)

# Help section
with st.expander("ℹ️ Dashboard Help"):
    st.markdown("""
        This dashboard provides analytics for your CodexContinueGPT usage.
        
        - **Key Metrics**: Overview of your conversation and token usage
        - **Usage Analytics**: Charts showing usage patterns over time
        - **Recent Conversations**: List of your most recent conversations
        
        Pro users can see basic analytics. Business users have access to additional metrics including cost estimates and data export.
    """)
