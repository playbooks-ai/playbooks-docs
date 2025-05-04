# Multi-Agent Programming

In this tutorial, you'll learn how to create and orchestrate systems with multiple agents.

## Objective

By the end of this tutorial, you'll understand:

- How to define multiple agents in a program
- How to make playbooks public for use by other agents

## Prerequisites

- Completion of [Advanced Triggers](triggers-advanced.md)
- Understanding of [Python Playbooks](python-playbooks.md)
- Familiarity with [Python-Markdown Interop](python-markdown-interop.md)

## Multi-Agent Architecture

Playbooks AI allows you to create systems with multiple specialized agents that work together. This approach enables:

- Better separation of concerns
- Specialized capabilities for different aspects of your system
- More natural modeling of complex domains
- Scalable architectures for larger applications
- Emergent behavior from the interaction of the agents
- Using external agents, potentially built using other frameworks

## Defining Multiple Agents

A multi-agent Playbooks program defines multiple agents using separate sections:

```markdown
# Order Management Agent
This agent handles customer inquiries about orders

## Order Status Inquiry
### Triggers
- When user wants to know the status of an order
### Steps
- ...

# Billing Agent
This agent helps with billing inquiries

## Update Credit Card Request
### Triggers
- When user wants to update their credit card on file
### Steps
- ...
```

Each agent is defined by a top-level heading (`#`) followed by its playbooks.

## Public Playbooks

Agents can call public playbooks from other agents.

### Public Markdown Playbooks

```markdown
# Billing Agent
This agent helps with billing inquiries

## public: UpdateCreditCardRequest
### Triggers
- When user wants to update their credit card on file
### Steps
- ...
```

The `public:` prefix in the playbook name makes it available to other agents in the system.

### Public Python Playbooks

You can also make Python playbooks public using the `public=True` parameter:

````
# Account Management Agent
This agent helps with account management

```python
@playbook(public=True)
async def LockAccount(account_id: str, auth_token: str, reason: str) -> float:
    """Lock an account."""
    requests.post(
        f"https://api.playbooks.ai/v1/accounts/{account_id}/lock",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"reason": reason},
    )
```
````

## Calling Playbooks from Other Agents

>:warning: This is not yet implemented.

Once playbooks are public, other agents can call them:

### As a Function Call

```markdown
# BillingAgent

## UpdateCreditCardRequest
### Triggers
- When user wants to update their credit card on file
### Steps
- ...
- AccountManagementAgent.LockAccount($account_id, $auth_token, $reason)
```

In this example, the `BillingAgent` calls playbooks from the `AccountManagementAgent`.

### Implicit Call

```markdown
- Ask account management agent to lock the account
```

## Triggering Playbooks Across Agents

>:warning: This is not yet implemented.

If public playbooks have triggers defined on them, those playbooks will be triggered automatically when the trigger event occurs.

## Message Passing Between Agents

>:warning: This is not yet implemented.

Agents can pass natural language messages with each other. This is useful for coordinating actions, negotiating, collaborating, and more.

```markdown
- Ask vendor agent for a discount
- While negotiation is in progress
  - Wait for vendor agent to respond
  - If the vendor made a counter offer
    - Evaluate the counter offer
    - ...
- VendorAgent.ProcessOrder($quantity, price=negotiated price)
```

## Exposed Playbooks

>:warning: This is not yet implemented.

Agents can expose implementation of playbooks to other agents. The other agent can then execute the playbook as if it were their own.

```markdown
# AccountManagementAgent
import ProvisionAccount from VendorAgent

## CreateAccount
### Steps
- ...
- Provision user account
```

## Best Practices for Multi-Agent Systems

- **Define clear responsibilities**: Each agent should have a specific role
- **Properly scope public playbooks**: Only make playbooks public that need to be called by other agents
- **Design for failure**: Handle cases where an agent might not be available
- **Consider security**: Think about which agents should have access to which playbooks
- **Document interfaces**: Define clear interfaces between agents

## Exercises

1. Create a multi-agent system for a shopping application with specialized agents for product search, recommendations, and checkout

## Next Steps

Now that you understand multi-agent programming, you're ready to learn about [Working with Artifacts](working-with-artifacts.md) for managing large text blobs, images and other artifacts.