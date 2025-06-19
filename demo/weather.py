from mcp.server.fastmcp import FastMCP

mcp=FastMCP(name="weather")

@mcp.tool()
async def get_weather(city:str)->str:
    return f"the weather in {city} is sunny"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
    