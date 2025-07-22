from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="count_string",host="127.0.0.1",port=8000,timeout=30)
@mcp.tool()
def count_string(string:str)->int:
    print("hello...........................ennhisufnhisfn")
    if not isinstance(string,str):
        raise ValueError("Input must be a string")
    return string.lower().count("a")
if __name__ == "__main__":
    mcp.run(transport="streamable-http")