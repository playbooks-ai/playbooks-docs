# Python Playbooks

In this tutorial, you'll learn how to create Python playbooks that can be used alongside markdown playbooks in your Playbooks AI programs.

## Objective

By the end of this tutorial, you'll understand:

- How to define playbooks using Python code
- How to use the `@playbook` decorator
- How to pass parameters and return values
- How to add triggers to Python playbooks

## Prerequisites

- Completion of [Calling Playbooks](calling-playbooks.md)
- Basic Python programming knowledge

## Why Use Python Playbooks?

While markdown playbooks are great for expressing workflows in natural language, Python playbooks allow you to:

- Implement complex logic and algorithms
- Integrate with external systems and APIs
- Process and transform data
- Perform calculations and validations
- Leverage existing Python libraries

## Creating a Basic Python Playbook

A Python playbook is a Python function decorated with the `@playbook` decorator:

```python
@playbook
async def greeting(name: str) -> str:
    return f"Hello, {name}! Welcome to Playbooks AI."
```

Key features:

- The `@playbook` decorator registers the function as a playbook
- Python playbooks must be async functions
- Parameter types and return types are specified using Python type hints

>:bulb: Python playbooks are executed as Python code, so must be valid Python code.

Python playbooks run in an isolated Python environment and can access all installed Python modules.

## Adding Python Playbooks to Your Program

Python playbooks are included within markdown playbooks using code blocks:

````markdown
# Python Demo
This program demonstrates Python playbooks.

```python
@playbook
async def greeting(name: str) -> str:
    return f"Hello, {name}! Welcome to Playbooks AI."
```

## Main
### Triggers
- At the beginning
### Steps
- Ask the user for their name
- $name = user's response
- $message = greeting($name)
- Tell the user: $message
- End program
````

Notice that:

1. The Python code is enclosed in a triple-backtick code block with the `python` language specifier
2. The markdown playbook can call the Python playbook just like any other playbook

## Adding Triggers to Python Playbooks

You can add triggers to Python playbooks using the `triggers` parameter:

````
```python
import math

@playbook(triggers=["When you want to apply magic operator to a number"])
async def magic_operator(input: str) -> float:
    input_num = float(input)
    return input_num * math.sin(input_num)
```
````

This Python playbook will be triggered when the condition "When you want to apply magic operator to a number" is met.

>:warning: Triggers are evaluated after each line in markdown playbook is executed. They are NOT evaluated during a Python playbook's execution.

## Public Python Playbooks

To make a Python playbook available to other [agents](../agents/index.md), you can use the `public` parameter:

```python
@playbook(public=True)
async def calculate_price(quantity: int, unit_price: float) -> float:
    return quantity * unit_price
```

Public playbooks can be called by other agents in a multi-agent system.

## Exercise

Consider the following Playbooks program:


```markdown
# Facts about nearby countries
This program prints interesting facts about nearby countries

## GetCountryFact($country)
### Steps
- Return an unusual historical fact about $country

## Main
### Triggers
- At the beginning
### Steps
- Ask user what $country they are from
- List 5 $countries near $country
- Tell the user that here are 5 nearby countries to the one they are from
- Inform the user that you will now tell them some interesting facts about each of the countries
- For each $country in $countries
  - $fact = GetCountryFact($country)
  - Tell the user: "$country: $fact"
- End program
```

Notice that the `Main` playbook loops through the list of countries and calls the `GetCountryFact` playbook for each country.

Let's use a Python playbook to execute the loop instead.

````
# Facts about nearby countries
This program prints interesting facts about nearby countries

```python
@playbook
async def process_countries(countries: list[str]) -> None:
    """
    Process all countries and tell the user about them

    Args:
        countries: A list of countries to process
    """
    for country in countries:
        fact = await GetCountryFact(country)
        await Say(f"{country}: {fact}")
```

## GetCountryFact($country)
### Steps
- Return an unusual historical fact about $country

## Main
### Triggers
- At the beginning
### Steps
- Ask user what $country they are from
- List 5 $countries near $country
- Tell the user that here are 5 nearby countries to the one they are from
- Inform the user that you will now tell them some interesting facts about each of the countries
- Process all countries
- End program
````

Notice that the `Main` playbook now calls the `process_countries` Python playbook with the list of countries. The `process_countries` playbook then calls the `GetCountryFact` markdown playbook for each country and a [built-in](../playbook-types/builtin-playbooks.md) `Say` playbook to tell the user about each country.

>:bulb: You can call markdown playbooks from Python playbooks and vice versa.

## Best Practices for Python Playbooks

- Use Python for complex logic and calculations
- Keep Python playbooks focused on a single task
- Handle errors gracefully with try/except blocks
- Use type hints to document parameters and return types
- Import only the libraries you need
- Document your Python playbooks with docstrings

### Using Docstrings

Add documentation to your Python playbooks using docstrings:

````
```python
@playbook
async def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculates the final price after applying a discount.
    
    Args:
        price: The original price
        discount_percent: The discount percentage (0-100)
        
    Returns:
        The final price after discount
    """
    if not 0 <= discount_percent <= 100:
        return("Discount percentage must be between 0 and 100")
    
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount
```
````

### External API Integration

Python playbooks are perfect for integrating with external APIs:

````
```python
import requests

@playbook
async def get_weather(city: str) -> dict:
    """Get weather information for a city"""
    
    api_key = os.environ.get("WEATHER_API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for HTTP errors
    
    return response.json()
```
````

## Next Steps

Now that you know how to create Python playbooks, you're ready to learn about [Advanced Triggers](../tutorials/triggers-advanced.md) to see how to use more complex triggers to control the execution of your playbooks.