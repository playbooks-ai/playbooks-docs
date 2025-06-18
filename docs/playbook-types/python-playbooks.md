# Python Playbooks

Python playbooks provide the full power and flexibility of Python within the Playbooks AI framework. They allow you to implement complex logic, integrate with external systems, and leverage the entire Python ecosystem.

## Overview

Python playbooks are python functions that can be called by other Markdown/Python playbooks, and **can call Markdown/Python playbooks**. These can also be conditionally triggered.

:bulb: Consider using an MCP server to implement simple python based tools that do not need trigger support or the ability to call Markdown playbooks.

## Creating Python Playbooks

Python playbooks are defined using the `@playbook` decorator applied to async or normal Python functions in a ```python code block:

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

### The @playbook Decorator

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

#### Decorator Parameters

The `@playbook` decorator accepts several parameters that control the playbook's behavior and metadata.

##### Reserved Parameters

- `triggers`: A list of trigger conditions (as strings) that will cause the playbook to execute

##### Standard Metadata Parameters

- `public`: A boolean indicating whether the playbook should be available to other agents to call
- `export`: A boolean indicating whether the playbook's implementation can be exported to other agents
- `remote`: A dictionary containing remote service configuration
  - `type`: mcp, playbooks, etc.
  - `url`: Remote service URL
  - `transport`: transport protocol to use for the remote service

##### Custom Metadata

**All other keyword arguments become metadata** attached to the playbook. This metadata can be used for documentation, configuration, etc.

See [Metadata](../playbooks-language/metadata.md) for more details.

## Error Handling

For Python playbooks that are called from Markdown playbooks, return a string with the error message, regardless of the return type of the function. This returned error message will be processed by the LLM and handled intelligently. Always catch all exceptions because Markdown playbooks do not handle Python exceptions.

For Python playbooks that are called from other Python playbooks, use standard error handling such as raising exceptions.

## Related Topics

- [Markdown Playbooks](../playbook-types/markdown-playbooks.md) - For structured, step-by-step flows
- [ReAct Playbooks](../playbook-types/react-playbooks.md) - For reasoning-based, adaptive behavior
