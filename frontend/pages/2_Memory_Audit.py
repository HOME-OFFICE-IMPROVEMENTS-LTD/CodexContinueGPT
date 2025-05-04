# frontend/pages/2_Memory_Audit.py

import streamlit as st
import requests

st.title("🧠 Memory Audit Tool")

session_id = st.text_input("Session ID to audit:", value="default")

if st.button("Audit Memory"):
    try:
        res = requests.get(f"http://localhost:8000/memory/audit/{session_id}")
        if res.status_code == 200:
            data = res.json()
            st.subheader("🧾 Short-Term Memory")
            for msg in data["short"]:
                st.markdown(f"- **{msg['role']}**: {msg['content']}")
            st.subheader("�� Long-Term Memory")
            for msg in data["full"]:
                st.markdown(f"- **{msg['role']}**: {msg['content']}")
        else:
            st.error(f"Error {res.status_code}: {res.text}")
    except Exception as e:
        st.error(f"Failed to connect: {e}")
