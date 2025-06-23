from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="count_string", host="0.0.0.0", port=8002)

@mcp.tool()
def count_string(string: str) -> int:
    return string.lower().count("a")

if __name__ == "__main__":
    mcp.run()
