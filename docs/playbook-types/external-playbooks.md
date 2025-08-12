---
title: External Playbooks
---

# External Playbooks

External playbooks are operations executed outside the local runtime. They behave like callable playbooks but do not call back into Playbooks.

Examples:

- MCP tools exposed by remote servers (see [MCP Agents](../agents/mcp-agent.md))
- HTTP APIs of external AI agents built with other frameworks
- (future) Exposed methods from an AI agent communicting using the A2A (Agent-to-Agent) protocol

Usage:

- Define an agent with `metadata.remote` of type `mcp` or point to an API
- Call its public tools/playbooks like any other playbook

Notes:

- External playbooks do not call Playbooks playbooks
- Handle authentication and transport per provider

## See also

- [MCP Agents](../agents/mcp-agent.md)
- [Playbooks Protocol](../advanced/playbooks-protocol.md)

