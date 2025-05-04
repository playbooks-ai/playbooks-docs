# Markdown Playbooks

Markdown playbooks are used to define a business process that the agent should follow. They define agent behavior using a clear, step-by-step approach with explicit sections for triggers, steps, and notes.

## Overview

Markdown playbooks are ideal for:

- Prescribed business processes with clear steps
- Customer service workflows
- Support scripts
- Situations where the agent should follow a specific, predefined flow

## Structure of a Markdown Playbook

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

### Playbook Definition

The playbook is defined with a second-level heading (`##`) followed by the playbook name. By convention, playbook names use PascalCase (e.g., `GreetCustomer`, `ProcessOrder`), but they can be any text (e.g. `greet the customer`, `process_order`).

A description should follow the playbook name, explaining what the playbook does and when it should be used.

### Parameters

Playbooks can accept parameters, which are indicated in the playbook name:

```markdown
## CalculateDiscount($total, $membership_level)
This playbook calculates the appropriate discount based on the total order value and membership level.
```

These parameters will be available as variables within the playbook.

### Triggers Section

The `### Triggers` section defines the conditions under which the playbook should execute. The playbook will run when **any** of the listed triggers are met.

Common trigger types include:

#### Temporal Triggers
```markdown
### Triggers
- At the beginning
- When program starts
- After 5 minutes
```

#### User Interaction Triggers
```markdown
### Triggers
- When user provides their email
- When user asks about pricing
- When user wants to speak to a human
```

#### State-Based Triggers
```markdown
### Triggers
- When $balance becomes negative
- When $cart_total exceeds 100
- When $attempts is greater than 3
```

#### Execution Flow Triggers
```markdown
### Triggers
- After calling VerifyIdentity
- Before calling ProcessPayment
- When CheckoutProcess fails
```

### Steps Section

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

#### Imperative Actions
```markdown
- Greet the user
- Ask the user for their order number
- Tell the user their order status
```

#### Variable Assignments
```markdown
- $total = $price * $quantity
- $shipping_cost = CalculateShipping($weight, $destination)
- Extract $relevant_info from the search results
```

#### Conditional Logic
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

#### Playbook Calls
```markdown
- ValidateEmail($email)
- $shipping_cost = CalculateShipping($weight, $destination)
- ProcessPayment($order_total)
```

#### Control Flow
```markdown
- End program
- Return $result
```

### Notes Section

The `### Notes` section provides additional guidance or rules for the playbook's execution:

```markdown
### Notes
- Maintain a professional tone throughout the conversation
- If the user mentions a competitor, highlight our unique advantages
- If the user is from California, mention that we're compliant with CCPA
```

Notes are used to handle exceptions, provide style guidance, or specify business rules that apply throughout the playbook.

## Example: Customer Support Playbook

Here's a complete example of a markdown playbook for handling order status inquiries:

```markdown
## CheckOrderStatusFlow($authToken)
Check the status of an order.

### Trigger
- When the user is authenticated and requests order status

### Steps
- Ask user for $orderId
- $orderStatus = GetOrderStatus($orderId)
- Extract $expectedDeliveryDate from $orderStatus
- Say("Your order {$orderId} is expected to be delivered on {$expectedDeliveryDate}.")

### Notes
- The $orderStatus dictionary includes the keys: orderId, expectedDeliveryDate.
- Always confirm that $authToken is valid before calling GetOrderStatus.
```

## Best Practices for Markdown Playbooks

1. **Be specific and clear**: Write steps that clearly describe what the agent should do.
2. **Use variables consistently**: Use the `$` prefix for all variables and maintain consistent naming.
3. **Handle edge cases**: Include steps for handling unexpected user responses or system failures.
4. **Break down complex tasks**: Keep steps simple and focused on a single action.
5. **Use playbook calls**: Factor out reusable logic into separate playbooks that can be called.
6. **Provide helpful notes**: Use the Notes section to guide the agent on tone, exceptions, and business rules.
7. **Use meaningful trigger conditions**: Make trigger conditions specific to ensure playbooks run at the right time.

## Related Topics

- [ReAct Playbooks](react-playbooks.md) - For less structured, reasoning-based approaches
- [Python Playbooks](python-playbooks.md) - For complex logic and integrations
- [Calling Playbooks](../tutorials/calling-playbooks.md) - How to call one playbook from another
- [Adding Triggers](../tutorials/adding-triggers.md) - More about trigger types and usage
