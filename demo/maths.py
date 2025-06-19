from mcp.server.fastmcp import FastMCP

mcp=FastMCP(name="maths")

@mcp.tool()
def add(a:int,b:int)->int:
    return a+b

@mcp.tool()
def mul(a:int,b:int)->int:
    return a*b

if __name__ == "__main__":
    mcp.run(transport="stdio")