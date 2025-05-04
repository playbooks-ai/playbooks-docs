# Built-in Playbooks

Playbooks AI provides a set of built-in playbooks that are available to every agent without requiring explicit import or definition. These playbooks handle common operations like communication, artifact management, and program control flow.

## Available Built-in Playbooks

### `SendMessage(target_agent_id: str, message: str)`

Sends a message to another agent or the user.

```python
@playbook
async def SendMessage(target_agent_id: str, message: str):
    """
    Send a message to another agent.
    
    Args:
        target_agent_id (str): The ID of the agent to send the message to.
                               Use "human" to send a message to the user.
        message (str): The content of the message.
    
    Returns:
        None
    """
    ...
```

**Example usage:**
```markdown
### Steps
- Send message to SupportAgent "Please assist with this customer inquiry"
- Tell the user their request has been forwarded to a specialist
```

### `Say(message: str)`

A convenience playbook that sends a message to the human user.

```python
@playbook
async def Say(message: str):
    """
    Send a message to the human user.
    
    This is a convenience wrapper around SendMessage("human", message).
    
    Args:
        message (str): The message to send to the user.
    
    Returns:
        None
    """
    await SendMessage("human", message)
```

**Example usage:**
```markdown
### Steps
- Say hello to the user
- Say("Here's your ticket link: https://support.playbooks.ai/tickets/{$ticket_id}")
```

### `WaitForMessage(source_agent_id: str) -> str | None`

Waits for a message from a specific agent or user.

```python
@playbook
async def WaitForMessage(source_agent_id: str) -> str | None:
    """
    Wait for a message from a specific agent.
    
    Args:
        source_agent_id (str): The ID of the agent to wait for a message from.
                               Use "human" to wait for a user message.
    
    Returns:
        str or None: The content of the received message, or None if the wait timed out.
    """
    ...
```

**Example:**
```markdown
### Steps
- SendMessage("SupportAgent", "What is the return policy for Canada?")
- $return_policy = WaitForMessage("SupportAgent")
- ...
```

### `SaveArtifact(artifact_name: str, artifact_summary: str, artifact_content: str)`

Saves data as a named artifact for later retrieval.

```python
@playbook
async def SaveArtifact(artifact_name: str, artifact_summary: str, artifact_content: str):
    """
    Save data as a named artifact.
    
    Args:
        artifact_name (str): The name to give the artifact, typically with an extension
                             (e.g., "report.md", "data.json").
        artifact_summary (str): A brief description of the artifact.
        artifact_content (str): The actual content to store in the artifact.
    
    Returns:
        None
    """
    ...
```

**Example:**
```markdown
### Steps
- Generate a detailed analysis report
- SaveArtifact("quarterly_report.md", "Q3 2023 Sales Analysis", generated report)
- Tell the user the report has been saved at Artifact["quarterly_report.md"]
```

### `LoadArtifact(artifact_name: str)`

Loads a previously saved artifact by name.

```python
@playbook
async def LoadArtifact(artifact_name: str):
    """
    Load a previously saved artifact by name.
    
    Args:
        artifact_name (str): The name of the artifact to load.
    
    Returns:
        Artifact: An object with properties:
            - name: The artifact's name
            - description: The artifact's summary
            - content: The artifact's content
    
    Raises:
        KeyError: If the artifact doesn't exist
    """
    ...
```

**Example:**
```markdown
### Steps
- LoadArtifact("Q1_report.md")
- LoadArtifact("Q2_report.md")
- LoadArtifact("Q3_report.md")
- LoadArtifact("Q4_report.md")
- Analyze the content of the quarterly reports and generate annual report
- SaveArtifact("annual_report.md", "Annual Report", generated annual report)
```

### `Return(value=None)`

Returns a value from the current playbook and ends its execution.

```python
@playbook
async def Return(value=None):
    """
    Return a value from the current playbook and end execution.
    
    Args:
        value: The value to return (optional).
    
    Returns:
        The provided value, or None if no value was provided.
    """
    ...
```

**Example:**
```markdown
## GetDiscount($membership_level)
### Steps
- If $membership_level is "premium"
  - Return(0.15)  # 15% discount
- If $membership_level is "standard"
  - Return(0.05)  # 5% discount
- Return(0)  # No discount
```

## Related Topics

- [Markdown Playbooks](markdown-playbooks.md) - Using built-in playbooks in markdown
- [Python Playbooks](python-playbooks.md) - Using built-in playbooks in Python
- [Working with Artifacts](../tutorials/working-with-artifacts.md) - More on artifacts
- [Multi-Agent Systems](../multi-agent-systems/index.md) - Communication between agents
