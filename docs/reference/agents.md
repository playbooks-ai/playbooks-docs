---
title: Agents
---

# Agents

Agents are first-class runtime entities in Playbooks. They can:

- Run their own playbooks
- Send messages to other agents
- Call other agents’ [public playbooks](./exported-and-public-playbooks.md) directly
- Participate in multi-agent meetings

In multi-agent programs, use natural language to specify messaging, meetings, and public playbook calls.

# Playbooks AI Agents

## Create an agent
It is easy to create an AI agent using Playbooks.

```md
# Hello World Agent
This is a simple agent that says hello world.

## Main

### Trigger
- When program starts

### Steps
- Say Hello World!
- End program
```

This creates a Hello World agent.

## Create multiple agents
A program is a collection of agents. Agents that are part of a program can natively call each other's [public playbooks](./exported-and-public-playbooks.md).

```md
# Agent 1
## PB1
public: true
### Steps
- Say Hello

# Agent 2
## PB2
### Trigger
- When program starts
### Steps
- call Agent 1's PB1
- end program
```

## Create an agent backed by an MCP server
It is easy to create an agent that exposes tools from an MCP server as playbooks.

Say we have an MCP server running at `http://localhost:8088/mcp` that exposes a `get_weather(zipcode: int) -> dict` tool that takes a zipcode and returns a weather report.

```md
# MCP Agent
remote:
  type: mcp
  transport: streamable-http
  url: http://localhost:8088/mcp

# Local Agent
## Main
### Trigger
- When program starts
### Steps
- ask the user for a zipcode
- get the weather for that zipcode from MCP Agent
- describe the weather to the user
- end program
```