# Playbooks Protocol (Roadmap)

Protocols like [MCP](https://modelcontextprotocol.io/) and [A2A](https://google.github.io/A2A/) are emerging standards. Playbooks will support them, while also pursuing a native protocol optimized for playbook sharing and execution.

We are developing a new protocol that we believe will lead to more capable, flexible and secure multi-agent systems.

## Tools as API endpoints
The standard method for applications to expose their capabilities is through API endpoints. "Tools" in MCP are simply these public API endpoints. There are existing standards for API discovery and documentation, such as [OpenAPI](https://www.openapis.org/) and [Swagger](https://swagger.io/). We think that "tools" should be exposed through these existing standards.

So, along with supporting MCP as way to publish capabilities, playbooks will also support OpenAPI as way to publish capabilities.

## Tools as public methods
In Object-Oriented Programming, classes expose their capabilities through public methods. When an agent wants to publish its capabilities, why not use public methods of the agent? Playbooks has native support for [public playbooks](../agents/exported-and-public-playbooks.md), where an agent can expose certain playbooks for other agents or systems to call.

## Prompts vs playbooks
In MCP (Model Context Protocol), "prompts" are predefined templates or instructions that MCP servers can expose to client applications. They serve as reusable, parameterized templates that define specific ways to interact with or use the resources and capabilities that the MCP server provides. They help standardize common operations across different MCP implementations. For example, a "prompt" might expose a specific way to executing a coding task, or how data should be retrieved using specific queries, or even multi-step workflows.

Playbooks are multi-step workflows that can be executed reliably. They are a more powerful and flexible concept than prompts. We believe that exporting playbooks that can be executed by the caller within their own context is the most useful way to expose these capabilities. Playbooks has native support for [exporting playbooks](../agents/exported-and-public-playbooks.md). A Playbooks oriented protocol would allow seamless transfer and execution of such playbooks, through standard programming paradigms like "import" directives and function calls. Exported playbooks can be "imported" into another agent and then called and executed as if they were local playbooks.

## Playbooks as a standard
Playbooks can standardize how agents expose capabilities and how agents discover and use each other.

