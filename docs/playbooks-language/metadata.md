# Metadata

Metadata in Playbooks AI allows you to attach structured information to agents and playbooks. This metadata can be used for documentation, configuration, tooling integration, and agent discovery.

## Overview

Metadata can be specified on:

- **Agents** - Information about the agent itself
- **Playbooks** - Information about individual playbooks

The metadata system is designed to be flexible and extensible, allowing you to add custom fields that make sense for your use case.

### Agent Metadata

Agent metadata is specified immediately after the agent heading:

```markdown
# Accountant
framework: GAAP
specialization:
  - accounting
  - tax
author: John Doe
This is an accountant agent that can help with accounting tasks.
```

## Metadata for Markdown Playbooks

In [markdown playbooks](../playbook-types/markdown-playbooks.md), metadata is specified directly in the description area of agents and playbooks using YAML-like syntax. Example:

```markdown
## PrepareTaxReturn
priority: high
category: tax-preparation
estimated_time: 30 minutes
This playbook prepares and submits tax returns following proper procedures.
```

## Metadata for Python Playbooks

For Python playbooks, metadata is specified directly on the `@playbook` decorator. All keyword arguments except `triggers` are treated as metadata. Example:

```python
@playbook(
    public=True, 
    export=True, 
    author="Amol Kelkar",
    category="financial",
    version="1.0"
)
async def CalculateROI(investment: float, returns: float) -> float:
    """Calculate return on investment."""
    return (returns - investment) / investment * 100
```

### Known Metadata Fields

Although any fields can be added as metadata, here are the fields that are processed by Playbooks.

- `public`: Whether the playbook is public
- `export`: Whether the playbook's implementation can be exported
- `remote`: Remote service configuration
  - `type`: mcp, playbooks, etc.
  - `url`: Remote service URL
  - `transport`: transport protocol to use for the remote service

Example:
```yaml
public: true
export: true
remote:
  type: mcp
  transport: streamable-http
  url: http://localhost:8088/mcp
```

## Compilation Behavior

When Playbooks Language (`.pb`) files are compiled to Playbooks Assembly Language (`.pbasm`), the compiler intelligently processes metadata:

### Metadata Extraction and Organization

The compiler gathers various metadata items specified in the description area and consolidates them under a `metadata:` section:

**Before compilation (example.pb):**
```markdown
# Accountant
public: true
export: true
This is an accountant agent that can help with accounting tasks.
author: John Doe
```

**After compilation (example.pbasm):**
```markdown
# Accountant
metadata:
  public: true
  export: true
  author: John Doe
---
This is an accountant agent that can help with accounting tasks.
```

## Related Topics

- [Playbooks Language](playbooks-language.md) - Overall language structure
- [Python Playbooks](../playbook-types/python-playbooks.md) - Python-specific features
- [Playbooks Assembly Language](playbooks-assembly-language.md) - Compilation target
- [Multi-Agent Systems](../agents/index.md) - Using metadata for agent coordination 