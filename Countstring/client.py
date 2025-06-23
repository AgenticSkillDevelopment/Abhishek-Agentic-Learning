# count_string_assistant.py

import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient  # Make sure mcp_use is installed or available

async def run_memory_chat():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found in environment or .env file")
    os.environ["GROQ_API_KEY"] = api_key

    config_file = "browser_mcp.json"
    print("📡 Initializing AI Assistant for `count_string` tool...")

    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="qwen-qwq-32b")

    agent = MCPAgent(llm=llm, client=client, max_steps=5, memory_enabled=True)

    print("💬 Interactive Assistant Ready (type 'exit' to quit, 'clear' to reset memory)\n")

    try:
        while True:
            user_input = input("🧑 You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Ending chat.")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("🧹 Memory cleared.")
                continue

            print("🤖 Assistant:", end=" ", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
