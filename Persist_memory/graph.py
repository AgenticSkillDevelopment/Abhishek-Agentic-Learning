from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from tools.rag_tool import create_rag_tool
from memory_store import JSONMemory

from dataclasses import dataclass
from typing import List
from langchain_core.messages import BaseMessage

@dataclass
class State:
    messages: List[BaseMessage]


def build_graph():
    memory = JSONMemory()
    rag_tool = create_rag_tool()

    def ai_node(state: State) -> State:
        last_msg = state.messages[-1].content
        print("[DEBUG] ai_node received:", last_msg)
        memory.save("user-session", last_msg)
        history = "\n".join(memory.load("user-session"))
        rag_response = rag_tool(last_msg)
        reply = f"Based on memory and knowledge:\n{rag_response}"
        return State(messages=state.messages + [AIMessage(content=reply)])

    builder = StateGraph(State)
    builder.add_node("ai_node", ai_node)
    builder.set_entry_point("ai_node")
    builder.set_finish_point("ai_node")
    return builder.compile()