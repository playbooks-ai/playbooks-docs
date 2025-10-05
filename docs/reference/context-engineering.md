# Context Engineering

Playbooks automates context engineering, allowing you to focus on writing agent logic while the framework intelligently manages LLM context. This automated approach ensures efficient token usage and optimal performance without manual intervention.

## Key Innovations

- [Stack-based Context Management](./context-engineering.md#stack-based-context-management)
Automatically compacts context as playbooks complete, preserving semantic information while reducing token usage.

- [Prompt Caching Optimization](./context-engineering.md#prompt-caching-optimization)
Intelligently manages context to maximize cache hits, reducing latency and API costs by up to 10x.

- [Programmer Control](./context-engineering.md#programmer-control-over-context)
Programmers have control over through specific control mechanisms.
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
- All playbook instructions, inputs, outputs, and intermediate steps are preserved in context

**After Playbook Returns:**
- When `SummarizeOrderStatus` completes, its detailed execution trace is replaced with a summary
- When `GetOrderStatus` returns to `Main`, both its traces are replaced with summary
- So, when `Main` playbook continues after `GetOrderStatus` returns, it has a compact context containing only the summary of `GetOrderStatus` execution, thus reducing context size and token usage

---

## Prompt Caching Optimization

Playbooks intelligently leverages prompt caching to minimize latency and reduce API costs. The framework automatically manages cache-friendly context structures.

### How Prompt Caching Works

**Prefix Caching:**

1. LLM providers cache the activations of prompt prefixes. Some LLM providers cache prefixes at specified locations in the context. some LLM providers charge extra for adding cache entries.
2. When a new request arrives, the longest matching cached prefix is identified
3. Cached activations are restored, avoiding reprocessing
4. Only tokens beyond the prefix are processed

**Performance Impact:**

- Cached tokens: ~10x cheaper and faster than regular tokens
- Cache hit on a 5,000 token prefix saves seconds of latency and significant cost

### Playbooks Cache Strategy

The framework automatically:

1. **Sets Strategic Cache Points**
Places cache boundaries at stable context segments and prioritizes frequently reused prefixes (system prompts, playbook definitions, call points). Claude allows a maximum of 4 cache points in the context, which the frameworks selects intelligently.

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
- Inject either inline in the description or as a separarate LLM message.
