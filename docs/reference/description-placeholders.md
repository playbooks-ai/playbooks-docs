# Description Placeholders

Description placeholders allow you to inject dynamic content into playbook descriptions using Python expressions. This enables runtime customization of the context sent to the LLM without modifying the playbook definition.

## Overview

Placeholders use the `{expression}` syntax within playbook descriptions. At runtime, these expressions are evaluated and replaced with their values before the description is sent to the LLM.

**Key characteristics:**

- Evaluated once when the playbook begins execution
- Support variables, playbook calls, and Python expressions
- Available in all LLM-executed [playbook types](./playbook-types.md) (Markdown, ReAct, Raw Prompt)
- Resolved before LLM sees the description

---

## Basic Syntax

Use curly braces `{}` to embed expressions in descriptions:

```markdown
## ProcessOrder
This playbook processes order {$order_id} for customer {$customer_name}
```

When executed, placeholders are resolved to actual values:

```
This playbook processes order 12345 for customer John Smith
```

---

## What You Can Use in Placeholders

- All state variables
- All playbooks and functions
- Standard Python built-ins
- Special variables listed below
- All imported modules from all ` ```python ` blocks in the agent


### 1. Variables

Reference any variable from the current execution state:

```markdown title="Variable placeholder example"
## ReviewTransaction
Review transaction {$transaction_id} with amount ${$amount}

### Steps
- Verify the transaction details
- Process the review
```

**Variable syntax:**

- `{$variable_name}` - Recommended, explicit
- `{variable_name}` - Also works, `$` prefix is optional

### 2. Playbook Calls

Call other playbooks to generate dynamic content:

```markdown title="Calling other playbooks example"
## AnswerQuestions
This playbook answers questions about quarterly summaries.

Q1 Summary: {QuarterlySummary("Q1")}
Q2 Summary: {QuarterlySummary("Q2")}
Q3 Summary: {QuarterlySummary("Q3")}
Q4 Summary: {QuarterlySummary("Q4")}

### Steps
- Answer user questions based on the summaries above
```

**Key points:**

- Playbook calls are awaited automatically, no need to use `await` keyword
- Return values are converted to strings
- Can pass arguments like regular function calls

**When the playbook executes:**

1. Each `QuarterlySummary(quarter)` call executes
2. Results replace the placeholders
3. LLM sees the full context with all quarterly data

### 3. Python Expressions

Use any valid Python expression:

```markdown title="Python expression example"
## AnalyzePerformance
Performance score: {round($score * 100, 2)}%
Status: {"Excellent" if $score > 0.9 else "Good" if $score > 0.8 else "Needs Improvement"}
Items to process: {len([x for x in $items if x.active])}
Timestamp: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}

### Steps
- Analyze the performance data
- Generate recommendations
```

### 4. Special Variables

Access agent information and execution context:

```markdown
## DebugInfo
Current agent: {agent.klass}
Executing playbook: {call.playbook_name}
Agent state: {agent.state.variables}
Current time: {timestamp}
```

**Available special variables:**

- `agent` - The agent instance

    - `agent.klass` - Agent class name
    - `agent.state` - Current execution state
    - `agent.namespace_manager.namespace` - Available functions

- `call` - Current playbook call

    - `call.playbook_name` - Name of the playbook
    - `call.args` - Positional arguments
    - `call.kwargs` - Keyword arguments

- `timestamp` - Current datetime object

---

### Security

The expression evaluator implements security safeguards:

**Blocked operations:**

- `subprocess`, `eval`, `exec`
- `__import__`, `open`
- Access to `__globals__`, `__locals__`

### Error Handling

If an expression fails to evaluate, the error will be returned as the expression value and inserted into the description.


### Single Evaluation

:warning: Placeholders are resolved **once** when the playbook begins execution and are **not re-evaluated** during playbook execution.
