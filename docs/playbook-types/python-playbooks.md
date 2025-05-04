# Python Playbooks

Python playbooks provide the full power and flexibility of Python within the Playbooks AI framework. They allow you to implement complex logic, integrate with external systems, and leverage the entire Python ecosystem.

## Overview

Python playbooks are ideal for:

- Complex calculations and algorithms
- Data processing and transformation
- Integration with external systems and APIs
- Implementing precise business logic
- Working with databases and file systems
- Handling structured data

## Creating Python Playbooks

Python playbooks are defined using the `@playbook` decorator applied to async Python functions in a ```python code block:

````
```python
@playbook
async def calculate_shipping(weight: float, destination: str) -> float:
    """Calculate shipping costs based on weight and destination."""
    base_rate = 5.99
    
    # Apply weight multiplier
    weight_cost = weight * 0.5
    
    # Apply destination surcharge
    destination_surcharge = get_destination_surcharge(destination)
    
    return base_rate + weight_cost + destination_surcharge
```
````

### The @playbook Decorator

The `@playbook` decorator registers a Python function as a playbook that can be called by other playbooks or triggered based on conditions.

```python
@playbook(
    triggers=["When user provides payment information"],
    public=True
)
async def process_payment(amount: float, card_info: dict) -> bool:
    """Process a payment transaction."""
    # Payment processing logic
    return True
```

#### Decorator Parameters

The `@playbook` decorator accepts several optional parameters:

- `triggers`: A list of trigger conditions (as strings) that will cause the playbook to execute
- `public`: A boolean indicating whether the playbook should be available to other agents
- `description`: An optional description of the playbook (the docstring is used if not provided)

### Type Annotations

Python playbooks should use type annotations for parameters and return values:

```python
@playbook
async def calculate_total(
    price: float,      # The price per item
    quantity: int,     # The number of items
    discount: float = 0.0  # Optional discount percentage
) -> float:            # The total price
    """Calculate the total price after applying discount."""
    total = price * quantity
    if discount > 0:
        total = total * (1 - discount / 100)
    return total
```

### Docstrings

Every Python playbook should include a docstring that explains:
- What the playbook does
- The purpose of each parameter
- What the return value represents
- Any side effects or important behavior notes

```python
@playbook
async def validate_address(address: dict) -> bool:
    """
    Validate a shipping address against postal service records.
    
    Args:
        address (dict): A dictionary containing address components:
            - street: The street address
            - city: The city name
            - state: The state/province code
            - zip: The postal/zip code
            - country: The country code (ISO 2-letter)
    
    Returns:
        bool: True if the address is valid, False otherwise
    
    Note:
        This playbook makes API calls to an external validation service
        and may have rate limits.
    """
    # Address validation logic
    return True
```

## Including Python Playbooks in Your Program

Python playbooks are included within markdown playbooks using code blocks:

````markdown
# Order Processing
This program handles order processing workflows.

```python
@playbook
async def calculate_tax(subtotal: float, state: str) -> float:
    """Calculate sales tax based on state."""
    tax_rates = {
        "CA": 0.0725,
        "NY": 0.045,
        "TX": 0.0625,
        # Other states...
    }
    
    default_rate = 0.05  # Default tax rate
    rate = tax_rates.get(state.upper(), default_rate)
    
    return subtotal * rate
```

## ProcessOrder
This playbook processes a new order.

### Triggers
- When user submits an order

### Steps
- Validate the order details
- Calculate the subtotal
- $tax = calculate_tax($subtotal, $customer.state)
- $total = $subtotal + $tax + $shipping
- Process the payment
- Create the order in the database
- Send confirmation to the customer
````


## Async and Await

All Python playbooks must be defined as `async` functions, and when calling other playbooks, you must use the `await` keyword:

```python
@playbook
async def process_order(order: dict) -> bool:
    """Process an order end-to-end."""
    # Validate order
    is_valid = await validate_order(order)
    if not is_valid:
        return False
    
    # Calculate costs
    subtotal = calculate_subtotal(order["items"])
    tax = await calculate_tax(subtotal, order["state"])
    shipping = await calculate_shipping(order["weight"], order["address"])
    
    # Process payment
    payment_success = await process_payment(subtotal + tax + shipping, order["payment"])
    
    return payment_success
```

## Public Python Playbooks

To make a Python playbook available to other agents to call, use the `public=True` parameter:

```python
@playbook(public=True)
async def currency_conversion(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert an amount between currencies using current exchange rates."""
    # Currency conversion logic
    return converted_amount
```

## Error Handling

Python playbooks should include proper error handling:

```python
@playbook
async def safe_api_call(endpoint: str, params: dict) -> dict:
    """Make a safer API call with error handling."""
    import requests
    
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        await Say("The service is taking too long to respond. Please try again later.")
        return {"error": "timeout"}
    except requests.exceptions.HTTPError as e:
        await Say(f"There was an error communicating with the service: {e}")
        return {"error": "http_error", "details": str(e)}
    except Exception as e:
        await Say("An unexpected error occurred. Please try again later.")
        return {"error": "unknown", "details": str(e)}
```

## Best Practices for Python Playbooks

1. **Keep functions focused**: Each playbook should do one thing well
2. **Use proper typing**: Include type annotations for all parameters and return values
3. **Add comprehensive docstrings**: Document what the playbook does and how to use it
4. **Handle errors gracefully**: Include try/except blocks and provide helpful error messages
5. **Be mindful of performance**: Consider execution time, especially for external API calls
6. **Use environment variables for secrets**: Never hardcode API keys or credentials
7. **Modularize complex logic**: Break down complex tasks into multiple playbooks
8. **Use consistent naming**: Follow a consistent convention for playbook names (usually snake_case)
9. **Test thoroughly**: Ensure playbooks handle edge cases and unexpected inputs
10. **Consider concurrency**: Use async patterns effectively for I/O-bound operations

## Related Topics

- [Markdown Playbooks](markdown-playbooks.md) - For structured, step-by-step flows
- [ReAct Playbooks](react-playbooks.md) - For reasoning-based, adaptive behavior
- [Python and Markdown Interop](../tutorials/python-markdown-interop.md) - How Python and markdown playbooks can work together
