# Playbooks Protocol — A Proposed Standard for Agent Interoperability and Skill Sharing

The Playbooks project is pursuing three complementary standards for AI agents:

* **Common Language Specification (CLS)** — a universal, human-readable, semantically precise format for defining agent behavior.
* **Common Language Runtime (CLR)** — a verifiable, transparent execution environment for running CLS programs with consistency and safety.
* **Playbooks Protocol** *(in exploration)* — a communication and capability-sharing standard that enables agents to call each other’s functions, import skills, and collaborate securely across systems.

The CLS and CLR define *how* agents are built and run. The Playbooks Protocol would define *how* they connect and share capabilities, forming the network layer of a unified AI agent stack.

## Purpose and Context

We are not building in isolation. Protocols like the **Model Context Protocol ([MCP](../agents/mcp-agent.md))** and **Agent-to-Agent (A2A)** are emerging standards for agent interoperability. Playbooks will support these where they fit, but we also see an opportunity for a native protocol optimized specifically for **playbook sharing and execution** — one that fully leverages the semantics, safety guarantees, and modularity of the Playbooks environment.

Our goal is a protocol that can make multi-agent systems more capable, flexible, and secure — without locking into brittle, ad-hoc integrations or over-indexing on any one coordination pattern.

## From Tools to Public Playbooks

In API design, capabilities are traditionally exposed as endpoints. MCP’s concept of listing *tools* fits this model — they are simply public API endpoints, discoverable and documented via existing standards like **OpenAPI** or **Swagger**. Playbooks will support these conventions so that agents publishing capabilities via MCP remain accessible in the wider ecosystem.

But object-oriented programming offers another useful analogy: public methods. In Playbooks, **public playbooks** are exactly that — specific workflows or functions that an agent intentionally exposes for others to call. Public playbooks can be invoked remotely, with typed parameters and structured return values, just like calling a local method.

## Beyond Prompts — Exported Playbooks

In MCP, *prompts* are reusable templates for common operations. They’re valuable, but limited: they don’t carry execution semantics, runtime safety, or multi-step control flow. Playbooks are richer — fully defined, auditable workflows that can be executed deterministically.

The Playbooks Protocol extends this further with **exported playbooks**: the actual code for a playbook, packaged for import into another agent’s environment. An agent can “import” an exported playbook from a trusted source and run it as if it were a local method. This allows agents to acquire entirely new skills — dynamically extending their capabilities without duplicating logic or reinventing proven workflows.

## Agent-to-Agent Collaboration

The Playbooks Protocol is designed to support multiple modes of collaboration between agents. Agents can:

* **Call public playbooks on other agents** directly, using RPC-style semantics with typed parameters and structured return values.
* **Exchange natural language messages** with other agents, conveying the semantic intent. The receiving agent can choose to execute a playbook to process the message and may respond with a natural language message. This enables multi-turn conversations for collaboration, negotiation and decision making.
* **Multi-party meetings** — For multi-party synchronous collaboration, Playbooks runtime offers a mechanisms for conducting "meetings". Each participant can follow their own playbook as the behavior guide for the meeting.

## Why Standardize

Without a shared protocol, agents remain silos — each with its own format for capabilities, its own invocation semantics, its own security assumptions. The Playbooks Protocol aims to solve this by:

* Defining a **portable, structured way to expose and discover capabilities**.
* Providing a **safe, verifiable mechanism** for executing remote capabilities and imported skills.
* Enabling **composability** so agents can be assembled into richer systems without custom glue for each integration.

When combined with CLS and CLR, the Playbooks Protocol could be a key part of an open, interoperable AI stack:

* **CLS** — defines the shape and semantics of agent logic.
* **CLR** — ensures any CLS-defined program runs predictably and safely.
* **Playbooks Protocol** — connects agents into a skill-sharing, capability-rich ecosystem.

This is like the network layer for the AI agent era — one that makes interoperability, discoverability, and trust first-class features rather than afterthoughts.

## See also

- [Exported and Public Playbooks](../agents/exported-and-public-playbooks.md)
- [MCP Agents](../agents/mcp-agent.md)
- [Agents](../agents/index.md)
