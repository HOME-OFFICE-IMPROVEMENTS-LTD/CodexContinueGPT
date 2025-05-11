import streamlit as st
import os

# Simple demo of the fix for the chat input issue

def main():
    st.title("CodexContinueGPT Chat Fix Demo")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input using Streamlit's chat_input (more reliable than text_area for chat)
    if prompt := st.chat_input("Your message"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
            
        # Display bot response
        with st.chat_message("assistant"):
            response = f"Echo: {prompt}"
            st.write(response)
            
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
