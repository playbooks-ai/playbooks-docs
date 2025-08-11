---
title: Variables & Expressions
---

# Variables & Expressions

Goal: Use variables safely and write expressions that evaluate reliably.

## Variables

- Use `$name` to reference a variable in steps
- Assign with `- $x = ...`
- Return with `- Return $x`

## Expressions

- You can write simple Python‑like expressions in assignments and conditions

Examples:

```
- Ask user their $age
- If $age is less than 25
  - Tell user about below 25 insurance requirements
```

## Description placeholders

You can use expressions in playbook descriptions with `{expression}` syntax:

```markdown
## ProcessOrder
Processing order {$order_id} for customer {$customer_name}
```

These placeholders are resolved at runtime when the playbook executes. See [Markdown Playbooks - Description placeholders](../playbook-types/markdown-playbooks.md#description-placeholders) for details.

See also: [Playbooks Language](../playbooks-language/playbooks-language.md) and [Metadata](../playbooks-language/metadata.md).

