# frontend/pages/memory_dashboard.py

import streamlit as st
import requests

st.title("🧠 Memory Audit Dashboard")

session_id = st.text_input("Enter Session ID", value="default")

if st.button("Fetch Memory Audit"):
    try:
        res = requests.get(f"http://localhost:8000/memory/audit/{session_id}")
        if res.status_code == 200:
            data = res.json()
            st.success("Memory retrieved successfully!")
            st.json(data)
        else:
            st.error(f"Error: {res.status_code} - {res.json().get('detail')}")
    except Exception as e:
        st.error(f"Request failed: {e}")
