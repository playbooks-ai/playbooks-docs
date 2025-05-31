# Playbooks Protocol

Protocols like [MCP](https://modelcontextprotocol.io/) and [A2A](https://google.github.io/A2A/) are emerging as standards for multi-agent systems. Playbooks will [support these protocols](mcp-a2a.md), but we do not think that those protocols are the best way for AI agents to share their capabilities and communicate with each other.

We are developing a new protocol that we believe will lead to more capable, flexible and secure multi-agent systems.

## "Tools" exposed by services are simply API endpoints
The standard method for applications to expose their capabilities is through API endpoints. "Tools" in MCP are simply these public API endpoints. There are existing standards for API discovery and documentation, such as [OpenAPI](https://www.openapis.org/) and [Swagger](https://swagger.io/). We think that "tools" should be exposed through these existing standards.

So, along with supporting MCP as way to publish capabilities, playbooks will also support OpenAPI as way to publish capabilities.

## "Tools" are agent's public methods
In Object-Oriented Programming, classes expose their capabilities through public methods. When an agent wants to publish its capabilities, why not use public methods of the agent? Playbooks has native support for [public playbooks](../multi-agent-systems/exported-and-public-playbooks.md), where an agent can expose certain playbooks for other agents or systems to call.

## Expose Prompts or Playbooks?
In MCP (Model Context Protocol), "prompts" are predefined templates or instructions that MCP servers can expose to client applications. They serve as reusable, parameterized templates that define specific ways to interact with or use the resources and capabilities that the MCP server provides. They help standardize common operations across different MCP implementations. For example, a "prompt" might expose a specific way to executing a coding task, or how data should be retrieved using specific queries, or even multi-step workflows.

Playbooks are multi-step workflows that can be executed reliably. They are a more powerful and flexible concept than prompts. We believe that exporting playbooks that can be executed by the caller within their own context is the most useful way to expose these capabilities. Playbooks has native support for [exporting playbooks](../multi-agent-systems/exported-and-public-playbooks.md). A Playbooks oriented protocol would allow seamless transfer and execution of such playbooks, through standard programming paradigms like "import" directives and function calls. Exported playbooks can be "imported" into another agent and then called and executed as if they were local playbooks.

## Playbooks as a standard
Playbooks not only has the potential to be a stadard for exposing agnet capabilities to LLMs and for agent to agent communication, but it also has the potential to be a standardize how agents are described, discovered and used.

