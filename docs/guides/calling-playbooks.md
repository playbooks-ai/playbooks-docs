---
title: Call Playbooks
---

# Call Playbooks

Goal: Call a playbook with arguments and capture return values.

## Explicit call

```markdown
## Greeting($name)
### Steps
- Say "Hello, $name!"

## Main
### Triggers
- At the beginning
### Steps
- Ask for $name
- Greeting($name)
```

## Return values

```markdown
## Total($price, $qty)
### Steps
- Return $price * $qty

## Main
### Steps
- $bill = Total($p, $q)
- Tell user bill is $bill
```

## Semantic call

````markdown
## Main
### Steps
- Calculate total bill amount ← This will call the CalculateTotal playbook
- Tell user the bill amount

```python
@playbook
def CalculateTotal(price, qty):
    return price * qty
```
````

Tips:

- Prefer semantic calls for readability
- Use parameters for clarity when needed

