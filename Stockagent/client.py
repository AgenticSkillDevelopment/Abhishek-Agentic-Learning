from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def main():
    # Set API key
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Connect to MCP server
    client = MultiServerMCPClient(
        {
            "stock": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    # Fetch tools safely
    try:
        print("Fetching tools from MCP server...")
        tools = await client.get_tools()
        print("✅ Tools loaded:", [tool.name for tool in tools])
    except Exception as e:
        print("❌ Failed to load tools:", e)
        return

    # Load Groq model
    model = ChatGroq(model="llama3-8b-8192")  # Replace with your preferred model

    # Create REACT agent
    agent = create_react_agent(model, tools)

    # Query the agent
    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "What is the stock price of AAPL?"}
        ]
    })

    print("📈 Stock Price Response:", response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
