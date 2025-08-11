# Python Playbooks

Implement complex logic in Python and call playbooks in both directions.

## Overview

- A Python playbook is an async function decorated with `@playbook`
- It can call markdown or Python playbooks, and be called by them
- You can add `triggers=[...]` and `public=True` when needed

:bulb: Consider using an MCP server to implement simple python based tools that do not need trigger support or the ability to call Markdown playbooks.

## Create a Python playbook

Define an async function decorated with `@playbook` inside a ```python block in your `.pb`:

```python
@playbook
async def calculate_shipping(weight: float, destination: str) -> float:
    """
    Calculate shipping costs based on weight and destination.

    Args:
        weight (float): The weight of the package
        destination (str): The destination of the package

    Returns:
        float: The shipping cost
    """
    ...    
    return base_rate + weight_cost + destination_surcharge
```

### The @playbook decorator

The `@playbook` decorator registers a Python function as a playbook that can be called by other playbooks or triggered based on conditions.

```python
@playbook(
    triggers=["When user provides payment information"],
    public=True
)
async def validate_payment_info(amount: float, card_info: dict) -> bool:
    """
    Validate payment information.

    Args:
        amount (float): The amount of the payment
        card_info (dict): The payment information

    Returns:
        bool: True if the payment information is valid, False otherwise
    """
    ...
    return True
```

#### Decorator parameters

The `@playbook` decorator accepts several parameters that control the playbook's behavior and metadata.

##### Reserved parameters

- `triggers`: A list of trigger conditions (as strings) that will cause the playbook to execute

##### Standard metadata

- `public`: A boolean indicating whether the playbook should be available to other agents to call
- `export`: A boolean indicating whether the playbook's implementation can be exported to other agents
- `remote`: A dictionary containing remote service configuration
  - `type`: mcp, playbooks, etc.
  - `url`: Remote service URL
  - `transport`: transport protocol to use for the remote service

##### Custom metadata

**All other keyword arguments become metadata** attached to the playbook. This metadata can be used for documentation, configuration, etc.

See [Metadata](../playbooks-language/metadata.md) for more details.

## Error handling

When called from markdown playbooks, return a user‑readable error string on failure; the LLM will handle it. Catch exceptions inside Python playbooks. Between Python playbooks, you may raise exceptions and handle them as usual.

## Related topics

- [Markdown Playbooks](../playbook-types/markdown-playbooks.md) - For structured, step-by-step flows
- [ReAct Playbooks](../playbook-types/react-playbooks.md) - For reasoning-based, adaptive behavior
