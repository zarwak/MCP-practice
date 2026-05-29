# MCP Basic Template

A **simple, beginner-friendly template** for understanding the Model Context Protocol (MCP) from the ground up.

This repo demonstrates the **fundamental concepts and low-level mechanics** of how MCP works:
- How servers expose capabilities (tools, resources)
- How clients discover and invoke those capabilities
- How Claude Desktop connects to and uses custom MCP servers
- The complete flow: initialization → tool discovery → tool execution

Perfect for **learning the basics** of MCP before building your own advanced integrations.

---

## How It Works

Server exposes capabilities → Client discovers and calls them → Host (Claude Desktop / your app) orchestrates everything.

## The 3 primitives

| Primitive | What it is | Controlled by |
|-----------|-----------|---------------|
| @tool | Function Claude can call | Model decides when |
| @resource | Data Claude can read | App/user exposes |
| @prompt | Reusable prompt template | User triggers |

## What happens under the hood

```
Your App / Claude Desktop  ←→  MCP Client  ←→  MCP Server
     (HOST)                    (CONNECTOR)      (CAPABILITY)
```

### Flow

1. Host starts client
2. Client launches server as subprocess
3. Client sends: `initialize()` → server responds with its capabilities
4. Client sends: `list_tools()` → server returns tool schemas
5. Claude decides to call `get_weather` → client sends `call_tool("get_weather", {...})`
6. Server runs the function → returns result
7. Client passes result back to Claude → Claude uses it in response

## Project Structure

```
mcp-practice/
├── server.py        ← your MCP server
├── client.py        ← your test client
└── requirements.txt ← mcp[cli], httpx
```

## Step 3 — Run it (2 ways)

### Way 1 — MCP Inspector (best for learning, has a UI)

```bash
mcp dev server.py
```

Opens a browser UI at localhost:6274 where you can visually call your tools and see responses. Use this first.

### Way 2 — Run client manually

```bash
# Terminal 1 — nothing to run, client launches server automatically

# Just run the client
python client.py
```

## Step 4 — Connect to Claude Desktop

This is where it gets real — Claude itself calls your tool.

Find your Claude Desktop config file:

```bash
# Mac
~/Library/Application Support/Claude/claude_desktop_config.json

# Windows
%APPDATA%\Claude\claude_desktop_config.json
```

Add your server to it:

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "python",
      "args": ["/full/path/to/your/server.py"]
    }
  }
}
```

## Then:

- Save the file
- Fully quit Claude Desktop (not just close window)
- Reopen it
- Look for the 🔌 hammer icon in the chat input
- Type: "What's the weather in Lahore?"
- Watch Claude call your tool automatically
