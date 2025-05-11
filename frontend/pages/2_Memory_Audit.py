# frontend/pages/2_Memory_Audit.py

import streamlit as st
import requests
import os

# Configuration - use the same backend configuration as main app
BACKEND_HOST = os.environ.get("BACKEND_HOST", "localhost") 
BACKEND_PORT = os.environ.get("BACKEND_PORT", "8000")  
BACKEND_BASE_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# Header and navigation
col1, col2 = st.columns([6, 1])
with col1:
    st.title("🧠 Memory Audit Tool")
with col2:
    st.markdown("""
    <a href="/" target="_self">
        <button style="background-color: #6b7280; color: white; border: none; 
        border-radius: 4px; padding: 8px 16px; cursor: pointer; width: 100%;">
        Back to Chat
        </button>
    </a>
    """, unsafe_allow_html=True)

# Try to fetch available sessions first
try:
    sessions_res = requests.get(f"{BACKEND_BASE_URL}/sessions")
    if sessions_res.status_code == 200:
        sessions_data = sessions_res.json()
        available_sessions = sessions_data.get("sessions", ["default"])
        
        session_id = st.selectbox(
            "Select Session ID to audit:", 
            options=available_sessions,
            index=0
        )
        
        if not available_sessions or len(available_sessions) == 0:
            st.warning("No active sessions found. Enter a session ID manually.")
            manual_session_id = st.text_input("Or enter Session ID manually:", value="default")
            if manual_session_id:
                session_id = manual_session_id
    else:
        session_id = st.text_input("Session ID to audit:", value="default")
        st.warning("Could not fetch available sessions. Enter a session ID manually.")
except Exception:
    session_id = st.text_input("Session ID to audit:", value="default")
    st.warning("Could not fetch available sessions. Enter a session ID manually.")

if st.button("Audit Memory"):
    try:
        res = requests.get(f"{BACKEND_BASE_URL}/memory/audit/{session_id}")
        if res.status_code == 200:
            data = res.json()
            
            # Display memory metrics and copy button
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.metric("Short-term Messages", len(data.get("short", [])))
            with col2:
                st.metric("Full Memory Messages", len(data.get("full", [])))
            with col3:
                st.markdown(f"""
                <button onclick="navigator.clipboard.writeText('{session_id}');
                alert('Session ID copied to clipboard!');" 
                style="background-color: #4f46e5; color: white; border: none; 
                border-radius: 4px; padding: 8px 16px; cursor: pointer; width: 100%;">
                Copy ID
                </button>
                """, unsafe_allow_html=True)
            
            # Display memory data in tabs
            memory_tabs = st.tabs(["Short-Term Memory", "Long-Term Memory", "Raw Data"])
            
            with memory_tabs[0]:
                st.subheader("🧾 Short-Term Memory")
                if not data.get("short"):
                    st.info("No short-term memory data available.")
                else:
                    for i, msg in enumerate(data["short"]):
                        with st.expander(f"{msg['role'].title()} - Message {i+1}"):
                            st.markdown(f"**Role:** {msg['role']}")
                            st.markdown(f"**Content:** {msg['content']}")
                            if 'timestamp' in msg:
                                st.caption(f"Timestamp: {msg['timestamp']}")
            
            with memory_tabs[1]:
                st.subheader("📚 Long-Term Memory")
                if not data.get("full"):
                    st.info("No long-term memory data available.")
                else:
                    for i, msg in enumerate(data["full"]):
                        with st.expander(f"{msg['role'].title()} - Message {i+1}"):
                            st.markdown(f"**Role:** {msg['role']}")
                            st.markdown(f"**Content:** {msg['content']}")
                            if 'timestamp' in msg:
                                st.caption(f"Timestamp: {msg['timestamp']}")
            
            with memory_tabs[2]:
                st.subheader("Raw Memory Data")
                st.json(data)
        else:
            st.error(f"Error {res.status_code}: {res.text}")
    except requests.exceptions.ConnectionError:
        st.error(f"Failed to connect to backend at {BACKEND_BASE_URL}")
        st.info("Make sure the backend service is running and accessible.")
        st.code(f"""
# Docker status check commands:
docker-compose ps backend
docker-compose logs --tail=20 backend
        """)
    except Exception as e:
        st.error(f"Failed to connect: {e}")
