import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

async def run_query():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing GROQ_API_KEY in .env")
    os.environ["GROQ_API_KEY"] = api_key

    client = MCPClient.from_config_file("browser_mcp.json")
    llm = ChatGroq(model="qwen-qwq-32b")

    agent = MCPAgent(llm=llm, client=client, max_steps=5, memory_enabled=False)

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(f"🤖 Assistant is processing: {user_input}")
        response = await agent.run(user_input)
        print(response)
    else:
        print("Please provide a query as a command line argument.")
    
    await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_query())
