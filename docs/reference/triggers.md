# Triggers

Triggers are a powerful feature in Playbooks AI that enable declarative event-driven programming through natural language conditions. They allow playbooks to be dynamically invoked when specified conditions are met.

## What are Triggers?

Triggers are conditions written in natural language that, when met, cause a playbook to be executed. They enable reactive and event-driven behavior in your AI agents.

## Types of Triggers

Triggers can be classified into three types:

- Temporal triggers ("when program starts")
- State-based triggers ("when $x becomes more than 15")
- Execution flow hooks ("after calling LoadAccount")
- User interaction triggers ("when user provides a PIN")
- Sentiment based triggers ("if the user is extremely frustrated")
- User requested triggers ("when user wants to connect with human agent")
- External event triggers ("when a new email is received")
- Communication based triggers ("when another agent asks you about tax rates")


## How to Add Triggers

Triggers are added to the `### Triggers` section of a playbook.

```markdown
### Triggers
- At the beginning
```

Triggers can also be added to Python playbooks.

````markdown
```python
@playbook(triggers=["At the beginning"])
async def MyPlaybook():
    pass
```
````