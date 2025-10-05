# MCP Agents

## Overview

Connect to external MCP servers and expose their tools as callable playbooks.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how AI applications can access external tools and data sources. MCP servers expose tools that can perform various tasks like:

- Accessing databases
- Making API calls
- Performing calculations
- Interacting with file systems
- Running specialized algorithms
- And much more

## Create an MCP agent

To create an MCP agent, you need to specify the agent's metadata with remote configuration:

```md
# Example MCP Server
remote:
  type: mcp
  url: memory://test
  transport: memory

# Example MCP Client Agent

## Main

### Triggers
- When program starts

### Steps
- get secret from Example MCP Server
- reveal secret to user
- end program
```

### Configuration Options

The MCP agent configuration supports the following options:

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `type` | Yes | Must be `mcp` for MCP agents | - |
| `url` | Yes | The MCP server URL or command | - |
| `transport` | No | Transport type (`sse`, `stdio`, `websocket`) | `sse` |
| `timeout` | No | Timeout in seconds for tool calls | `30.0` |
| `auth` | No | Authentication configuration object | `{}` |

### Transport types

MCP agents support different transport protocols:

- SSE (Server-Sent Events)
- stdio
- WebSocket

## How MCP Agents Work

1. **Connection**: When the program starts, the MCP agent connects to the specified server
2. **Tool Discovery**: The agent automatically discovers all available tools from the server
3. **Playbook Creation**: Each MCP tool becomes a playbook that can be called
4. **Execution**: When a playbook is called, the agent forwards the request to the MCP server

## Use MCP tools as playbooks

Once connected, all MCP tools are automatically available as playbooks. You can call them just like any other playbook:

```md
# Weather MCP Agent
metadata:
  remote:
    type: mcp
    url: http://weather-service.example.com/mcp
    transport: sse
---
This agent connects to a weather MCP service.

# Weather Assistant
## Main
### Trigger
- When program starts

### Steps
- Say "Welcome to Weather Assistant! What location would you like weather for?"
- Get user's location
- Call Weather MCP Agent's get_current_weather with location=$location
- Display the weather: "Current weather in $location: $weather"
- End program
```

## Combine multiple MCP agents

You can use multiple MCP agents in a single program:

```md
# Weather MCP
metadata:
  remote:
    type: mcp
    url: http://weather-api.com/mcp
---
Weather service integration.

# News MCP
metadata:
  remote:
    type: mcp
    url: http://news-api.com/mcp
---
News service integration.

# Assistant
## DailyBriefing
### Steps
- Get weather from Weather MCP's get_current_weather for New York
- Get news from News MCP's get_top_headlines with technology category
- Create briefing combining weather and news
- Present briefing to user
```

## Authentication

For MCP servers that require authentication:

```md
# Secure API Agent
metadata:
  remote:
    type: mcp
    url: https://api.example.com/mcp
    transport: sse
    auth:
      type: bearer
      token: ${API_TOKEN}
---
Connects to a secured MCP endpoint.
```

## Run an MCP server (examples)

You can create simple MCP servers with `fastmcp`. Example servers in the repo:

- Insomnia server: `tests/data/insomnia/mcp.py`
- Travel advisor server: `tests/data/travel_advisor/mcp.py`

Run them with:

```bash
python tests/data/insomnia/mcp.py
python tests/data/travel_advisor/mcp.py
```

Then point your MCP agent `url` at the server (e.g., `http://localhost:8000` if using streamable-http) and set `transport` accordingly.
