"""MCP Client Example
This client connects to the MCP server and demonstrates how to:
- Discover available tools
- Call tools with parameters
- Read resources from the server
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    """Main entry point - demonstrates MCP client-server communication."""

    # STEP 1: Define HOW to launch the server
    # StdioServerParameters tells the client how to start the server process
    server_params = StdioServerParameters(
        command="python",        # Use Python to run the server
        args=["server.py"],      # Path to the server script
    )

    # STEP 2: Establish connection to server
    # stdio_client opens a pipe (read/write channels) between client and server
    # The server launches automatically as a subprocess
    async with stdio_client(server_params) as (read, write):
        # ClientSession manages the MCP protocol over the connection
        async with ClientSession(read, write) as session:

            # STEP 3: Initialize - client and server exchange capabilities
            # This is the "handshake" that discovers what the server can do
            await session.initialize()

            # STEP 4: Discover available tools
            # Ask the server: "What tools do you have?"
            tools = await session.list_tools()
            print("Tools available on server:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # STEP 5: Call a tool with parameters
            # This is like calling a function on the remote server
            # Server receives the tool name and arguments, executes, and returns result
            result = await session.call_tool(
                "get_weather",                    # Which tool to call
                {"city": "Lahore"}                # Parameters to pass
            )
            print("\nTool result:", result.content[0].text)

            # STEP 6: Read a resource from the server
            # Resources are data (not functions) that the server exposes
            resource = await session.read_resource("notes://all")
            print("\nResource content:", resource.contents[0].text)

# Entry point: Run the async main function
asyncio.run(main())