---
title: User Interaction
---

# User Interaction

Goal: Ask for input, validate it, and respond.

## Basic flow

```markdown
## Greet
### Triggers
- At the beginning
### Steps
- Ask the user for their $name
- Say hello to $name
```

## Validation loop

```markdown
## Main
### Triggers
- At the beginning
### Steps
- Ask for a 4-digit $pin
- While $pin is not a 4-digit number
  - Tell user PIN is invalid
  - Ask again for $pin
- Tell user PIN is accepted
```

## Single line validation loop

```markdown
## Main
### Triggers
- At the beginning
### Steps
- Ask user for a 4-digit $pin, engage in a professional conversation till user provides pin or gives up
```

## Automatic validation

```markdown
## Main
### Triggers
- At the beginning
### Steps
- Ask user for a 4-digit $pin, engage in a professional conversation till user provides a valid pin or gives up

## ValidatePin

### Triggers
- When user provides a new pin

### Steps
- If pin is not a 4-digit number
  - Return "PIN should be 4 digits"
- sum up the digits of the pin
- If sum is greater than 10
  - Return "This is not a valid PIN"
- Return "PIN is valid"
```

Tips:

- Use variables to store responses
- Keep prompts short and specific

## See also

- [Tutorials Part 1](../tutorials/part-1-user-interaction.md)
- [Markdown Playbooks](../playbook-types/markdown-playbooks.md)
- [Built-in Playbooks](../playbook-types/builtin-playbooks.md)
- [Variables & Expressions](variables-and-expressions.md)

