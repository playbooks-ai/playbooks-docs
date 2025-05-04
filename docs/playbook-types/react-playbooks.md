# ReAct Playbooks

ReAct playbooks are a specialized type of playbook in the Playbooks AI framework that leverage the reasoning and planning capabilities of large language models. Unlike standard markdown playbooks, ReAct playbooks focus on dynamic problem-solving with less rigid structure.

## Overview

ReAct playbooks are ideal for:

- Complex problem-solving tasks
- Deep research and information gathering tasks
- Dynamic planning
- Tasks where the exact steps aren't known in advance

## Structure of a ReAct Playbook

A ReAct playbook is defined as a standard markdown playbook, but without the `### Steps` section:

```markdown
## PlaybookName
Detailed description of the task, goals, and constraints. Write full prompt here.

### Triggers
- Trigger condition 1
- Trigger condition 2
```

The key difference is that ReAct playbooks **do not** include a `### Steps` section. Instead, the system provides a default ReAct execution flow that implements a "think - plan - select tool - execute tool - interact - evaluate" cycle.

### Playbook Definition

Like other playbooks, a ReAct playbook is defined with a second-level heading (`##`) followed by the playbook name.

The description that follows the playbook name is much more important in ReAct playbooks, as it serves as the primary instruction set for the LLM. This description should be detailed and clear about:

1. The objective of the playbook
2. The constraints and requirements
3. The expected output or deliverable
4. Any special considerations or approaches to take

### Triggers Section

The `### Triggers` section works the same way as in standard markdown playbooks, defining the conditions under which the playbook should execute.

## Default ReAct Execution Flow

When a ReAct playbook is executed, the system applies a default execution flow that follows this pattern (this is a reference implementation, and may change in the future):

```markdown
- Think deeply about the task to understand requirements and context
- If task needs clarification
  - Ask the user clarification questions
  - Wait for user response
  - Update understanding of the task with user's response
- Initialize $task with clarified understanding and context of the task
- Initialize $task_status with "started"
- While $task_status is not "complete"
  - Think about the current state; Check if any playbooks can be used; create/update your plan for completing the task
  - Based on the plan, decide the next $task_action, one of ["call", "communicate", "finish"]; must produce a "finish" action at the end
  - If $task_action is "call"
    - Queue calls to appropriate playbooks with appropriate parameters
    - Wait for all the calls to complete
  - If $task_action is "communicate"
    - Decide whether to ask or tell: $communication_type
    - If $communication_type is "ask"
      - Formulate and ask question to the user
      - Wait for user response
    - If $communication_type is "tell"
      - Say appropriate message to the user
  - If $task_action is "finish"
    - If task is expected to produce a comprehensive report
      - Generate final result; follow the output format if specified; save the result as an artifact `SaveArtifact("name of report file.md", "One line summary of the report", "report content...")`
      - Return artifact reference 'Artifact["name of report file.md"]'
    - If task is expected to produce a short answer
      - Generate final result; follow the output format if specified
      - Return the answer as a string
    - Set $task_status to "complete"
```

This execution flow enables the LLM to:

1. **Think** - Analyze the task and context
2. **Plan** - Formulate a strategy to complete the task
3. **Act** - Execute the plan through calling playbooks, communicating with the user, or producing a final result
4. **Observe** - Process results and user feedback
5. **Reflect** - Update understanding and refine the plan

## Example: Research Playbook

Here's an example of a ReAct playbook for product research:

```markdown
## ResearchProduct
This playbook conducts comprehensive research on a product specified by the user. The research should include:

1. General product information (features, specifications, pricing)
2. Customer reviews and sentiment analysis
3. Comparison with at least 3 competing products
4. Pros and cons based on the research
5. A final recommendation with justification

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

## Benefits of ReAct Playbooks

ReAct playbooks offer several advantages:

1. **Flexibility**: They can handle a wide range of tasks without needing to specify exact steps in advance.
2. **Reasoning**: They leverage the LLM's reasoning capabilities to solve complex problems.
3. **Adaptability**: They can adjust their approach based on new information or changing requirements.
4. **Contextual understanding**: They consider the broader context and can make more nuanced decisions.
5. **Natural language guidance**: They can be directed with natural language instructions rather than rigid steps.

## When to Use ReAct Playbooks vs. Markdown Playbooks

Use ReAct playbooks when:

- The exact sequence of steps can't be predetermined
- The task requires complex reasoning or research
- The task has many possible approaches or paths
- You want to leverage the LLM's problem-solving abilities
- The task requires synthesis of information from multiple sources

Use standard markdown playbooks when:

- The workflow is well-defined and predictable
- You want to ensure specific steps are followed in a precise order
- The task is relatively simple with clear decision points
- Consistency and predictability are more important than flexibility

## Best Practices for ReAct Playbooks

1. **Be clear about objectives**: Clearly define what the playbook should accomplish.
2. **Provide context**: Include relevant background information.
3. **Define constraints**: Specify any limitations or requirements.
4. **Use special sections**: Leverage planning rules, style guides, and output format sections.
5. **Don't overspecify**: Avoid trying to dictate the exact thinking process.
6. **Test extensively**: ReAct playbooks may behave differently across runs, so test thoroughly.

## Related Topics

- [Markdown Playbooks](markdown-playbooks.md) - For more structured, step-by-step approaches
- [Python Playbooks](python-playbooks.md) - For complex logic and integrations
- [Working with Artifacts](../tutorials/working-with-artifacts.md) - How ReAct playbooks can create and store data
