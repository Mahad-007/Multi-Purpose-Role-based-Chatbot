import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file


GROQ_API_KEY = st.secrets["RAPIDAPI_KEY"]


# Initialize Groq OpenAI-compatible client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"  # ✅ Corrected base_url
)

# Use exact model names from Groq
MODEL_OPTIONS = [
    "meta-llama/llama-3-8b-instruct",
    "meta-llama/llama-3-70b-instruct",
    "meta-llama/llama-4-scout-17b-16e-instruct"
]

# Personality prompts
PERSONALITIES = {
    "Math Teacher": "You are a helpful Math Teacher. Only answer math-related questions. Politely decline other topics.",
    "Doctor": "You are a professional doctor. Only provide health and medical information. Politely refuse other topics.",
    "Travel Guide": "You are a travel guide. Only answer travel-related questions. Refuse unrelated queries.",
    "Chef": "You are a chef. Only answer questions about food, recipes, and cooking.",
    "Tech Support": "You are a tech support assistant. Only help with software, devices, or tech problems."
}

# Streamlit UI
st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("💬 Groq Chatbot with Personalities")

# Sidebar: model and personality selection
selected_model = st.sidebar.selectbox("Select Groq Model", MODEL_OPTIONS)
selected_persona = st.sidebar.selectbox("Choose a Personality", list(PERSONALITIES.keys()))

# Initialize conversation
if "messages" not in st.session_state or st.session_state.get("persona") != selected_persona:
    st.session_state.messages = [
        {"role": "system", "content": PERSONALITIES[selected_persona]}
    ]
    st.session_state.persona = selected_persona

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Call Groq model
        response = client.chat.completions.create(
            model=selected_model,
            messages=st.session_state.messages,
            temperature=1
        )

        ai_message = response.choices[0].message.content

        # Show assistant message
        with st.chat_message("assistant"):
            st.markdown(ai_message)

        st.session_state.messages.append({"role": "assistant", "content": ai_message})

    except Exception as e:
        st.error(f"❌ Error: {e}")
