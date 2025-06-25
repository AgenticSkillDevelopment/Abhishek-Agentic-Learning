import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
from uuid import uuid4
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from memory_store import JSONMemory  # <-- Add this import

async def run_memory_chat():
    load_dotenv()

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    config_file = "browser_mcp.json"

    # Generate dynamic session ID
    session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:8]}"
    memory = JSONMemory()  # <-- Create memory instance

    print(f"🧠 Session ID: {session_id}")
    print("Initializing MCP Client...")
    client = MCPClient.from_config_file(config_file)

    print("Loading Groq LLM (qwen-qwq-32b)...")
    llm = ChatGroq(model="qwen-qwq-32b")

    agent = MCPAgent(llm=llm, client=client, max_steps=5, memory_enabled=True)

    print("\n💬 Interactive Assistant Started")
    print("Type 'exit' to quit, 'clear' to reset memory.\n")

    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Exiting...")
                break
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("🧹 Memory cleared.")
                continue

            # Save user message
            memory.save(session_id, f"You: {user_input}")

            print("Assistant: ", end="", flush=True)
            try:
                response = await agent.run(user_input)
                print(response)

                # Save assistant response
                # Only save the assistant's final response (no user prompt, no <think>)
                if isinstance(response, str):
                    clean_response = response.strip().split("</think>\n")[-1] if "</think>" in response else response
                    memory.save(session_id, clean_response.strip())

            except Exception as e:
                print(f"⚠️ Error: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
