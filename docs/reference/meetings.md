# Meetings

Meetings enable multi-agent coordination through structured group conversations. They provide a shared communication channel where multiple agents can collaborate, share information, and reach consensus.

## Overview

Meetings are first-class abstractions in Playbooks for multi-party coordination. Unlike one-to-one messaging or direct public playbook calls, meetings allow multiple agents to participate in an ongoing conversation with shared context.

**Key capabilities:**

- **Multi-party coordination** - Host and multiple attendees collaborate in real-time
- **Shared communication channel** - All messages visible to all participants
- **Shared state** - Participants can read and write to a shared data structure
- **Required attendees** - Ensure critical stakeholders are present before proceeding
- **Meeting lifecycle** - Clear start, active phase, and end phases

## When to Use Meetings

✅ **Use meetings when:**

- Multiple agents need to collaborate on a shared task
- Back-and-forth discussion is needed between participants
- Agents need to build consensus or make joint decisions
- Shared context must be maintained across all participants
- Complex coordination with 3+ agents

❌ **Don't use meetings when:**

- Simple request-response between two agents (use [public playbooks](./exported-and-public-playbooks.md))
- Fire-and-forget communication (use messaging)
- Agents don't need to see each other's messages
- Linear, sequential delegation is sufficient

## Creating a Meeting

### Basic Structure

Each participating agent defines a meeting playbook with `meeting: true` metadata:

```markdown
# HostAgent
## PlanningSession
meeting: true

### Steps
- ...

# ParticipantAgent
## PlanningSession
meeting: true

### Steps
- ...
```

### Starting a Meeting

The host agent starts a meeting using natural language:

```markdown
### Steps
- Start a planning session with TeamLead and Engineer
- ...
```

The framework automatically:
1. Creates instances of TeamLead and Engineer agents
2. Creates the meeting
3. Invites specified attendees
4. Waits for them to join
5. Sets up shared state and a shared communication channel for the meeting
6. Routes messages between participants


## Required vs Optional Attendees

### Required and Optional Attendees

Specify critical participants who must be present before the meeting begins and optional participants who are invited but not required for the meeting to proceed:

```markdown
## Main

### Steps
 - Start a strategy meeting

## StrategyMeeting
meeting: true
required_attendees: [CFO, CTO]
optional_attendees: [VP_Sales]

### Steps
- ...
```

## Meeting Lifecycle

### 1. Creation

The host agent initiates the meeting:

```markdown
- Start a code review meeting with SeniorDev and TechLead
```

### 2. Invitation

The framework sends invitations to all specified attendees. Participants receive the invitation and accept by starting their appropriate meeting playbook.

### 3. Active Phase

During the meeting, each participant follows instructions in their meeting playbook. Typically meeting playbooks have a `while meeting is in progress` loop with steps to:

- Send meeting messages visible to all attendees
- Read meeting messages from other participants
- Access and modify shared state
- Think and coordinate on shared goals
- Wait for either specific participants or anyone from the meeting to say something

### 4. Termination

The meeting **ends when the host agent returns from its meeting playbook**. When the meeting ends, all participants receive an end-of-meeting signal.

## Shared State

Meeting participants can share variables through a shared state object accessible to all attendees.

### Accessing Shared State

From markdown playbooks:

```markdown
- Set current player to Player1 in meeting shared state
- Look at game board from the meeting shared state and consider my move
- ...
```

From Python playbooks:

```python
@playbook
async def RunAlgorithm():
    if meeting.shared_state.game_board[0] == "X":
        meeting.shared_state.game_board[1] = "O"
        meeting.shared_state.strategy = "defensive"
```

Note that `meeting.shared_state` is a `Box` object that allows both `["attr"]` or `.attr` access.

## Related Documentation

- [Agents](./agents.md) - Creating and managing agents that participate in meetings
- [Built-in Playbooks](./builtin-playbooks.md) - Meeting-related playbooks like `InviteToMeeting()`
- [Triggers](./triggers.md) - Using triggers to respond to meeting invitations
- [Programming Guide: Multi-Agent Programs](../programming-guide/index.md#multi-agent-programs) - High-level overview and patterns

