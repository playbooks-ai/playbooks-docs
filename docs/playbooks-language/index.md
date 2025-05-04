# Playbooks Language

Playbooks Language is a human-readable, semantically interpreted programming language designed specifically for building AI agents. It allows developers to define agent behavior using natural language within a structured markdown format, combined with the power and flexibility of Python.

## Overview

Playbooks Language enables you to:

- Write agent logic in a way that's understandable by both humans and AI
- Seamlessly integrate natural language instructions with Python code
- Create reusable, modular components that can be composed into complex workflows
- Implement event-driven behavior through triggers
- Build multi-agent systems where agents can communicate and collaborate

## Program Structure

A Playbooks program consists of one or more agents, each containing one or more playbooks. The basic structure follows standard markdown heading conventions:

````markdown
# Agent name
Agent description and overview

```python
# Python playbooks are defined here using the @playbook decorator
```

## Playbook name
Playbook description

### Triggers
- Trigger conditions

### Steps
- Step-by-step instructions

### Notes
- Additional notes, instructions and rules
````

### Program Components

#### 1. Agent Definition

Agents are defined using a top-level heading (`#`) followed by the agent name and an optional description:

```markdown
# Customer Service Agent
This agent handles customer service inquiries and guides users through the support process.
```

An agent can have multiple playbooks and can include Python code that's accessible to its playbooks.

#### 2. Python Functions as Playbooks

Python functions can be defined as playbooks using the `@playbook` decorator:

```python
@playbook
async def CalculateTotal(price: float, quantity: int) -> float:
    """Calculate the total price for a given quantity of items."""
    return price * quantity

@playbook(triggers=["When user provides payment information"])
async def ProcessPayment(amount: float, card_info: dict) -> bool:
    """Process a payment transaction."""
    # Payment processing logic
    return True
```

>:bulb: By convention, Playbook names are PascalCase. While Python functions are typically named using snake_case, we suggest using PascalCase for Python playbook names.

#### 3. Markdown Playbooks

Markdown playbooks are defined using second-level headings (`##`) followed by the playbook name and an optional description:

```markdown
## GreetCustomer
This playbook greets the customer and collects their basic information.
```

Playbooks can accept parameters:

```markdown
## CalculateDiscount($total, $membership_level)
This playbook calculates the appropriate discount based on the total and membership level.
```

#### 4. Triggers

Triggers define when a playbook should execute. They're specified in a section marked by a `### Triggers` heading. The playbook will execute when **any** of the triggers are met.

```markdown
### Triggers
- At the beginning
- When user provides their name
- When $order_total exceeds 100
```

#### 5. Steps

Steps define the actual logic of a playbook, specified in a section marked by a `### Steps` heading:

```markdown
### Steps
- Greet the user and ask for their $age
- If $age is less than 68
  - Tell the user about retirement products
- Otherwise
  - Tell the user about investment products
- End program
```

Steps support:

- Imperative instructions (e.g., "Greet the user")
- Variable assignments (e.g., "$total = $price * $quantity", "Extract $relevant_info from search results")
- Conditionals (e.g., "If $status is 'approved'", "If user is not satisfied with the answer")
- Loops (e.g., "While conversation is active", "While $attempts < 3", "For each $product in all products")
- Playbook calls (e.g., "ProcessPayment($amount)")
- Control flow (e.g., "End program", "Return $result")

>:bulb: When no steps are provided for a markdown playbook, the runtime treats the playbook's description as a ReAct-style prompt.

#### 6. Notes

The `### Notes` section can provide additional guidance or rules for the playbook:

```markdown
### Notes
- Maintain a professional tone throughout the conversation
- If the user mentions a competitor, highlight our unique advantages
- If the user is from California, mention that we're compliant with CCPA
```

## Variable Usage

Variables in Playbooks are denoted with a `$` prefix:

```markdown
- $total = $price * $quantity
- Tell the user their $total
```

Variables can store:

- Strings
- Numbers
- Booleans
- Lists
- Dictionaries
- Null values

## Example: Complete Playbooks program

Here's a complete example of a simple playbooks program:

````markdown
# CustomerSupportAgent
This agent handles customer support inquiries.

```python
@playbook(triggers=["When user provides order number"])
async def ValidateOrderNumber(order_number: str) -> bool:
    """Validate that an order number is in the correct format."""
    import re
    pattern = r"^ORD-\d{6}$"
    return bool(re.match(pattern, order_number))
```

## OrderStatus
This playbook helps customers check their order status.

### Triggers
- When user asks about order status

### Steps
- Greet the user and ask for their order number
- If order number is not valid
  - Tell the user their order number is invalid
  - Ask the user to provide a valid order number in the format ORD-XXXXXX
  - If order number is still not valid
    - Apologize and offer to connect them with a human agent
    - End program
- $order_details = LookUpOrder($order_number)
- Tell the user the current status of their order
- Ask if they need any additional assistance

### Notes
- If the user becomes frustrated, offer to connect them with a human agent
- Always thank the user for their patience
```
````
## Next Steps

- [Intermediate Representation](intermediate-representation.md) - How playbooks are transpiled for execution
