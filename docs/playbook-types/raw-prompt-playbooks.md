---
title: Raw Prompt Playbooks
---

# Raw Prompt Playbooks

Use a raw prompt when you need full control over the prompt sent to the LLM. This playbook type bypasses compiler enrichment and sends playbook description verbatim after any placeholder substitutions.

To make a raw prompt playbook, add `execution_mode: raw` to the playbook description and do not include any steps.

## Example

```markdown
## GetTicketCategory ← This is a raw prompt playbook
execution_mode: raw

Here is customer message in a support ticket: {$ticket_message}
You will categorize this ticket in one of the following categories:
- Technical Support
- Billing
- Account Management
- Other

Respond with just the category of the ticket and nothing else.
The ticket category is:


## EnrichTicketInfo($ticket) ← This is a regular markdown playbook

### Steps
- $ticket.category = GetTicketCategory($ticket.message)
- SaveTicket($ticket)
```

When to use:

- Specific single shot tasks
- When you want full control over what is sent to the LLM

Considerations:

- You lose some safety checks and verification of how the prompt is executed
- Prefer standard markdown playbooks for control and observability

## Execution context

Raw playbooks do not add any execution context to LLM calls. The runtime sends exactly your description (prompt) as-is, with no automatic conversation summaries, state, or helper context.

- If your prompt needs variables, prior state, or computed values, include them explicitly using description placeholders.

>:warning: Raw playbooks make a single LLM call with no loop or planning. Ensure your description, i.e. prompt, contains all necessary instructions and context.

## See also

- [ReAct Playbooks](react-playbooks.md) for the context-enriched think–act loop execution flow
- [Automating Context Engineering](../advanced/automating-context-engineering.md)

## Description placeholders

Use `{expression}` placeholders in the playbook description to inject execution context.

See [Markdown Playbooks - Description placeholders](markdown-playbooks.md#description-placeholders) for full details on placeholder syntax and capabilities.


