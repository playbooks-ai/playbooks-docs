# Advanced Triggers

In this tutorial, you'll explore more advanced trigger patterns and use cases in Playbooks AI.

## Objective

By the end of this tutorial, you'll understand:

- How to create complex data validation triggers
- How to use sentiment and intent-based triggers
- How to implement communication-based triggers
- How to build robust error handling with triggers

## Prerequisites

- Completion of [Basic Triggers](adding-triggers.md)
- Understanding of [User Interaction](user-interaction.md)
- Familiarity with [Calling Playbooks](calling-playbooks.md)

## Data Validation Triggers

One powerful application of triggers is data validation. You can create playbooks that automatically trigger when users provide certain types of data:

```markdown
## Main
### Triggers
- At the beginning
### Steps
- Tell the user this is a banking system
- Ask the user for their account number
- Ask the user for their PIN
- Load account information
- ...

## AccountNumberValidation
### Triggers
- When user provides an account number
### Steps
- While account number is not exactly 10 digits
  - Tell the user their account number is invalid
  - Ask the user to provide a valid 10-digit account number
  - If the user wants to quit
    - End program
- Return the account number

## PinValidation
### Triggers
- When user provides a PIN
### Steps
- While PIN is not exactly 4 digits
  - Tell the user their PIN is invalid
  - Ask the user to provide a valid 4-digit PIN
  - If the user has made 3 failed attempts
    - Lock user account
    - Tell the user their account is locked
    - End program
- Return the PIN
```

This pattern:

- Separates validation logic from the main workflow
- Automatically triggers validation when specific data is provided
- Provides clear error messages and recovery paths

## Sentiment-Based Triggers

You can create triggers that respond to user sentiment, enabling more natural conversations:

```markdown
## AngryCustomerResponse
### Triggers
- When user is frustrated or abusive
### Steps
- Apologize to the user for the frustration
- Offer to connect them with a human support agent
- Ask if they would like to continue or speak with a human
- ...
```

This trigger activates when the system detects negative sentiment in the user's messages, allowing for empathetic responses at the right time.

## Intent-Based Triggers

Similar to sentiment, you can create triggers based on user intent:

```markdown
## AccountBalanceInquiry
### Triggers
- When user wants to know their account balance
### Steps
- ...
```

This trigger activates when the user expresses a need for help or shows signs of confusion, providing assistance without explicit commands.

## Communication-Based Triggers

In multi-agent systems, triggers can respond to messages from other agents:

```markdown
## StockUpdateNotification
### Triggers
- When you receive message from InventoryAgent asking for stock level
### Steps
- ...
```

This allows agents to communicate and react to information shared by other agents.

## Error Handling with Triggers

Triggers can implement robust error handling patterns:

```markdown
## MissingPlaybook
### Triggers
- When no suitable playbook is available
### Steps
- Tell the user that an error occurred
- ...
```

This creates a centralized error handling approach that can cover your entire application.

## Combining Multiple Trigger Types

For complex scenarios, you can combine multiple trigger types:

```markdown
## SecurityAlert
### Triggers
- When user attempts more than 3 failed logins
- When user attempts more than 3 failed credit card transactions
### Steps
- Log the security concern
- ...
```

This pattern creates sophisticated security monitoring by evaluating multiple risk factors.

## Best Practices for Advanced Triggers

- **Prioritize user experience**: Use triggers to make conversations feel natural and responsive
- **Handle edge cases**: Create specific triggers for error conditions and unusual scenarios
- **Test thoroughly**: Complex trigger systems need careful testing with various user inputs
- **Document your trigger strategy**: Make it clear which triggers exist and when they activate

## Exercises

1. Implement a simple customer support agent who helps with order status and account renewal requests.

## Next Steps

Now that you understand advanced trigger patterns, you're ready to explore [Multi-Agent Programming](multi-agent-programming.md) to create systems with multiple specialized agents. 