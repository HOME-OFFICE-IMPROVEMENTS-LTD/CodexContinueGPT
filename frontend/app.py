import streamlit as st
import requests

st.set_page_config(page_title="CodexContinue", layout="wide")

st.title("🤖 CodexContinue - Developer Assistant")

query = st.text_area("Ask the assistant anything about your code:")

if st.button("Ask"):
    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://localhost:8000/chat", json={"message": query})
            res.raise_for_status()
            st.success(f"🧠 Response: {res.json()['reply']}")
        except Exception as e:
            st.error(f"🚨 Request failed: {e}")
