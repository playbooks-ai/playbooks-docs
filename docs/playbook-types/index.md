# Playbook Types

Playbooks AI supports multiple types of playbooks, each with its own strengths and use cases. This flexibility allows you to choose the right tool for each aspect of your agent's behavior.

## Overview of Playbook Types

### [Markdown Playbooks](markdown-playbooks.md)

Markdown playbooks use a structured format with clear sections for triggers, steps, and notes. They are ideal for:

- Prescribed business processes with clear steps
- Customer service workflows
- Support scripts
- Situations where the agent should follow a specific, predefined flow

```markdown
## GreetCustomer
This playbook greets the customer and collects their information.

### Triggers
- At the beginning

### Steps
- Greet the user and ask for their name
- Ask the user how you can help them today
```

### [ReAct Playbooks](react-playbooks.md)

ReAct playbooks leverage the LLM's reasoning capabilities through a descriptive prompt. They are ideal for:

- Complex problem-solving tasks
- Research and information gathering
- Dynamic planning
- Situations requiring flexible, adaptive behavior

```markdown
## ResearchProduct
Research information about a product the user is interested in.

Search for detailed product information, customer reviews, 
pricing data, and comparisons with similar products. Analyze 
the information to provide a comprehensive overview that 
helps the user make an informed decision.
```

### [Python Playbooks](python-playbooks.md)

Python playbooks give you the full power of Python for complex logic and external integrations. They are ideal for:

- Complex calculations
- Data processing and transformation
- Integration with external systems and APIs
- Implementing business logic

````
```python
@playbook
async def CalculateShipping(weight: float, destination: str) -> float:
    """Calculate shipping costs based on weight and destination."""
    base_rate = 5.99
    
    # Apply weight multiplier
    weight_cost = weight * 0.5
    
    # Apply destination surcharge
    destination_surcharge = get_destination_surcharge(destination)
    
    return base_rate + weight_cost + destination_surcharge
```
````

## Mixing Playbook Types

One of the powerful features of Playbooks AI is the ability to mix different types of playbooks within the same agent or program. This allows you to define your agent's behavior in a flexible and modular way.

## Next Steps

Explore each playbook type in detail:

- [Markdown Playbooks](markdown-playbooks.md) - For structured, step-by-step flows
- [ReAct Playbooks](react-playbooks.md) - For reasoning-based, adaptive behavior
- [Python Playbooks](python-playbooks.md) - For complex logic and integrations

Also see:

- [Exported and Public Playbooks](../agents/exported-and-public-playbooks.md) - For multi-agent systems
- [Multi-Agent Programming](../agents/index.md) - For creating multi-agent systems