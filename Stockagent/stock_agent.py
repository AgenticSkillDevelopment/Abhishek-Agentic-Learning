import os
from mcp.server.fastmcp import FastMCP
import yfinance as yf

# Optional: Set custom port using environment variable
os.environ["PORT"] = "8000"

# Create MCP server
mcp = FastMCP(name="stock_checker")

# Register stock price tool
@mcp.tool()
async def get_stock_price(symbol: str) -> str:
    try:
        stock = yf.Ticker(symbol)
        price = stock.info.get("regularMarketPrice")
        if price:
            return f"The current price of {symbol.upper()} is ${price:.2f}"
        else:
            return f"No price data available for {symbol.upper()}"
    except Exception as e:
        return f"Error fetching stock price: {e}"

# Run the server
if __name__ == "__main__":
    
    mcp.run(transport="streamable-http")
