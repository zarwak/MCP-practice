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
#               ---A MORE SIMPLE TEMPLATE---
'''
# server.py
from mcp.server.fastmcp import FastMCP

# Create the server — give it a name
mcp = FastMCP("my-first-server")


# --- TOOL: Claude can call this like a function ---
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""   # ← Claude reads this docstring
    return a + b                       # to decide WHEN to call this tool


@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # In real life: call a weather API here
    return f"Weather in {city}: 32°C, humid"


# --- RESOURCE: Static or dynamic data Claude can read ---
@mcp.resource("notes://all")          # ← URI is the address
def get_all_notes() -> str:
    """Returns all saved notes."""
    return "Note 1: Study MCP\nNote 2: Build projects"


# --- PROMPT: Reusable prompt template ---
@mcp.prompt()
def analyze_topic(topic: str) -> str:
    """Generate a deep analysis prompt for any topic."""
    return f"Analyze '{topic}' covering: definition, use cases, limitations, future."


# Run the server
if __name__ == "__main__":
    mcp.run()  # default: stdio transport'''