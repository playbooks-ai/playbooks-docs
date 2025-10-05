# Playbook Types

Playbooks framework supports multiple types of playbooks, each optimized for different scenarios. This flexibility allows you to choose the right approach for each aspect of your agent's behavior.

## Overview

Playbooks provides five distinct playbook types:

- **[Markdown Playbooks](#markdown-playbooks)** - Structured workflows with explicit steps
- **[ReAct Playbooks](#react-playbooks)** - Reasoning-based execution with tool usage
- **[Raw Prompt Playbooks](#raw-prompt-playbooks)** - Direct LLM prompts with full control
- **[Python Playbooks](#python-playbooks)** - Complex logic and external integrations
- **[External Playbooks](#external-playbooks)** - Remote tools and services via MCP or APIs

The power of Playbooks is the ability to mix and compose them seamlessly within a single agent. The frameworks also comes with a set of [built-in playbooks](./builtin-playbooks.md).

---

## Markdown Playbooks

**Best for:** Prescribed workflows, customer service scripts, structured processes

Markdown playbooks define step-by-step workflows in natural language. They are ideal when you know the exact sequence of actions the agent should follow.

### Structure

```markdown
## PlaybookName($param1, $param2)
Description of what this playbook does

### Triggers
- When user asks for help
- At the beginning

### Steps
- Step 1 instruction
- $variable = Step 2 with assignment
- If condition
  - Conditional step
- Step 3 instruction

### Notes
- Additional guidance or business rules
```

### Key Features

**Explicit Control Flow**
- Sequential steps executed in order
- Conditional logic (if/else)
- Loops (while, for each)
- Variable assignments

**Parameters**
- Define parameters in the playbook name: `PlaybookName($param1, $param2)`
- Use parameters as variables in steps: `$param1`, `$param2`

**Triggers**
- Define when the playbook should execute
- See [Triggers](./triggers.md) for details

**Notes Section**
- Provide additional context and business rules
- Guide LLM behavior throughout execution

:bulb: You can use natural language or explicit Python-like syntax in the steps. For example, `$order_details = GetOrderFromDatabase($order_id)`, `Get $order_details from the database` and `Get order details` can be equivalent.

### Example

```markdown
## CheckOrderStatus($customer_id)
Check the status of a customer's order

### Triggers
- When user asks about their order

### Steps
- Ask user for their order id
- Get order details from the database
- If order was not found
  - Tell user we couldn't find that order
- Otherwise
  - Tell user order status and when it will arrive
- End program

### Notes
- If order is delayed, let user know that they will receive a $10 store credit
```


### When to Use

✅ **Use Markdown Playbooks when:**

- Steps are known in advance
- Process follows a clear, repeatable pattern
- Need explicit control over execution flow
- Building customer service workflows or support scripts

❌ **Avoid when:**

- Steps cannot be predetermined
- Task requires extensive research or exploration
- Need complex Python logic or external API calls

---

## ReAct Playbooks

**Best for:** Research, problem-solving, dynamic planning, adaptive behavior

ReAct (Reasoning and Acting) playbooks let the LLM reason about the task and decide what actions to take. They excel when the exact steps cannot be predetermined.

### Structure

```markdown title="ReAct playbook structure"
## PlaybookName($param)
execution_mode: react
Detailed description of the task, goals, constraints, and expected output.

Use XML tags like <planning_rules>, <style_guide>, and <output_format>
to structure your prompt.

### Triggers
- When user needs research assistance
```

**Key difference:** No `### Steps` section. The framework provides a default think-plan-act loop. `execution_mode: react` is optional - any playbook without steps and without `execution_mode: raw` will be treated as a ReAct playbook.

:bulb: All playbooks are available as tools to be called from ReAct playbooks.

### Default Execution Flow

When a playbook has no explicit steps, Playbooks automatically applies a ReAct execution loop:

```markdown title="Default ReAct execution flow"
1. Think deeply about the task to understand requirements
2. Write down exit conditions for task completion
3. While exit conditions are not met:
   - Analyze current state and progress
   - Decide what action to take next
   - Execute the action (tool call, user interaction, computation)
   - Evaluate results against exit conditions
4. Return final results
```

### Example

```markdown title="ReAct playbook example"
## ResearchCompetitor($company_name)
Conduct comprehensive competitive analysis of the specified company.

Research the company's products, market position, pricing strategy, and
recent developments. Provide a balanced, data-driven analysis.

<planning_rules>
- Start by identifying the company's primary products and services
- Search for recent news and financial reports (last 6 months)
- Analyze customer reviews and sentiment
- Compare with top 3 competitors in the same space
- Verify information across multiple reputable sources
</planning_rules>

<style_guide>
- Maintain objective, analytical tone
- Support claims with specific evidence and sources
- Present both strengths and weaknesses
- Use clear headings and bullet points for organization
</style_guide>

<output_format>
    # Competitive Analysis: [Company Name]

    ## Overview
    [Company description and market position]

    ## Product Portfolio
    [Key products and services]

    ## Market Position
    [Market share, competitive advantages, challenges]

    ## Recent Developments
    [News, product launches, strategic changes]

    ## SWOT Analysis
    [Strengths, Weaknesses, Opportunities, Threats]

    ## Conclusion
    [Key insights and recommendations]
</output_format>

### Triggers
- When user requests competitive analysis
```

### When to Use

✅ **Use ReAct Playbooks when:**

- Task requires research or information gathering
- Steps cannot be determined in advance
- Need flexible, adaptive behavior
- Problem-solving requires iteration and refinement

❌ **Avoid when:**

- Need guaranteed execution order
- Process has strict compliance requirements
- Want explicit visibility into every step

---

## Raw Prompt Playbooks

**Best for:** Single-shot tasks, full prompt control, simple transformations

Raw prompt playbooks send your prompt directly to the LLM without any framework enrichment. Use when you need complete control over the exact text sent to the model.

### Structure

```markdown title="Raw prompt playbook structure"
## PlaybookName
execution_mode: raw

Your exact prompt text goes here. This will be sent to the LLM verbatim.

You can use {$variables} and {PlaybookCalls()} for dynamic content.
```

**Key difference:** Add `execution_mode: raw` metadata at the start of the description.

### Key Features

**Direct Prompt Control**

- Exactly what you write is what the LLM sees
- No automatic context, no conversation history
- No execution loop - single LLM call

**Description Placeholders**

- Use `{$variable}` to inject state variables
- Use `{PlaybookCall()}` to inject playbook results
- Placeholders resolved before sending to LLM

**No Framework Overhead**
- Minimal token usage
- Fastest execution
- Complete prompt transparency

### Example

```markdown title="Raw prompt playbook example"
## CategorizeTicket
execution_mode: raw

Here is a customer support ticket message:

{$ticket_message}

Categorize this ticket into one of the following categories:
- Technical Support
- Billing
- Account Management
- General Inquiry

Respond with ONLY the category name, nothing else.

Category:
```

### When to Use

✅ **Use Raw Prompt Playbooks when:**

- Need exact control over prompt text
- Single-shot task (classification, extraction, formatting)
- Want minimal token overhead
- Testing or debugging specific prompts

❌ **Avoid when:**

- Need multi-turn interaction
- Require tool usage or loops
- Want automatic context management
- Need observability into execution

### Important Limitations

⚠️ **Raw playbooks:**

- Make a single LLM call (no loops)
- Cannot call other playbooks during execution
- Do not receive automatic execution context
- Lose framework safety checks

For most use cases, prefer Markdown or ReAct playbooks for better observability and control.

---

## Python Playbooks

**Best for:** Complex calculations, data processing, external API integrations, business logic

### Structure

````markdown title="Python playbook structure"
# Agent Name

```python
from typing import Dict, List

@playbook
async def PlaybookName(param1: str, param2: int) -> float:
    """
    Playbook description goes in the docstring.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value
    """
    # Your Python code here
    result = perform_calculation(param1, param2)

    # Can call other playbooks
    other_result = await OtherPlaybook(result)

    return final_result
```
````

### Key Features

**Full Python Power**

- Standard Python syntax and semantics
- Access to any Python library
- Complex calculations and data transformations
- External API calls and integrations

**Decorator Options**

- `@playbook` - Basic playbook
- `@playbook(triggers=[...])` - Add trigger conditions
- `@playbook(public=True)` - Make available to other agents
- `@playbook(metadata={...})` - Add custom metadata

**Calling Other Playbooks**

- Use `await` to call markdown or Python playbooks
- Execute on the same call stack
- Mix Python and natural language seamlessly

### Example

````markdown title="Python playbook example"
# Shipping Calculator Agent

```python
from typing import Dict

@playbook
async def CalculateShipping(
    weight_kg: float,
    destination: str,
    is_expedited: bool = False
) -> Dict[str, float]:
    """
    Calculate shipping costs based on weight, destination, and speed.

    Args:
        weight_kg: Package weight in kilograms
        destination: Destination country code (e.g., "US", "UK")
        is_expedited: Whether to use expedited shipping

    Returns:
        Dictionary with cost breakdown
    """
    # Base rates by destination
    base_rates = {
        "US": 5.99,
        "UK": 12.99,
        "EU": 14.99,
        "ASIA": 19.99
    }

    base_cost = base_rates.get(destination, 24.99)
    weight_cost = weight_kg * 2.50
    expedited_cost = 15.00 if is_expedited else 0.00

    total = base_cost + weight_cost + expedited_cost

    return {
        "base": base_cost,
        "weight": weight_cost,
        "expedited": expedited_cost,
        "total": total,
        "currency": "USD"
    }

@playbook
async def ProcessShipment(order_id: str) -> str:
    """Process shipment for an order."""
    # Call another playbook to get order details
    order = await GetOrderDetails(order_id)

    # Calculate shipping using Python playbook
    cost = await CalculateShipping(
        order["weight"],
        order["destination"],
        order["is_express"]
    )

    # Update database
    update_shipping_cost(order_id, cost["total"])

    return f"Shipping cost calculated: ${cost['total']:.2f}"
```
````

### Decorator Parameters

**Reserved Parameters:**

- `triggers` - List of trigger conditions (strings)

**Standard Metadata:**

- `public` - Boolean, make callable by other agents
- `export` - Boolean, allow implementation export
- `remote` - Dict with `type`, `url`, `transport` for remote services

**Custom Metadata:**
All other keyword arguments become metadata attached to the playbook.

### When to Use

✅ **Use Python Playbooks when:**

- Need complex calculations or data processing
- Integrating with external APIs or databases
- Implementing business logic that's difficult in natural language
- Need type safety and code reuse

❌ **Avoid when:**

- Natural language description would be clearer
- Task is primarily about conversation or reasoning
- Don't need programmatic control

### Alternative: MCP Tools

For simple Python tools that don't need triggers or the ability to call markdown playbooks, consider using an [MCP Agent](./mcp-agent.md) instead.

---

## External Playbooks

**Best for:** Consuming tools from MCP servers

When you use an MCP server backed agent, all tools exposed by the MCP server are automatically available as external playbooks.

**Roadmap:**

- **APIs**: Using API specifications such as OpenAPI or Swagger, load available API endpoints as external playbooks.
- **From external agents**: Methods exposed by other agents via protocols such as the A2A protocol will be available as external playbooks.

### How to Use

Define an MCP agent:

```markdown title="MCP agent example"
# Github agent
agent_type: remote
remote:
  type: mcp
  url: "https://github.com/mcp"
  transport: "http"
```

Then call its public tools/playbooks like any other playbook:

```markdown
## MyWorkflow

### Steps
- $repo_handle = GithubAgent.GetRepository($repository_name)
- Get last 10 $commits
- Show user the list of $commits
```

:bulb: `Get last 10 $commits` is a natural language instruction and would be equivalent to something like `GithubAgent.GetCommits($repo_handle, limit=10)`, assuming appropriate tool description is available from the MCP server.

### Key Features

**Seamless Integration**

- Call remote services like local playbooks
- Framework handles authentication and transport transparently
- Automatic error handling and retries

### When to Use

✅ **Use External Playbooks when:**

- Integrating with existing MCP servers
- (roadmap) Calling specialized external services
- (roadmap) Connecting to other AI agent frameworks

---

## Choosing the Right Type

| Type | Executed on | Best For | Key Advantage | Limitation | Observability |
|------|-------------|----------|---------------|------------|-------------|
| **Markdown** | LLM |Structured workflows | Explicit control flow | Steps must be predetermined | Yes |
| **ReAct** | LLM | Research, problem-solving | Adaptive behavior | Less predictable execution | Yes |
| **Raw Prompt** | LLM | Single-shot tasks | Full prompt control | No loops or context | Limited |
| **Python** | CPU | Complex logic, APIs | Full programming power | More code to maintain | Yes |
| **External** | Remote | Remote services | Leverage existing tools | No callback capability | Limited |

### Decision Guide

**Start with Markdown if:**

- You know the steps in advance
- Process is repeatable and structured

**Use ReAct if:**

- Steps depend on intermediate results
- Task requires research or exploration

**Choose Python if:**

- Natural language can't express the logic
- Need external integrations or complex calculations

**Use Raw Prompt if:**

- Simple transformation or classification
- Want minimal overhead and exact prompt control

**Use External if:**

- Functionality already exists in an MCP server
- Integrating with external systems

## Mixing Playbook Types

One of Playbooks' most powerful features is seamless composition. You can freely mix types within a single agent:

````markdown title="Mixing playbook types example"
# Customer Service Agent

## HandleInquiry
### Steps
- Find inquiry type for user message # Raw prompt playbook
- If inquiry type is "technical"
  - Research the technical issue  # ReAct playbook
  - Format the research output # Python playbook
  - Tell user the formatted response

## ClassifyInquiry($message)
execution_mode: raw
Classify this inquiry: {$message}
Categories: technical, billing, general
Category:

## ResearchTechnicalIssue($issue)
Research the technical issue and provide a detailed solution.
<planning_rules>
- Search knowledge base first
- If not found, search web
- Verify solution applies to user's situation
</planning_rules>

```python
@playbook
async def FormatResponse(answer: str) -> str:
    """Format the answer with proper styling and links."""
    # Add styling, links, formatting
    return formatted_html
```
````
