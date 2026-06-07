import streamlit as st
import json
import os

from chatbot import get_response
from prompt import SYSTEM_PROMPT

HISTORY_FILE = "chat_history.json"

st.set_page_config(
    page_title="Smart Agriculture Bot",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #EAF7E4;
}

/* Sidebar Background */
[data-testid="stSidebar"] {
    background-color: #D8F0D0;
}

/* Main Title */
h1 {
    color: #2E7D32;
}

/* Buttons */
.stButton button {
    background-color: #81C784;
    color: black;
    border-radius: 8px;
}

/* Chat Input Box */
[data-testid="stChatInput"] {
    border-radius: 10px;
}

/* Sidebar Text */
[data-testid="stSidebar"] {
    color: #1B5E20;
}

</style>
""", unsafe_allow_html=True)

# Load chat history
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        saved_history = json.load(f)
else:
    saved_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "recent_chats" not in st.session_state:
    st.session_state.recent_chats = saved_history

# Sidebar
with st.sidebar:

    st.image("logo.png", width=200)

   
    st.title("🧠 Smart Thinkers")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []

    st.markdown("---")

    st.subheader("Info")
    st.write("Agriculture Bot for crop explanation")

    st.subheader("Recent Chats")

    if not st.session_state.recent_chats:
        st.caption("No recent chats")

    for chat in reversed(st.session_state.recent_chats[-10:]):
        st.write(f"• {chat}")

# Main page
st.title("🌾 Agri Bot ")



# Show chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

query = st.chat_input("Type your question here...")

if query:

    # Save recent chat
    st.session_state.recent_chats.append(query)

    with open(HISTORY_FILE, "w") as f:
        json.dump(st.session_state.recent_chats, f)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.write(query)

    final_prompt = f"""
{SYSTEM_PROMPT}

User Question:
{query}
"""

    answer = get_response(final_prompt)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.write(answer)