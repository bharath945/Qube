import streamlit as st
import requests
import time

API_URL = "https://dev-api-gateway.aesthatiq.com/mcp-service/ask"

# Minimal function to send messages to the API
def send_message(messages):
    try:
        payload = {"messages": messages}
        response = requests.post(API_URL, json=payload, verify=False, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "messages" in data:
                for msg in reversed(data["messages"]):
                    if msg.get("role") == "assistant":
                        return msg.get("content", "")
                return "No assistant response found"
            elif isinstance(data, dict) and "response" in data:
                return data["response"]
            elif isinstance(data, dict) and "content" in data:
                return data["content"]
            elif isinstance(data, str):
                return data
            else:
                return str(data)
        else:
            return f"Error: API returned status code {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.set_page_config(page_title="AesthatiQ", page_icon="🤖")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! How can I assist you with aesthetic or body-related services today?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask me anything about aesthetic services...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(st.session_state.messages)
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 