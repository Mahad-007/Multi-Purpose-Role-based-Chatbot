import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

API_URL = "https://grok-2-by-xai.p.rapidapi.com/"
HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "grok-2-by-xai.p.rapidapi.com",
    "Content-Type": "application/json"
}

PERSONALITIES = {
    "Math Teacher": "You are a helpful Math Teacher. Only answer math-related questions. Politely decline other topics.",
    "Doctor": "You are a professional doctor. Only provide health and medical information. Politely refuse other topics.",
    "Travel Guide": "You are a travel guide. Only answer travel-related questions. Refuse unrelated queries.",
    "Chef": "You are a chef. Only answer questions about food, recipes, and cooking.",
    "Tech Support": "You are a tech support assistant. Only help with software, devices, or tech problems."
}

st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("💬 Groq Chatbot with Personalities")

# Sidebar
selected_model = st.sidebar.selectbox("Select Groq Model", ["Grok-2"])
selected_persona = st.sidebar.selectbox("Choose a Personality", list(PERSONALITIES.keys()))

# Chat history (session state)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": PERSONALITIES[selected_persona]}
    ]
# Display messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input field
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare request
    payload = {
        "model": selected_model,
        "temperature": 1,
        "max_tokens": 2048,
        "messages": st.session_state.messages
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
        data = response.json()
        ai_message = data["choices"][0]["message"]["content"]

    except Exception as e:
        ai_message = f"❌ Error: {e}"

    # Show assistant reply
    with st.chat_message("assistant"):
        st.markdown(ai_message)

    st.session_state.messages.append({"role": "assistant", "content": ai_message})
