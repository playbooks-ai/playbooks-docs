---
title: Adding Triggers
---

# Adding Triggers

Goal: Run a playbook when a condition is met.

## Common triggers

- At the beginning
- When $variable meets a condition (e.g., `When $x > 10`)
- Before/After calling another playbook
- When user provides specific input

## Example

```markdown
## Main
### Triggers
- At the beginning
### Steps
- $x = 10
- LoadAccount
- $x = $x * 2
- Tell user balance

## TooBig
### Triggers
- When $x > 15
### Steps
- Tell user $x is too big

## AfterLoad
### Triggers
- After calling LoadAccount
### Steps
- Tell user account loaded
```

Tips:

- Write clear conditions
- Avoid mutually triggering playbooks
- Prefer triggers for validation over inline checks

## See also

- [Triggers](../triggers/index.md)

