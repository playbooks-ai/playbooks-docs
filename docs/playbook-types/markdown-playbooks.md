# Markdown Playbooks

Define prescribed workflows in natural language with clear triggers and steps.

## Overview

Markdown playbooks are ideal for:

- Prescribed business processes with clear steps
- Customer service workflows
- Support scripts
- Situations where the agent should follow a specific, predefined flow

## Structure

A markdown playbook follows this structure:

```markdown
## PlaybookName
Playbook description

### Triggers
- Trigger condition 1
- Trigger condition 2

### Steps
- Step 1
- Step 2
- Step 3

### Notes
- Note 1
- Note 2
```

### Playbook definition

The playbook is defined with a second-level heading (`##`) followed by the playbook name. By convention, playbook names use PascalCase (e.g., `GreetCustomer`, `ProcessOrder`), but they can be any text (e.g. `greet the customer`, `process_order`).

A description should follow the playbook name, explaining what the playbook does and when it should be used.

### Parameters

Playbooks can accept parameters, which are indicated in the playbook name:

```markdown
## CalculateDiscount($total, $membership_level)
This playbook calculates the appropriate discount based on the total order value and membership level.
```

These parameters will be available as variables within the playbook.

### Description placeholders

Playbook descriptions can include dynamic content using placeholder Python expressions with the `{expression}` syntax. This allows descriptions to be customized at runtime based on the current state and context.

:warning: Description placeholders are resolved when the playbook begins execution and are not re-evaluated during the execution of the playbook.

#### Basic syntax

Use curly braces to embed expressions in descriptions:

```markdown
## ProcessOrder
This playbooks processes order {$order_id} for customer {$customer_name}
```

The placeholders are resolved when the playbook is executed, showing the actual values to the LLM.

#### What you can use in placeholders

##### Variables
Reference any variable from the current state:
```markdown
## ReviewTransaction
Review transaction {$transaction_id} with amount ${$amount}
```

Note: The `$` prefix is optional - both `{$order_id}` and `{order_id}` work.

##### Playbook calls
Call other playbooks to generate dynamic content. No need to await the calls.
```markdown
## Answer questions about quarterly summaries
This playbook answers questions about quarterly summaries.
Q1: {QuarterlySummary("Q1")}
Q2: {QuarterlySummary("Q2")} 
Q3: {QuarterlySummary("Q3")}
Q4: {QuarterlySummary("Q4")}

### Steps
...
```

##### Python expressions
Use any valid Python expression:
```markdown
## AnalyzePerformance
Performance score: {round($score * 100, 2)}%
Status: {"Good" if $score > 0.8 else "Needs Improvement"}
Items to process: {len([x for x in $items if x.active])}
```

##### Special variables
Access agent information and current execution context:
```markdown
## DebugInfo
Current agent: {agent.klass}
Executing call: {current_playbook_call}
Full state: {agent.state}
```

#### How it works

1. When a playbook is executed, the description is scanned for `{expression}` patterns
2. Each expression is evaluated in the current context with access to:
      - All state variables
      - All available playbooks and functions
      - The agent object and its methods
      - Standard Python built-ins

3. The resolved values replace the placeholders in the description shown to the LLM
4. The original playbook description remains unchanged for future invocations

### Triggers

The `### Triggers` section defines the conditions under which the playbook should execute. The playbook will run when **any** of the listed triggers are met. See [Triggers](../triggers/index.md) for concepts and patterns.

Common trigger types include:

#### Temporal
```markdown
### Triggers
- At the beginning
- When program starts
- After 5 minutes
```

#### User interaction
```markdown
### Triggers
- When user provides their email
- When user asks about pricing
- When user wants to speak to a human
```

#### State‑based
```markdown
### Triggers
- When $balance becomes negative
- When $cart_total exceeds 100
- When $attempts is greater than 3
```

#### Execution flow
```markdown
### Triggers
- After calling VerifyIdentity
- Before calling ProcessPayment
- When CheckoutProcess fails
```

### Steps

The `### Steps` section contains a list of steps to execute, in order. Each step is a bullet point that describes an action to take:

```markdown
### Steps
- Greet the user and ask for their name
- $name = user's response
- If $name is empty
  - Ask for their name again
- Tell the user "Hello, $name! How can I help you today?"
```

Steps can include:

#### Imperative actions
```markdown
- Greet the user
- Ask the user for their order number
- Tell the user their order status
```

#### Variable assignments
```markdown
- $total = $price * $quantity
- $shipping_cost = CalculateShipping($weight, $destination)
- Extract $relevant_info from the search results
```

#### Conditional logic
```markdown
- If $order_total > 100
  - Apply free shipping
- If user is not satisfied
  - Offer a discount
  - Ask if they want to speak with a manager
- Otherwise
  - Thank them for their feedback
```

#### Loops
```markdown
- While conversation is active
  - Wait for user input
  - Respond appropriately
- For each $product in $cart
  - Calculate $product_total
  - Add $product_total to $grand_total
```

#### Calling other playbooks

Both markdown and Python playbooks can be called using Python function syntax or natural language instruction.

```markdown
- Validate the email
- ValidateEmail($email)

- Figure out how much it would cost to ship $weight to $destination
- $shipping_cost = CalculateShipping($weight, $destination)

- Process payment
- ProcessPayment(total=$order_total)

- Ask accountant to calculate the tax amount
- $tax_amount = Accountant.CalculateTax($order_total)
```

#### Control flow
```markdown
- End program
- Return $result
```

### Notes

The `### Notes` section provides additional guidance or rules for the playbook's execution:

```markdown
### Notes
- Maintain a professional tone throughout the conversation
- If the user mentions a competitor, highlight our unique advantages
- If the user is from California, mention that we're compliant with CCPA
```

Notes are used to handle exceptions, provide style guidance, or specify business rules that apply throughout the playbook.

## Example

Here's a complete example of a markdown playbook for handling order status inquiries:

```markdown
## CheckOrder_statusFlow($authToken)
Check the status of an order.

### Trigger
- When the user is authenticated and requests order status

### Steps
- Ask user for $order_id
- Get $order_status
- Extract $expected_delivery_date from $order_status
- Tell user when their order will be delivered

### Notes
- The $order_status dictionary includes the keys: order_id, expected_delivery_date.
- Always confirm that $authToken is valid before calling GetOrderStatus.
```

## Related topics

- [ReAct Playbooks](react-playbooks.md) - For less structured, reasoning-based approaches
- [Raw Prompt Playbooks](raw-prompt-playbooks.md) - For simple, one-off playbooks where you want to control the prompt entirely
- [Python Playbooks](python-playbooks.md) - For complex logic and integrations
- [Calling Playbooks](../guides/calling-playbooks.md) - How to call one playbook from another
- [Adding Triggers](../guides/adding-triggers.md) - More about trigger types and usage
