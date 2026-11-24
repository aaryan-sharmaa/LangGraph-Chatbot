
import sqlite3
from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


load_dotenv()

DB_PATH = Path(__file__).parent / "chatbot.db"

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=2048,
    reasoning_effort="low"
)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# SQLite checkpointing
connection = sqlite3.connect(DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(connection)

workflow = graph.compile(checkpointer=checkpointer)


# Stream chatbot responses
def stream_chatbot(prompt, thread_id):
    config = {"configurable": {"thread_id": thread_id}}

    for chunk, metadata in workflow.stream(
        {"messages": [HumanMessage(content=prompt)]},
        config=config,
        stream_mode="messages"
    ):
        if metadata.get("langgraph_node") == "chat_node":
            if isinstance(chunk.content, str) and chunk.content:
                yield chunk.content
