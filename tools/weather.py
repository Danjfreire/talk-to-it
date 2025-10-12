from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
def get_weather(location: str) -> str:
    """Gets the current weather for a given location."""
    return f"It is currently sunny in {location}."


if __name__ == "__main__":
    mcp.run(transport="stdio")