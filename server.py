"""MCP Server Example
This server exposes tools and resources that clients (like Claude) can use.
- Tools: Functions that clients can call
- Resources: Data that clients can read
"""

import httpx  # Library for making HTTP requests
from mcp.server.fastmcp import FastMCP  # FastMCP framework for building servers
from urllib.parse import quote  # URL encode special characters in URLs

# Create an MCP server instance with a name
# The name identifies this server to clients connecting to it
mcp = FastMCP("weather-server")


@mcp.tool()  # Decorator: tells FastMCP this function is a tool clients can call
def get_weather(city: str) -> str:
    """Get real current weather for any city.
    
    This demonstrates:
    - Taking parameters from the client
    - Making external API calls
    - Returning results back to the client
    """
    
    # Clean user input: remove leading/trailing whitespace
    clean_city = city.strip()
    
    # URL-encode the city name to safely include in a URL
    # Example: "New York" becomes "New%20York"
    encoded_city = quote(clean_city)
    
    # Build the API URL for wttr.in weather service
    # format=3 requests a compact 1-line weather response
    url = f"https://wttr.in/{encoded_city}?format=3"
    
    # Make HTTP GET request to the weather API (10 second timeout)
    response = httpx.get(url, timeout=10)
    
    # Return the weather text back to the client
    return response.text


@mcp.tool()  # Another example tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.
    
    A simple example of a basic tool.
    """
    return a + b


@mcp.resource("notes://all")  # Resource: data that clients can read
def get_all_notes() -> str:
    """Return all notes.
    
    Resources are static or dynamic data available to clients.
    Clients read them with read_resource(\"notes://all\")
    """
    return "Your notes would go here..."


# This block runs only if script is executed directly (not imported)
if __name__ == "__main__":
    # Start the MCP server
    # It listens for client connections and processes tool/resource calls
    mcp.run()
