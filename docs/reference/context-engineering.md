# Context Engineering

Playbooks automates context engineering, allowing you to focus on writing agent logic while the framework intelligently manages LLM context. This automated approach ensures efficient token usage and optimal performance without manual intervention.

## Key Innovations

- [Stack-based Context Management](./context-engineering.md#stack-based-context-management)
Automatically compacts context as playbooks complete, preserving semantic information while reducing token usage.

- [State Compression](./context-engineering.md#state-compression)
Uses I-frame/P-frame technique (similar to video compression) to efficiently represent state changes across LLM calls.

- [Artifacts](../programming-guide/artifacts.md)
Automatic, efficient use of long content in LLM context.

- [Prompt Caching Optimization](./context-engineering.md#prompt-caching-optimization)
Intelligently manages context to maximize cache hits, reducing latency and API costs by up to 10x.

- [Programmer Control](./context-engineering.md#programmer-control-over-context)
Programmers have control through specific control mechanisms.

---

## Stack-based Context Management

Playbooks uses a stack-based approach to manage LLM context dynamically. As playbooks execute and return, their detailed execution traces are automatically replaced with concise summaries, keeping context focused and efficient.

### How It Works

Consider this call stack in a running Playbooks program:

```
Main
  └─ GetOrderStatus
      └─ SummarizeOrderStatus
```

**During Execution:**
- When `SummarizeOrderStatus` is active, the context includes the full execution trace from `Main` → `GetOrderStatus` → `SummarizeOrderStatus`
- Long content is automatically stored as artifact so the value is not duplicated in the context multiple times.
- All playbook instructions, inputs, outputs, artifacts, and intermediate steps are preserved in context

**After Playbook Returns:**
- When `SummarizeOrderStatus` completes, its detailed execution trace is replaced with a summary. Any artifacts created/loaded in `SummarizeOrderStatus` are unloaded from context.
- When `GetOrderStatus` returns to `Main`, both its traces are replaced with summary
- So, when `Main` playbook continues after `GetOrderStatus` returns, it has a compact context containing only the summary of `GetOrderStatus` execution, thus reducing context size and token usage

**👉 [Complete Artifacts Guide](../programming-guide/artifacts.md)** - Detailed explanation, API reference, and usage patterns

---

## State Compression

MPEG video compression uses I-frames (full images) and P-frames (only the pixels that changed since the last frame) to reduce video file size. Playbooks uses a similar technique to efficiently represent state changes across LLM calls. Instead of sending the full state on every call, the framework sends incremental changes, significantly reducing token usage when state is large.

### How It Works

**I-frames (Full State):**
The first LLM call includes the complete state representation:

```json
{
    "variables": {},
    "agents": [
    "Host(agent 1000)",
    "HumanAgent(User, User, human)"
    ]
}
```

**P-frames (Predicted/Delta):**
Subsequent calls only include what changed. If nothing changed, the state representation is empty:

```
empty
```

If two new agents were created:

```json
{
    "new_agents": [
    "Player(agent 1001, name:MysticMind)",
    "Player(agent 1002, name:SharpGuesser)"
    ]
}
```

If an agent was terminated and a variable was set:

```json
{
    "new_variables": {
        "latest_move": "Place X at position 5"
    },
    "deleted_agents": [
        "Player(agent 1002, name:SharpGuesser)"
    ]
}
```

**Periodic I-frames:**
After `state_compression.full_state_interval` P-frames (configured in `playbooks.toml`), the framework sends a new I-frame with full state:

```json

{
    "variables": {
        "latest_move": "Place O at position 2"
    },
    "agents": [
        "Host(agent 1000)",
        "HumanAgent(User, User, human)"
    ]
}
```

### When This Helps

State compression saves significant tokens when:

- There are many variables
- Variables have large values (e.g., lists, complex objects)
- Multiple agents exist but change infrequently
- State is mostly stable between calls

---

## Prompt Caching Optimization

Playbooks intelligently leverages prompt caching to minimize latency and reduce API costs. The framework automatically manages cache-friendly context structures.

### How Prompt Caching Works

**Prefix Caching:**

1. LLM providers cache the activations of prompt prefixes. Some LLM providers cache prefixes at specified locations in the context. Some LLM providers charge extra for adding cache entries.
2. When a new request arrives, the longest matching cached prefix is identified
3. Cached activations are restored, avoiding reprocessing
4. Only tokens beyond the prefix are processed

**Performance Impact:**

- Cached tokens: ~10x cheaper and faster than regular tokens
- Cache hit on a 5,000 token prefix saves seconds of latency and significant cost

### Playbooks Cache Strategy

The framework automatically:

1. **Sets Strategic Cache Points**
Places cache boundaries at stable context segments and prioritizes frequently reused prefixes (system prompts, playbook definitions, call points). Claude allows a maximum of 4 cache points in the context, which the framework selects intelligently.

2. **Balances Cache Efficiency**
There are competing factors to balance when it comes to using the cache effectively, while compacting the context to reduce token usage.

    - The oldest part of the context is the best candidate to be compacted because those details may not be relevant to the current execution. But compacting the oldest part invalidates the prefix cache completely.

    - Compacting the newest part of the context allows for long cache prefix hits, but it may not be the best candidate to be compacted because those details may be relevant to the current execution.

    - As a result, Playbooks framework compacts the middle part of the context, which balances between preserving cache prefix and preserving context for the current execution.

    - Note that as the program proceeds and call stack unwinds, what was the middle part of the context may become the current execution part and thus what was previously compacted away may need to be added back at full detail. This is handled automatically by the framework by preserving the full uncompacted context and progressively adjusting the context on every LLM call.

---

## Programmer Control Over Context

While Playbooks automates context management, you retain full control when needed for specialized scenarios.

### Control Mechanisms

**[Raw Prompt Playbooks](./playbook-types.md#raw-prompt-playbooks)**
- Write literal prompt text that bypasses automatic context management
- Useful for expert and narrow prompt engineering scenarios

**[Description Placeholders](./description-placeholders.md)**
- Inject dynamic values into playbook descriptions
- Inject either inline in the description or as a separate LLM message.

**[Artifacts](../programming-guide/artifacts.md)**
- Control when large content enters/exits context through explicit artifact creation with `SaveArtifact()` and loading with `LoadArtifact()`
- Influence automatic artifact creation threshold via `artifact_result_threshold` configuration
