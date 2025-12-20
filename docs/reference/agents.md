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

## Waiting for agent responses

When an agent waits for a response from another agent, Playbooks uses **adaptive waiting** - intelligent, context-aware waiting without hard timeouts.

### How it works

Instead of rigid timeouts that force binary wait-or-abort decisions, agents receive periodic notifications (every 5 seconds) while waiting:

- **Status updates** showing how long they've been waiting
- **Interrupt messages** from other sources (user, other agents)
- **The opportunity** to decide whether to continue waiting, take alternative action, or escalate

The agent's LLM makes contextual decisions based on task urgency, expected wait times, and available alternatives. There is no hard maximum wait time.

### Providing context

Use the **Notes section** to give agents guidance about expected wait times and alternatives:

```md
# SupportAgent
## HandleRefundRequest
### Steps
- Ask user for their order ID
- Ask OrderVerification agent to verify the order
- Wait for verification result
- If order is verified
  - Process refund
- Otherwise
  - Inform user verification failed

### Notes
- Order verification typically takes 3-5 seconds
- If verification takes longer than 30 seconds, there may be a backend issue
- Consider offering to escalate to a supervisor in that case
```

### Example behavior

**At 5 seconds**: Agent sees typical time is 3-5 seconds, decides to keep waiting.

**At 15 seconds**: Agent informs user: "Verification is taking longer than usual, please bear with me..."

**At 30 seconds**: Agent reaches the threshold mentioned in Notes and offers to escalate: "Would you like me to escalate this to a supervisor?"

If OrderVerification responds at any point, the agent immediately continues with the normal workflow. Adaptive waiting is transparent when everything works as expected.

### Example: Alternative strategies

```md
# DataCoordinator
## FetchAnalytics
### Steps
- Ask DataAgent for the analytics report
- Wait for the report
- Present the report to user

### Notes
- DataAgent typically responds in 5-10 seconds
- If no response after 15 seconds, check StatusAgent for service status
- If the service is down, inform user and offer to open a support ticket
```