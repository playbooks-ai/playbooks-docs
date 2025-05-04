# Imported Playbooks

Imported playbooks are a powerful feature of Playbooks AI that allows an agent to execute playbooks defined by another agent within its execution context.

>:bulb: Playbooks AI's imported playbooks capability is significantly more powerful than MCP's prompts because it enables true capability sharing and execution between agents, not just structured guidance. While MCP prompts are valuable for standardizing LLM interactions, Playbooks AI enables building extensible agent ecosystems with genuine code reuse and modular architectures.

## Overview

Imported playbooks are ideal for:

- Creating specialized service agents that provide capabilities to other agents
- Enabling modular agent architectures
- Building extensible systems where capabilities can be added dynamically
- Implementing agent marketplaces where agents can share capabilities
- Enforcing separation of concerns between different parts of your system

## How Imported Playbooks Work

When an agent imports a playbook from another agent, it can execute that playbook as if it were defined within the importing agent itself. The execution occurs in the context of the importing agent, but the implementation is provided by the exporting agent.

### Syntax for Importing Playbooks

>:warning: This feature under active development and not available yet.

To import a playbook from another agent, use the `import` statement at the beginning of an agent definition:

```markdown
# AccountManagementAgent
import ProvisionAccount from VendorAgent
```

This imports the `ProvisionAccount` playbook from the `VendorAgent` and makes it available to use within the `AccountManagementAgent`.

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

## Differences from Direct Playbook Calls

Imported playbooks differ from direct cross-agent playbook calls in several important ways:

| Feature | Imported Playbooks | Direct Playbook Calls |
|---------|-------------------|----------------------|
| **Execution Context** | Runs in the importing agent's context | Runs in the exporting agent's context |
| **State Access** | Can access importing agent's state | Cannot access calling agent's state |
| **Return Values** | Returns values to the importing agent | Returns values to the calling agent |
| **Error Handling** | Errors are handled by the importing agent | Errors must be propagated back to the caller |
| **Syntax** | Used like a local playbook | Called with agent name prefix |

## Example: Service Provider Pattern

A common pattern is to create specialized service agents that provide capabilities to other agents:

```markdown
# PaymentProcessingAgent
This agent provides payment processing capabilities to other agents.

## export: ProcessPayment($amount, $payment_method)
This playbook processes a payment and returns a transaction ID.

### Steps
- Validate payment method
- Charge the payment method for the specified amount
- Generate transaction ID
- Record the transaction in the payment system
- Return the transaction ID

# ECommerceAgent
import ProcessPayment from PaymentProcessingAgent

## Checkout
### Triggers
- When user confirms their purchase
### Steps
- Calculate final total with tax and shipping
- Ask user for payment information
- $transaction_id = ProcessPayment($cart_total, $payment_info)
- Create order with the transaction ID
- Send order confirmation to user
```

In this example, the `ECommerceAgent` imports the `ProcessPayment` playbook from the `PaymentProcessingAgent` and uses it as part of its checkout process.

## Security Considerations

>:boom: Be careful! Imported playbooks raise several security considerations.

1. **Trust**: Importing agents must trust the exporting agents, as imported playbooks have access to the importing agent's context. This can lead to security vulnerabilities like code injection attacks.

2. **Permission Management**: Systems may need to implement permission schemes to control which playbooks can be imported and what they can access.

3. **Version Control**: Changes to exported playbooks may affect importing agents, requiring careful version management.

## Best Practices for Imported Playbooks

1. **Document the Interface**: Clearly document the parameters, return values, and expected behavior of exported playbooks.

2. **Define Versioning Strategy**: Use versioning to manage changes to exported playbooks without breaking importers.

3. **Limit Scope**: Export only the playbooks that are meant to be used by other agents.

4. **Error Handling**: Implement robust error handling in exported playbooks to avoid failures in importing agents.

5. **Test Integration**: Test the integration between agents extensively to ensure consistent behavior.

## Example: Agent Ecosystem

```markdown
# DatabaseAgent
This agent provides database access capabilities.

## export: QueryDatabase($query, $parameters)
### Steps
- Validate the query for security
- Execute the query with parameters
- Return the query results

# AuthenticationAgent
This agent handles user authentication.

## export: VerifyCredentials($username, $password)
### Steps
- Check credentials against secure store
- Return authentication result and user details if valid

# APIGatewayAgent
import QueryDatabase from DatabaseAgent
import VerifyCredentials from AuthenticationAgent

## HandleRequest
### Triggers
- When an API request is received
### Steps
- $auth_result = VerifyCredentials($request.auth.username, $request.auth.password)
- If $auth_result.success is true
  - $data = QueryDatabase($request.query, $request.parameters)
  - Return successful response with $data
- Otherwise
  - Return authentication error
```

This example demonstrates an ecosystem of specialized agents that work together through imported playbooks to handle API requests.

## Related Topics

- [Multi-Agent Programming](../tutorials/multi-agent-programming.md) - More about setting up and using multiple agents
- [Agent Communication](../agents/agent-communication.md) - How agents can communicate beyond playbook calls
- [Python Playbooks](python-playbooks.md) - How to create playbooks using Python
- [Markdown Playbooks](markdown-playbooks.md) - Standard playbook structure
