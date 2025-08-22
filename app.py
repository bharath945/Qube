import streamlit as st
import requests
import time

API_URL = "https://dev-api-gateway.aesthatiq.com/mcp-service/ask"

# Constant IDs
USER_ID = "f2abb647-5043-49a5-9cd2-ae16a234fd11"
SESSION_ID = "f2abb647-5043-49a5-9cd2-ae16a234fd11"

# Function to send a single user input to the API
def send_message(user_input):
    try:
        payload = {
            "session_id": SESSION_ID,
            "user_id": USER_ID,
            "input": user_input
        }
        response = requests.post(API_URL, json=payload, verify=False, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "reply" in data:
                return data["reply"]
            else:
                return str(data)
        else:
            return f"Error: API returned status code {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.set_page_config(page_title="AesthatiQ", page_icon="🤖")

    # Store chat history locally in session_state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I assist you with aesthetic or body-related services today?"}
        ]

    # Display all previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    prompt = st.chat_input("Ask me anything about aesthetic services...")
    if prompt:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant reply
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(prompt)
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

        # Store assistant reply
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()



