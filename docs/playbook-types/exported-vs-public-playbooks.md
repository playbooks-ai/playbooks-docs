# Exported vs Public Playbooks

## Exported Playbooks
Exported playbooks are a powerful feature of Playbooks AI that allows an agent to execute playbooks defined by another agent within its own execution context as if they were implemented locally within the importing agent.

>:bulb: Playbooks AI's exported playbooks capability is significantly more powerful than MCP's prompts because it enables true capability sharing and execution between agents, not just structured guidance. While MCP prompts are valuable for standardizing LLM interactions, Playbooks AI enables building extensible agent ecosystems with genuine code reuse and modular architectures.

## Public Playbooks
When an agent marks a playbook as public, another agent can call that playbook remotely.

>:bulb: Public playbooks are similar to MCP's tools. When a client calls a tool, it is executed on the MCP server. Similarly, when an agent calls a public playbook on another agent, it is executed on the called agent's server.

## How Exported Playbooks Work

When an agent exports a playbook, another agent can import implementation of that playbook and then execute that playbook within its execution context.

### Exporting Playbooks

>:warning: This feature under active development and not available yet.

Exported playbooks are marked using the `export` keyword:

````markdown
# AccountManagementAgent

```python
@playbook(export=True)
async def CloseAccount($user_id) -> str:
    """Close an account for a user."""
    # ...
```

## export: ProvisionAccount($user_id, $service_tier)
### Steps
- ...
````

In this example, the `AccountManagementAgent` exports the `CloseAccount` and `ProvisionAccount` playbooks.

>:bulb: Implementations of both markdown and Python playbooks can be exported.

### Importing Exported Playbook Implementations

To import a playbook's implementation from another remote agent, register that remote agent and then use the `import` statement:

```markdown
# AccountManagementAgent(url="https://acme.com/account-management")

# ServiceAgent
import CloseAccount, ProvisionAccount from AccountManagementAgent
```

This imports implementations of the `CloseAccount` Python playbook and the `ProvisionAccount` markdown playbook from the `AccountManagementAgent` agent.

### Using Imported Playbooks

Once imported, you can use the playbook just like any other playbook defined within your agent:

```markdown
## CreateAccount
### Steps
- Validate user information
- Create user record in database
- ProvisionAccount($user_id, $service_tier)
- Send welcome email to user
```

The imported `ProvisionAccount` playbook is called as if it were a local playbook.

## How Public Playbooks Work

>:warning: This feature under active development and not available yet.

When agent A marks a playbook as public, another agent B can **call that playbook remotely on a running instance of agent A**.

### Marking Playbooks as Public

To mark a playbook as public, use the `public` keyword:

```
# AuthenticationAgent
This agent handles user authentication.

## public: VerifyCredentials($username, $password)
### Steps
- Check credentials against secure store
- Return authentication result and user details if valid
```

Both markdown and Python playbooks can be marked as public.

### Calling Public Playbooks

To call a public playbook, first register the remote agent and then call the playbook as a method on that agent:

```
# AuthenticationAgent(url="https://acme.com/authentication")

# APIGatewayAgent

## HandleRequest
### Steps
- $auth_result = AuthenticationAgent.VerifyCredentials($request.auth.username, $request.auth.password)
- ...
```

Here, the `APIGatewayAgent` directly calls the `VerifyCredentials` playbook on the `AuthenticationAgent` instance running at `https://acme.com/authentication`. The playbook is executed on the remote agent's server and the result is returned to the calling agent.


## Differences Between Exported and Public Playbooks

Exported playbooks differ from public playbooks in several important ways:

|  | Exported Playbooks | Public Playbooks |
|---------|-------------------|----------------------|
| **Example** | `import CloseAccount from AccountManagementAgent` and then `CloseAccount($user_id)` | `# PaymentProcessingAgent("https://acme.com/ppa")` and then `PaymentProcessingAgent.ProcessPayment($amount, $payment_method)` |
| **Execution Context** | Local execution in importing agent's context | Remote procedure call on the remote agent instance |
| **State Access** | Can access local agent's state | Cannot access local agent's state |

## Security Considerations

>:boom: Be careful! Importing playbooks raise several security considerations.

1. **Code Injection**: An agent that imports playbooks from another agent must trust that agent. Importing playbook implementations from untrusted agents and executing them can lead to security vulnerabilities like code injection attacks.

2. **Version Control**: Changes to exported playbooks may affect importing agents, requiring careful version management.

## Example: Agent Ecosystem

Let's say that we have an ecosystem of three agents.

### 1. DatabaseAgent
```markdown
# DatabaseAgent
This agent provides database access capabilities.

## export: FindTable($query, $database)
### Steps
- List all tables in the $database
- Find the table that is most likely to contain data to answer the $query
- Return the table name
```

Let's say that `DatabaseAgent` is available at the URL `https://acme.com/database.agent`. It exports the `FindTable` playbook. It is a generic procedure for finding a database table.

### 2. AuthenticationAgent
```markdown
# AuthenticationAgent
This agent handles user authentication.

## public: VerifyCredentials($username, $password)
### Steps
- Check credentials against secure store
- Return authentication result and user details if valid
```

Let's say that an instance of the `AuthenticationAgent` is running at the URL `https://acme.com/authentication.agent`. The public `VerifyCredentials` playbook requires access to the secure store within ACME Corp's infrastructure.

### 3. APIGatewayAgent
APIGatewayAgent uses the above two agents. It first registers those two agents, specifying their URLs. Then it imports the `FindTable` playbook from the `DatabaseAgent`. It then remotely calls the `VerifyCredentials` playbook on the `AuthenticationAgent` instance. Finally, it locally executes the `FindTable` playbook.

```
# DatabaseAgent(url="https://acme.com/database.agent")

# AuthenticationAgent(url="https://acme.com/authentication.agent")

# APIGatewayAgent
import FindTable from DatabaseAgent

## HandleRequest
### Triggers
- When an API request is received
### Steps
- $auth_result = AuthenticationAgent.VerifyCredentials($request.auth.username, $request.auth.password)
- If $auth_result.success is true
  - $table_name = FindTable($request.query, $database)
  - Return $table_name
- Otherwise
  - Return authentication error
```

## Related Topics

- [Multi-Agent Programming](../tutorials/multi-agent-programming.md) - More about setting up and using multiple agents
- [Agent Communication](../agents/agent-communication.md) - How agents can communicate beyond playbook calls
- [Python Playbooks](python-playbooks.md) - How to create playbooks using Python
- [Markdown Playbooks](markdown-playbooks.md) - Standard playbook structure
