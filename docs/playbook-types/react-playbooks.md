# ReAct Playbooks

Let the LLM reason and plan the next action in a think–act loop when steps are not known in advance.

## Overview

ReAct playbooks are ideal for:

- Complex problem-solving tasks
- Deep research and information gathering tasks
- Dynamic planning
- Tasks where the exact steps aren't known in advance

## Structure

A ReAct playbook is defined as a standard markdown playbook, but without the `### Steps` section:

```markdown
## PlaybookName
Detailed description or prompt for the task, goals, and constraints. Do not use markdown in the prompt.

### Triggers
- Trigger condition 1
- Trigger condition 2
```

The key difference is that ReAct playbooks **do not** include a `### Steps` section. Instead, the system provides a default ReAct execution flow that implements a "think - plan - select tool - execute tool - interact - evaluate" cycle.

>:warning: **Do not use markdown in the prompt** for ReAct playbooks because that will interfere with the playbook program's structure that uses #, ## and ### headings. Use xml tags like `<output_format>`, `<planning_rules>`,  `<style_guide>`, etc. for defining various parts of the prompt.

### Playbook definition

Like other playbooks, a ReAct playbook is defined with a second-level heading (`##`) followed by the playbook name.

The description that follows the playbook name is much more important in ReAct playbooks, as it serves as the primary instruction set for the LLM. This description should be detailed and clear about:

1. The objective of the playbook
2. The constraints and requirements
3. The expected output or deliverable
4. Any special considerations or approaches to take

### Description placeholders

Like markdown playbooks, ReAct playbook descriptions support dynamic content using `{expression}` placeholders.

See [Markdown Playbooks - Description placeholders](markdown-playbooks.md#description-placeholders) for full details on placeholder syntax and capabilities.

### Triggers

The `### Triggers` section works the same way as in standard markdown playbooks, defining the conditions under which the playbook should execute.

## Default execution flow

When a ReAct playbook is executed (i.e., a playbook without explicit steps), the system automatically applies a default ReAct execution flow. This flow is dynamically compiled and added to the playbook at runtime.

The default ReAct steps follow this pattern:

```markdown
- Think deeply about the $task to understand requirements
- Write down $exit_conditions for the task
- While $exit_conditions are not met:
  - Analyze current state and progress
  - Decide what action to take next
  - Execute the action (tool call, user interaction, computation)
  - Evaluate results against exit conditions
- Return final results
```

### Execution cycle

The ReAct loop enables the LLM to:

1. **Understand** - Analyze the task requirements deeply
2. **Define Success** - Establish clear exit conditions for task completion
3. **Iterate** - Loop through a cycle of analysis, action, and evaluation
4. **Act** - Execute appropriate actions (tool calls, user interactions, computations)
5. **Evaluate** - Check progress against exit conditions
6. **Complete** - Return final results when exit conditions are met

## Example

Here's an example of a ReAct playbook for deep product research:

```text
## ResearchProduct
This playbook conducts comprehensive research on a product specified by the user.

Use WebSearch to find relevant information. Analyze the data critically and present findings in a clear, organized format. Prioritize recent sources (within the last year if possible) and reputable websites.

<planning_rules>
    - Always start by determining the exact product to research
    - Create a structured research plan with specific queries
    - Perform multiple searches with different queries to get comprehensive information
    - Group searches by category (general info, reviews, comparisons)
    - Verify information across multiple sources when possible
    - If conflicting information is found, note the discrepancy and evaluate source credibility
</planning_rules>

<style_guide>
    - Write in a neutral, objective tone
    - Use clear headings and subheadings for organization
    - Present pros and cons in balanced fashion
    - Support claims with evidence from research
    - When providing your recommendation, clearly explain your reasoning
</style_guide>

<output_format>
    # Product Research: [Product Name]

    ## Overview
    [General product information]

    ## Features and Specifications
    [Detailed features]

    ## Customer Sentiment
    [Analysis of customer reviews]

    ## Competitive Comparison
    [Comparison with alternatives]

    ## Pros and Cons
    [Balanced assessment]

    ## Recommendation
    [Final recommendation with justification]
</output_format>

### Triggers
- When user wants to research a product
```

## Related topics

- [Markdown Playbooks](markdown-playbooks.md) - For more structured, step-by-step approaches
- [Python Playbooks](python-playbooks.md) - For complex logic and integrations
- [Working with Artifacts](../artifacts/index.md) - How ReAct playbooks can create and store data
