# import os
# from dotenv import load_dotenv
# from mcp.server.fastmcp import FastMCP
# from langchain_core.messages import HumanMessage
# from graph import build_graph, State

# load_dotenv()
# mcp = FastMCP(name="ChatMemoryRAGAgent")

# @mcp.tool()
# async def ask_agent(message: str) -> str:
#     print("[DEBUG] ask_agent received:", message)
#     state = State(messages=[HumanMessage(content=message)])
#     result = build_graph().invoke(state)
#     return result.messages[-1].content

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from langchain_core.messages import HumanMessage
from graph import build_graph, State

load_dotenv()
mcp = FastMCP(name="ChatMemoryRAGAgent")

@mcp.tool()
async def ask_agent(message: str) -> str:
    print("[DEBUG] ask_agent received:", message)
    state = State(messages=[HumanMessage(content=message)])
    result = build_graph().invoke(state)
    return result.messages[-1].content

if __name__ == "__main__":
    mcp.run(transport="streamable-http")