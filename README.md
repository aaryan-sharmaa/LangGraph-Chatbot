# LangGraph Chatbot

A conversational AI chatbot built using Python, LangGraph, and Streamlit, with persistent conversation history and real-time response streaming.

## Overview

This project explores building a stateful AI chatbot using LangGraph. It started as a basic graph-based chatbot and evolved into a multi-file application with a Streamlit interface and SQLite-backed conversation persistence.

The goal is to understand and implement core LangGraph concepts through practical development, gradually extending the chatbot with more advanced capabilities.

## Features

- **Graph-Based Chatbot:** Uses LangGraph to manage conversational workflows.
- **Conversation Memory:** Maintains context across messages within a conversation.
- **Persistent Chat History:** Uses SQLite to preserve conversation state across application restarts.
- **Multiple Conversations:** Supports separate chat sessions using thread IDs.
- **Real-Time Streaming:** Displays generated responses incrementally.
- **Streamlit Interface:** Provides an interactive web interface for chatting.

## Tech Stack

- Python
- LangGraph
- LangChain
- Streamlit
- SQLite

## Project Structure

```text
LangGraph-Chatbot/
├── app.py
├── chatbot.py
├── chatbot.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/aaryan-sharmaa/LangGraph-Chatbot.git
cd LangGraph-Chatbot
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file and add the API credentials required by the configured LLM provider.

**5. Run the chatbot**

```bash
streamlit run app.py
```

## Future Improvements

- LangSmith tracing and observability
- External tools and function calling
- Model Context Protocol (MCP) integration
- Retrieval-Augmented Generation (RAG)

## About

A hands-on LangGraph learning project focused on building and understanding stateful, persistent, and extensible AI applications.