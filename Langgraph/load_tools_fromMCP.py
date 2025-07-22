import json
import httpx
from langchain_core.tools import Tool

async def load_tools_from_mcp(registry_path: str) -> list[Tool]:
    # Load the registry config (a Python file that returns a dict)
    with open(registry_path, "r") as f:
        registry = json.load(f)

    tools = []

    for mcp in registry["mcpServers"]:
        name = mcp
        config = registry["mcpServers"][mcp]
        mcp_url = config["url"]

        # Fetch tool spec from MCP server
        async with httpx.AsyncClient() as client:
            res = await client.get(mcp_url)
            res.raise_for_status()
            spec = res.json()

        for t in spec["tools"]:
            tool_name = f"{name}::{t['name']}"
            tool_description = t["description"]
            tool_url = t["url"]

            async def tool_func(input_str: str, url=tool_url):
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, json={"input": input_str})
                    resp.raise_for_status()
                    result = resp.json()
                    return result.get("result", "⚠️ No result field in response.")

            tools.append(
                Tool(
                    name=tool_name,
                    description=tool_description,
                    func=tool_func
                )
            )

    return tools