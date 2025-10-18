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

To create an MCP agent, you need to specify the agent's remote configuration. The agent acts as a proxy to the MCP server, making all its tools available as playbooks.

### Basic Example

```md
# My MCP
This agent provides various python tools.
remote:
  type: mcp
  url: http://127.0.0.1:8888/mcp
  transport: streamable-http
```

Once defined, you can call tools from the MCP server in your instructions:

```md
# Assistant
## Main
### Triggers
- When program starts

### Steps
- Call ListProjects from My MCP
- Display the project list to the user
- End program
```

### Configuration Options

The MCP agent configuration supports the following options:

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `type` | Yes | Must be `mcp` for MCP agents | - |
| `url` | Yes | The MCP server URL or command | - |
| `transport` | No | Transport type (`sse`, `stdio`, `websocket`, `streamable-http`) | `sse` |
| `timeout` | No | Timeout in seconds for tool calls | `30.0` |
| `auth` | No | Authentication configuration object | `{}` |

### Transport types

MCP agents support different transport protocols:

- **SSE (Server-Sent Events)**: Default transport for HTTP-based MCP servers
- **streamable-http**: HTTP-based streaming transport
- **stdio**: Standard input/output for local processes
- **WebSocket**: WebSocket-based transport for persistent connections

## How MCP Agents Work

1. **Connection**: When the program starts, the MCP agent connects to the specified server
2. **Tool Discovery**: The agent automatically discovers all available tools from the server
3. **Playbook Creation**: Each MCP tool becomes a playbook that can be called
4. **Execution**: When a playbook is called, the agent forwards the request to the MCP server

## Use MCP tools as playbooks

Once connected, all MCP tools are automatically available as playbooks. You can call them just like any other playbook:

```md
# Weather MCP
This agent connects to a weather MCP service.
remote:
  type: mcp
  url: http://weather-service.example.com/mcp
  transport: sse

# Weather Assistant
## Main
### Triggers
- When program starts

### Steps
- Say "Welcome to Weather Assistant! What location would you like weather for?"
- Get user's location
- Call get_current_weather from Weather MCP with location=$location
- Display the weather: "Current weather in $location: $weather"
- End program
```

## Combine multiple MCP agents

You can use multiple MCP agents in a single program:

```md
# Weather MCP
Weather service integration.
remote:
  type: mcp
  url: http://weather-api.com/mcp

# News MCP
News service integration.
remote:
  type: mcp
  url: http://news-api.com/mcp

# Assistant
## DailyBriefing
### Steps
- Call get_current_weather from Weather MCP for New York
- Call get_top_headlines from News MCP with technology category
- Create briefing combining weather and news
- Present briefing to user
```

## Authentication

For MCP servers that require authentication:

```md
# Secure API Agent
Connects to a secured MCP endpoint.
remote:
  type: mcp
  url: https://api.example.com/mcp
  transport: sse
  auth:
    type: bearer
    token: ${API_TOKEN}
```

## Run an MCP server (examples)

You can create simple MCP servers with `fastmcp`. Example servers in the repo:

- Insomnia server: `tests/data/insomnia/mcp.py`
- Travel advisor server: `tests/data/travel_advisor/mcp.py`
