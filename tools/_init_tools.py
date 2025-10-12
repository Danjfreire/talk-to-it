from langchain.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

async def init_tools() -> list[BaseTool]:
    """Initialize and return a list of tools for the agent."""

    mcp_client = MultiServerMCPClient({
        "weather": {
            "transport": "stdio",
            "command": "python",
            "args": ["tools/weather.py"],
        }
    })

    return await mcp_client.get_tools()