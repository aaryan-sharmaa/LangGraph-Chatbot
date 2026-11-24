
import sqlite3
import streamlit as st
from uuid import uuid4

from langchain_core.messages import HumanMessage, AIMessage
from chatbot import workflow, stream_chatbot, DB_PATH


st.set_page_config(page_title="Basic Chatbot", page_icon="💬")
st.title("💬 Basic Chatbot")


# Database helpers
def get_connection():
    return sqlite3.connect(DB_PATH, timeout=30)


def setup_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                thread_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def get_conversations():
    with get_connection() as conn:
        return conn.execute("""
            SELECT thread_id, title
            FROM conversations
            ORDER BY created_at DESC, rowid DESC
        """).fetchall()


def create_chat():
    thread_id = str(uuid4())

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO conversations (thread_id, title) VALUES (?, ?)",
            (thread_id, "New Chat")
        )

    return thread_id


def update_title(thread_id, title):
    with get_connection() as conn:
        conn.execute(
            "UPDATE conversations SET title = ? WHERE thread_id = ?",
            (title, thread_id)
        )


# Initialize database and session
setup_database()

if "current_thread" not in st.session_state:
    conversations = get_conversations()

    if conversations:
        st.session_state.current_thread = conversations[0][0]
    else:
        st.session_state.current_thread = create_chat()


# Sidebar
with st.sidebar:
    st.title("💬 Conversations")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_thread = create_chat()
        st.rerun()

    st.divider()
    st.subheader("Recent Chats")

    for thread_id, title in get_conversations():
        if st.button(title, key=thread_id, use_container_width=True):
            st.session_state.current_thread = thread_id
            st.rerun()


# Load selected conversation
thread_id = st.session_state.current_thread
config = {"configurable": {"thread_id": thread_id}}

state = workflow.get_state(config)
messages = state.values.get("messages", [])


# Display chat history
for message in messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)


# Handle user input
if prompt := st.chat_input("Type your message..."):

    conversations = dict(get_conversations())

    if conversations.get(thread_id) == "New Chat":
        update_title(thread_id, prompt[:30])

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(
            stream_chatbot(prompt, thread_id)
        )

    st.rerun()
