import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient  # Assuming this is your utility wrapper

async def run_memory_chat():
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # MCP tool config file
    config_file = "stock_mcp.json"

    print("📡 Initializing Stock Price Assistant...")

    # Connect to MCP
    client = MCPClient.from_config_file(config_file)

    # Set up Groq model (use lighter model to avoid 'no healthy upstream')
    llm = ChatGroq(model="llama3-8b-8192")

    # Build the agent with memory
    agent = MCPAgent(llm=llm, client=client, max_steps=5, memory_enabled=True)

    print("💬 Interactive Stock Checker Assistant Ready (type 'exit' to quit)")

    try:
        while True:
            user_input = input("\n🧑 You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Ending chat.")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("🧹 Conversation history cleared.")
                continue

            print("🤖 Assistant: ", end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"\n❌ Error: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
