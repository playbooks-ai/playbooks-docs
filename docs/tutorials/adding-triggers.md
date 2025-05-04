# Adding Triggers

In this tutorial, you'll learn how to use triggers to control when your playbooks execute.

## Objective

By the end of this tutorial, you'll understand:
- What triggers are and why they're useful
- How to define different types of triggers in your playbooks
- How to execute playbooks conditionally using triggers

## Prerequisites

- Completion of [Anatomy of a Playbook](anatomy-of-a-playbook.md)
- A basic understanding of playbook structure

## What Are Triggers?

Triggers are conditions that determine when a playbook should execute. They enable semantic event-driven programming. Rather than relying on complex if-else statements, you can define in plain English when your playbook should run.

## Types of Triggers

Playbooks AI supports several types of triggers:

### 1. Temporal Triggers

Temporal triggers execute playbooks at specific times or moments:

```markdown
### Triggers
- At the beginning

### Triggers
- When the program ends
```

### 2. State-Based Triggers

State-based triggers execute playbooks when variables reach certain states or values:

```markdown
### Triggers
- When $x becomes larger than 15
- When $account_balance is negative
```

### 3. Execution Flow Triggers

Execution flow triggers execute playbooks before, during, or after other playbooks:

```markdown
### Triggers
- After calling LoadAccount
- Before calling ProcessPayment
```

### 4. User Interaction Triggers

User interaction triggers execute playbooks in response to user actions:

```markdown
### Triggers
- When user provides a PIN
- When user wants to know the account balance
```

## Example: Using Multiple Types of Triggers

Let's create a more complex example that uses different types of triggers:

```markdown
# Account Management
This program demonstrates various types of triggers.

## Main
### Triggers
- At the beginning
### Steps
- Ask user for a PIN
- Ask user for email
- $x = 10
- Load user account
- $x = $x * 2
- Tell the user their account balance

## LoadAccount($email, $pin)
### Steps
- Return {"balance": 8999}

## Validation
### Triggers
- When user provides a PIN
### Steps
- While PIN is not 4 digits
  - Tell user PIN is not valid and ask for PIN again
  - If the user gives up
    - Apologize and end the conversation
- Return PIN

## TooBig
### Triggers
- When $x > 15
### Steps
- Tell user $x is too big

## AccountLoaded
### Triggers
- After calling LoadAccount
### Steps
- Tell user that you have loaded their account
```

In this example:

1. The `Main` playbook runs at the beginning
2. When the user provides a PIN, the `Validation` playbook runs to verify it
3. When the variable `$x` becomes greater than 15, the `TooBig` playbook runs
4. After the `LoadAccount` playbook is called, the `AccountLoaded` playbook runs

## Creating a Playbook with Triggers

Let's create a simpler version that demonstrates triggers:

1. Create a new file named `triggers-demo.md` with the following content:

```markdown
# Trigger Demo
This program demonstrates different types of triggers.

## Main
### Triggers
- At the beginning
### Steps
- Tell the user this is a trigger demonstration
- $counter = 5
- Ask the user to provide a number
- $counter = $counter * 2
- Tell the user that the counter is now $counter
- End program

## BigNumber
### Triggers
- When $counter > 15
### Steps
- Tell the user that the counter has exceeded 15
- Tell the user that this message was triggered automatically
```

2. Run your playbook:

```bash
python src/playbooks/applications/agent_chat.py triggers-demo.md --verbose
```

3. When you run this program and enter a value, you should notice:
   - The `Main` playbook executes at the start
   - If your inputs cause `$counter` to exceed 15, the `BigNumber` playbook executes automatically

## How Triggers Work

When you run a Playbooks AI program:

1. The framework monitors the program state, including variables, user inputs, and execution flow
2. When a state change occurs (e.g., a variable is updated) or a step is executed, the framework checks all trigger conditions
3. If any trigger conditions are met, the corresponding playbooks are queued for execution
4. Triggered playbooks execute after the current step completes

## Best Practices for Using Triggers

- Use clear and specific trigger conditions
- Avoid trigger loops where playbooks could trigger each other indefinitely
- Use state-based triggers (`When $x > 15`) to handle exceptions rather than checking conditions in steps so that the main playbook does not become too complex
- Consider the execution order when using multiple triggers

## Advanced Trigger Patterns

### Chaining Triggers

You can create chains of triggers where one playbook triggers another:

```markdown
## Step1
### Triggers
- At the beginning
### Steps
- $x = 10

## Step2
### Triggers
- When $x becomes 10
### Steps
- $y = 20

## Step3
### Triggers
- When $y becomes 20
### Steps
- Tell the user the chain is complete
```

### Combining Trigger Conditions

You can use multiple trigger conditions for a single playbook:

```markdown
## EmergencyAlert
### Triggers
- When $temperature > 90
- When $pressure < 30
- When user reports an emergency
### Steps
- Alert the maintenance team
```

### Triggering Multiple Playbooks

Multiple playbooks can be triggered by the same condition, creating a fan-out pattern where a single event causes multiple playbooks to execute:

```markdown
## UpdateInventory
### Triggers
- When an item is purchased
### Steps
- Reduce the inventory count for the purchased item
- If inventory is below reorder threshold
  - Flag item for reordering

## NotifyShipping
### Triggers
- When an item is purchased
### Steps
- Create a shipping label
- Notify the warehouse to prepare the package

## RecordSale
### Triggers
- When an item is purchased
### Steps
- Record the sale details in the accounting system
- Update sales analytics dashboard
```

In this example, when an item is purchased:

1. `UpdateInventory` executes to adjust inventory counts
2. `NotifyShipping` executes to start the shipping process
3. `RecordSale` executes to record financial details

This pattern allows you to:

- Separate concerns into distinct playbooks
- Add new behaviors without modifying existing playbooks
- Create modular, maintainable event-driven systems

Caution! The framework does not guarantee the order of execution of triggered playbooks, so those playbooks should be independent of each other.

## Exercises

1. Modify the trigger demo to add a new playbook that triggers when the user enters a specific word
2. Create a playbook with multiple trigger conditions
3. Create a chain of three playbooks that trigger each other in sequence

## Next Steps

Now that you understand how to use triggers, you're ready to learn about [User Interaction](user-interaction.md) in Playbooks AI. 