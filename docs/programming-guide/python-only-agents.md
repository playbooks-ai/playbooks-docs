# Python-Only Agents

This document explains how to write agents that use pure Python logic without making any LLM calls, enabling deterministic, fast, and cost-free execution for workflows that don't require AI reasoning.

This is mainly a demonstration of how Playbooks can be used to build fully-deterministic workflows. It is not a recommended approach for production systems (why use Playbooks at all in that case?), but may be handy for prototyping and testing.

You can write a Python-only agent by writing all its playbooks using Python code.

````markdown
### Example Python-Only Agent

```python
@playbook(triggers=["At the beginning"])
async def Main():
    Say("user", "What's your name?")
    messages = WaitForMessage("user")
    Say("user", f"Received messages: {messages}")
    Say("user", f"Secret code: {await GetSecret()}")
    Exit()

@playbook
async def GetSecret():
    return "OhSoSecret!"
```
````

When this agent starts, the `Main` playbook is triggered that executes an interactive workflow with the user and calls another Python playbook.

