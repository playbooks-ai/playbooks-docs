# Calling Playbooks

In this tutorial, you'll learn how to call one playbook from another to create modular, reusable components.

## Objective

By the end of this tutorial, you'll understand:

- How to define playbooks that accept parameters
- How to call one playbook from another
- How to capture and use return values from playbooks
- How to create modular, reusable playbook components

## Prerequisites

- Completion of [User Interaction](user-interaction.md)
- Understanding of variables in playbooks

## Why Call Playbooks?

>:bulb: Each playbook is equivalent to a function.

Calling playbooks allows you to:

- Break complex processes into smaller, reusable components
- Create libraries of common functionality
- Improve readability and maintainability
- Enable more complex logic through composition

## Defining Playbooks

### With Explicit Parameters

To create a reusable playbook, you can define it with parameters:

```markdown
## Greeting($name)
Greet the user by welcoming them to the service
### Steps
- Say "Hello, $name! Welcome to our service."
```

### With Implicit Parameters

>:bulb: A playbook has access to all state variables.

```markdown
## Greeting
Greet the user by welcoming them to the service
### Steps
- Say "Hello, $name! Welcome to our service."
```

This playbook does not specify a parameter. It can still use the `$name` variable if it is set previously, say from the calling playbook.

## Calling a Playbook

### Like a Python Function

You can call a playbook from another playbook like a python function call:

```markdown
## Main
### Triggers
- At the beginning
### Steps
- Ask the user for their $user_name and $city
- Greeting($user_name, city=$city, age=50, state="WA")
- End program
```

>:bulb: It is OK to deviate from standard Python syntax.

For example, the following is also valid Playbooks code:

```markdown
- Greeting($user_name, city=$city, age=50, state=two letter state code where Seattle is located)
```

The Playbooks runtime will automatically convert `state=two letter state code where Seattle is located` to `state="WA"`!

### Implicitly

You can also call a playbook implicitly:

```markdown
## Main
### Triggers
- At the beginning
### Steps
- Ask the user for their $name
- Greet the user using their $name
- End program
```

>:bulb: Playbooks runtime can infer which playbook to call based on the description of the playbook and current context.

Note that Playbooks runtime will interpret "Greet the user" as a call to the `Greeting` playbook based on the description of the playbook `Greet the user by welcoming them to the service`. It will also automatically pass the `$name` variable to the `Greeting` playbook based on the signature of the playbook.

## Capturing Return Values 

### With a Python-like Syntax

Playbooks can return values that can be captured and used by the calling playbook:

```markdown
## CalculateTotal($price, $quantity)
Calculates the total bill amount from the price and quantity

### Steps
- $total = $price * $quantity
- Return $total

## OrderProcess
### Triggers
- At the beginning
### Steps
- Ask the user for the item $price
- Ask the user for the $quantity
- $bill_amount = CalculateTotal($price, $quantity)
- Tell user that their total bill is $bill_amount
- End program
```

### Implicitly

If you don't need the returned value beyond a yield point, do not capture it explicitly. For example,

```markdown
- Get total bill amount from CalculateTotal($price, $quantity)
- Tell user what their total bill is
```

## Fully Semantic Calls

Combined with semantic playbook calls with implicit parameters and return values, this can also be expressed as:

```markdown
- Calculate total bill amount
- Tell user what their total bill is
```

>:bulb: This is the preferred way to author playbooks, because it is more readable and easier to maintain.

## A Practical Example: Country Facts

Let's create a more complex example that demonstrates both parameters and return values:

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

In this example:

- `GetCountryFact` takes a country name and returns a fact about it
- `Main` calls `GetCountryFact` for each country in a list
- The return value is stored and used in the response


## Exercises

1. Create a program with playbooks that process a shopping cart (add items, calculate total, apply discounts)
2. Create a playbook to implement tic-tac-toe

## Next Steps

Now that you know how to call playbooks from markdown, it's time to learn about [Python Playbooks](python-playbooks.md) for more advanced functionality. 