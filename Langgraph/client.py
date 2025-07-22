import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, AIMessage
 
# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key is None:
    raise EnvironmentError("GROQ_API_KEY not found in environment variables or .env file.")
 
# Initialize MCP client
client = MultiServerMCPClient({
    "currency_checker": {
        "url": "http://localhost:8010/mcp",
        "transport": "streamable_http"
    }
})
 
# Initialize Groq LLM
llm = ChatGroq(model="qwen/qwen3-32b", api_key=groq_api_key, temperature=0)
 
# Define the state for LangGraph
class State(MessagesState):
    pass
 
# Define the chat node to process user queries
async def chat_node(state: State) -> State:
    tools = await client.get_tools()  # Fetch MCP tools
    llm_with_tools = llm.bind_tools(tools)  # Bind tools to LLM
    response = await llm_with_tools.ainvoke(state["messages"])
    return {"messages": [response]}
 
# Build the LangGraph workflow
async def create_graph():
    builder = StateGraph(State)
    builder.add_node("chat_node", chat_node)
    tools = await client.get_tools()
    builder.add_node("tool_node", ToolNode(tools=tools))
    builder.add_edge(START, "chat_node")
    builder.add_conditional_edges("chat_node", tools_condition, {"tools": "tool_node", "__end__": END})
    builder.add_edge("tool_node", "chat_node")
    return builder.compile()
 
# Main function to run the assistant
async def main():
    graph = await create_graph()
    print("💬 Interactive Assistant Ready (type 'exit' to quit)")
    try:
        while True:
            user_input = input("\n🧑 You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Ending chat.")
                break
            response = await graph.ainvoke({"messages": [HumanMessage(content=user_input)]})
            print("🤖 Assistant: " + response["messages"][-1].content)
    finally:
        if client.sessions:
            await client.close_all_sessions()
 
if __name__ == "__main__":
    asyncio.run(main())