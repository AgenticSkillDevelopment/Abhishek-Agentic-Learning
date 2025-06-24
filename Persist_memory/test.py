import asyncio
from main import ask_agent

async def run():
    result = await ask_agent("What is LangGraph?")
    print("Agent says:", result)

asyncio.run(run())
