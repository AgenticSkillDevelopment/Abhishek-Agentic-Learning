import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

async def run_detection_assistant():
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # === MCP Client config ===
    config_file = "mcp.json"  # Points to FastMCP server in `server.py`
    print("⚙️ Initializing Video Detection Assistant...")

    # === Initialize MCP Client & Agent ===
    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="qwen-qwq-32b")
    agent = MCPAgent(llm=llm, client=client, max_steps=5, memory_enabled=True)

    print("🤖 Interactive Video Detection Chat Assistant Ready")
    print("Type 'exit' or 'clear' anytime.\n")

    try:
        while True:
            user_input = input("🧑 You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Ending session.")
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
                print(f"❌ Error: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()
            print("🔒 Sessions closed.")

if __name__ == "__main__":
    asyncio.run(run_detection_assistant())
