from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="weather", host="0.0.0.0", port=8001)

@mcp.tool()
async def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny ☀️"

if __name__ == "__main__":
    mcp.run()
