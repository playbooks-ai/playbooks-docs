# Built-in Playbooks

Playbooks framework comes with a set of built-in playbooks that are available to every agent without requiring explicit import or definition. These playbooks handle common operations like communication, artifact management, and program control flow.

## Overview

Built-in playbooks fall into two categories:

1. **Callable Playbooks** - Available for use in your playbooks (e.g., `Say`, `SendMessage`, `SaveArtifact`)
2. **Hidden/Internal Playbooks** - Used internally by the system (marked with `hidden=True`) that should not be used in Playbooks

## Available Built-in Playbooks

### `Say(target: str, message: str)`

Sends a message to a specified target (agent or user).

**Example usage:**
```markdown
### Steps
- Welcome the user
- Ask user for account number
- Ask Account Management Agent to handle customer's account inquiry
```

### `SendMessage(target_agent_id: str, message: str)`

**(Hidden/Internal Playbook)**
Internal implementation of `Say`

### `WaitForMessage(source_agent_id: str) -> str | None`

**(Hidden/Internal Playbook)**

Waits for a message from a specific agent or user. This is a low-level communication primitive typically used internally for agent-to-agent coordination.

For example, when executing a step like `"Ask user for account number"`, the playbook will send a message to the user using `SendMessage("human", "What is your account number?")` and wait for the user's response using `WaitForMessage("human")`.


### `SaveArtifact(artifact_name: str, artifact_summary: str, artifact_content: str)`

Saves data as a named artifact for later retrieval.

**Example:**
```markdown
### Steps
- Generate a detailed analysis report
- SaveArtifact("quarterly_report.md", "Q3 2023 Sales Analysis", generated report)
- Tell the user the report has been saved as Artifact["quarterly_report.md"]
```

### `LoadArtifact(artifact_name: str)`

Artifacts are **not** included in the LLM context by default because they can be large. When you need to operate on the contents of an artifact, load the artifact first. This will yield execution back to the runtime, which will include the artifact in the LLM context and resume playbook execution.

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

### `CreateAgent(agent_klass: str, **kwargs)`

Creates and starts a new agent dynamically during runtime.

**Example:**
```markdown
### Steps
- Create a new SupportAgent with approprate name
- Ask the support agent to handle customer inquiry
- Wait for the agent's response
```

### `InviteToMeeting(meeting_id: str, attendees: list)`

Invites additional agents to an existing meeting for multi-agent collaboration.

**Example:**
```markdown
### Steps
- Start a meeting with Accountant and CFO
- Invite Data analyst and Project manager to the meeting
```

### `Loadfile(file_path: str, inline: bool = False, silent: bool = False)`

Loads content from a file in the filesystem. This is used in description placeholders to load reference materials to execute the playbook.

**Example:**
```markdown
## Generate a summary($document)
This playbook generates summary of the given document.
Use the following format: {Loadfile("summary-format.txt")}
```