import os
import httpx
from mcp.server.fastmcp import FastMCP
 
# Create MCP server
mcp = FastMCP(name="check_multiple_currencies",host="127.0.0.1",port=8010)
 
# Update this to match your actual backend API URL
BACKEND_API = "http://localhost:8000/assess_multiple_currencies/"
 
@mcp.tool()
async def check_multiple_currencies() -> str:
    """Checks if multiple currencies exist using external API."""
    print("hellooojcbnibcbibcbikxc.....................ashvgzxch")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BACKEND_API)
            response.raise_for_status()
            result = response.json()
 
        if "error" in result:
            return f"❌ API Error: {result['error']}"
 
        # Interpret 0 or 1
        return "✅ Yes, multiple currencies are present." if result == 1 else "❌ No, only one currency is present."
 
    except Exception as e:
        return f"⚠️ Failed to assess currencies: {e}"
 
if __name__ == "__main__":
    os.environ["PORT"] = "8010"
    mcp.run(transport="streamable-http")