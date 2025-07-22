import os
import httpx
from mcp.server.fastmcp import FastMCP

# Load API key from environment or replace with your actual key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") or "YOUR_OPENWEATHERMAP_KEY"

# Create MCP server
mcp = FastMCP(name="weather_tool")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Fetch current weather data for a city from OpenWeatherMap API."""
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={WEATHER_API_KEY}&units=metric"
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()

        if response.status_code != 200:
            return f"❌ Could not fetch weather: {data.get('message', 'Unknown error')}"

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"🌤️ Weather in {city.title()}: {weather}, {temp}°C"

    except Exception as e:
        return f"⚠️ Error: {e}"

if __name__ == "__main__":
    os.environ["PORT"] = "8001"
    mcp.run(transport="streamable-http")
