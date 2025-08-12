---
title: Common Language Runtime (CLR)
---

# Common Language Runtime (CLR)

Playbooks provides a Common Language Runtime for executing programs authored under the CLS. The CLR treats LLMs as an execution unit within a fetch–decode–execute loop, verifying each step against the compiled program.

## Responsibilities

- Load compiled PBASM and program metadata
- Manage agents, call stack, variables, artifacts, and events
- Coordinate LLM-driven step execution and Python function execution on the same stack
- Verify that LLM outputs conform to the program contract
- Provide observability (session logs, event bus, debug server)

## Execution loop

High-level phases:

1. Decide next playbook to execute (queued calls, triggers, or start-of-program)
2. Execute next fragment:
   - For Markdown Playbooks: request LLM to produce structured control actions
   - For Python Playbooks: invoke Python function in-process
3. Parse, verify, and apply actions: variable updates, Say, calls, returns, triggers
4. Yield: to user, to call, or to exit

## Verification contract

The CLR expects LLM responses in a structured format (recap, plan, Var[], Step[], trig?, yld). Responses are parsed and verified to ensure:

- Steps map to valid program locations with correct line numbers and codes
- Variable updates are explicit and typed
- [Triggers](../triggers/index.md) are evaluated between steps and on relevant updates
- Control transfers occur only via valid yields (user, call, exit)

If verification fails, the CLR treats it as unexpected control flow and can recover or surface errors.

## Multi‑agent and messaging

- Agents can send messages, wait for messages, and call public playbooks of other agents
- Meetings enable broadcast-style coordination
- CLR routes messages and enforces boundaries for agent-to-agent calls

## Observability and debugging

- Session logs with rich, structured entries
- Event bus for real‑time visibility
- Optional debug server for step debugging and IDE integration

See also:

- [Playbooks Runtime](index.md)
- [Playbooks Assembly Language](../playbooks-language/playbooks-assembly-language.md)


