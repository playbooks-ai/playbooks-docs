# Playbooks Programming Guide

> **Software 3.0 programming, where natural language is code and LLMs are CPUs.**

This is the comprehensive guide for writing Playbooks programs. Whether you're building your first agent or working on complex multi-agent systems, you'll learn to think at a higher behavioral abstraction level and leverage powerful framework features.

## What's Covered

- Think at the right abstraction level: specify agent behavior, not implementation mechanics
- Mix natural language and Python seamlessly on the same call stack
- Use powerful abstractions like multi-agent meetings, triggers, and dynamic plans
- Handle edge cases naturally without explicit code for every contingency
- Build complex, nuanced agent behaviors that are readable and verifiable

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Language Syntax and Formatting](#language-syntax-and-formatting)
3. [The Five Playbook Types](#the-five-playbook-types)
4. [Decomposing Tasks into Playbooks](#decomposing-tasks-into-playbooks)
5. [Natural Language vs Explicit Syntax](#natural-language-vs-explicit-syntax)
6. [Multi-Agent Programs](#multi-agent-programs)
7. [Triggers: Event-Driven Programming](#triggers-event-driven-programming)
8. [Description Placeholders](#description-placeholders)
9. [Artifacts](#artifacts)
10. [Common Patterns and Best Practices](#common-patterns-and-best-practices)
11. [Editing Existing Programs](#editing-existing-programs)
12. [Understanding PBAsm Compilation](#understanding-pbasm-compilation)

---

## Core Concepts

### Philosophy: Software 3.0

- **LLMs as CPUs**: Natural language instructions are the program; the runtime compiles them to PBAsm and executes on LLM
- **High-level behavior specification**: Describe what agents should do, not how to do it; focus on behavior, not mechanics
- **Soft + Hard logic**: Run soft logic (NL) on LLM, hard logic (Python) on CPU, on same call stack
- **Natural exception handling**: LLM handles edge cases without explicit code for every contingency
- **Verifiable execution**: Programs compile to structured PBAsm for auditing and debugging
- **Powerful abstractions**: Meetings, triggers, seamless integration - complex patterns built into the framework

### Key Abstractions

- **Agents** (H1 `#`) = Classes with state and methods
- **Playbooks** (H2 `##` or `@playbook`) = Methods/functions
- **Multi-agent communication** = Message passing + direct calls
- **Triggers** = Event-driven interrupts (like CPU interrupts)
- **Variables** = Prefixed with `$`, typed at runtime

---

## Language Syntax and Formatting

### File Structure

````markdown
# AgentName
Agent description and personality. Define capabilities and behavioral traits here.

## PlaybookName($param1, $param2)
Playbook description explaining what it does and when to use it.

### Triggers
- When to execute this playbook

### Steps
- Step 1
- Step 2

### Notes
- Additional guidance for LLM

```python
# Python code blocks can appear anywhere
@playbook
async def PythonPlaybook(param: str) -> dict:
    """Docstring becomes playbook description"""
    return result
```

# SecondAgent
Another agent in the same program file
````

### Formatting Rules

**Heading Tags**:
- `# AgentName` - Agent definitions with description
- `## PlaybookName($params)` - Playbook definitions
- `### Triggers`, `### Steps`, `### Notes` - Special sections within playbooks

**Metadata** - Key-value pairs at start of playbook description:
```markdown
## PlaybookName
execution_mode: raw
public: true
```

**Variables** - Always prefixed with `$`, optional type annotations:
```markdown
- Ask user for their $name
- $count:int = 10
- $result = GetData($name)
```

**Comments**: `<!-- This is a comment in Playbooks -->`

---

## The Five Playbook Types

### Decision Framework

```
START: What type of playbook do I need?
│
├─ Do I need deterministic logic, external APIs, or complex calculations?
│  └─ YES → Python Playbook
│       └─ Will I have 4+ Python playbooks in this agent and will this Python playbook NOT need to call a Markdown/ReAct/Raw Prompt playbook?
│           └─ YES → Extract into MCP Server instead
│
├─ Do I know the exact steps in advance?
│  └─ YES → Markdown Playbook
│
├─ Do steps depend on dynamic research/reasoning?
│  └─ YES → ReAct Playbook
│
├─ Do I need exact prompt control for single-shot task?
│  └─ YES → Raw Prompt Playbook
│
└─ Am I integrating external MCP server tools?
   └─ YES → External Playbook (via MCP agent)
```

### 1. Markdown Playbooks - Structured Workflows

**Use when**: Steps are known, process is repeatable, need explicit control flow

**Structure**:
```markdown
## PlaybookName($param1, $param2)
Description

### Triggers
- When condition is met

### Steps
- Step with natural language instruction
- $variable = Assign from another step
- If condition
  - Nested step
  - While another condition
    - Deeply nested step
- Otherwise
  - Alternative path
- Return result

### Notes
- Business rules that apply throughout execution
```

**Example**:
```markdown
## ProcessOrder($order_id)
Process a customer order from validation through fulfillment

### Steps
- Get $order from database using $order_id
- If $order was not found
  - Tell user order not found
  - Return error
- Validate payment for $order
- If payment is valid
  - Update order status to processing
  - Send confirmation email to customer
  - Return success
- Otherwise
  - Tell user payment failed
  - Return payment error
```

**Control Flow**:
- Sequential: Just list steps in order
- Conditional: `If condition`, `Otherwise`, `Else if condition`
- Loops: `While condition`, `For each $item in $list`
- Variable assignment: `$var = value` or `Get $var from source`
- Return: `Return value` or `Return $variable`
- End program: `End program` (terminates execution)

### 2. ReAct Playbooks - Dynamic Reasoning

**Use when**: Steps can't be predetermined, need research, adaptive behavior

**Structure**:
```markdown
## PlaybookName($param)
execution_mode: react  # Optional - inferred if no Steps section

Detailed description of task, goals, constraints, and expected output.

<planning_rules>
- Rule 1 for how to approach the task
- Rule 2 for verification
</planning_rules>

<style_guide>
- Tone and communication style
- Formatting preferences
</style_guide>

<output_format>
Expected structure of final output
</output_format>

### Triggers
- When to execute
```

**Key Points**:
- No `### Steps` section
- Framework provides default think-plan-act loop
- All playbooks available as tools
- LLM decides what actions to take

**Example**:
```markdown
## ResearchCompany($company_name)
Conduct comprehensive competitive analysis with market positioning,
products, pricing, and recent developments.

<planning_rules>
- Start by identifying primary products and services
- Search for recent news and financials (last 6 months)
- Verify information across multiple sources
- Compare with top 3 competitors
</planning_rules>

<output_format>
# Company Analysis: [Name]
## Overview
## Products
## Market Position
## Recent Developments
## Conclusion
</output_format>
```

### 3. Raw Prompt Playbooks - Full Control

**Use when**: Need exact prompt control, single-shot tasks, minimal overhead

**Structure**:
```markdown
## PlaybookName
execution_mode: raw

Exact prompt text. This goes directly to LLM.
Use {$variable} and {PlaybookCall()} for dynamic content.
```

**Key Points**:
- Single LLM call, no loops
- Cannot call other playbooks during execution
- No automatic context management
- Use for classification, extraction, formatting

**Example**:
```markdown
## CategorizeTicket
execution_mode: raw

Categorize this support ticket: {$ticket_message}

Categories:
- Technical Support
- Billing  
- Account Management
- General Inquiry

Respond with ONLY the category name.
Category:
```

### 4. Python Playbooks - Hard Logic

**Use when**: Need deterministic logic, external APIs, complex calculations

**Structure**:
````markdown
```python
from typing import Dict, List

@playbook
async def PlaybookName(param1: str, param2: int = 10) -> float:
    """
    Docstring becomes playbook description.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        Description
    """
    # Your Python code
    result = compute(param1, param2)
    
    # Can call other playbooks (Markdown or Python)
    summary = await SummarizeResult(result)
    
    return summary

@playbook(triggers=["When user provides PIN"], public=True)
async def ValidatePIN(pin: str) -> bool:
    """Validate PIN format and check database."""
    return len(pin) == 4 and pin.isdigit()
```
````

**Decorator Options**:
- `@playbook` - Basic playbook
- `@playbook(public=True)` - Callable by other agents
- `@playbook(export=True)` - Allow implementation export
- `@playbook(triggers=["condition"])` - Add triggers
- `@playbook(metadata={...})` - Custom metadata

**Key Points**:
- Full Python power: any library, complex logic, external APIs
- Use `await` to call other playbooks
- Return user-readable strings/dicts when called from Markdown
- Can call Markdown playbooks: `await MarkdownPlaybook(args)`

**Python-Only Agents**: You can build entire agents using only Python playbooks without any LLM calls. This is useful for deterministic workflows, prototyping, testing, or scenarios where you don't need AI reasoning. See the **[Python-Only Agents Guide](python-only-agents.md)** for details.

### When to Extract Python Playbooks to MCP Server

⚠️ **Important Rule**: If you have **more than 3 Python playbooks** in a single agent, extract them to a separate MCP server instead.

**Why Extract to MCP**:
- Keeps agent code focused on behavior, not implementation
- Python tools can be reused across multiple agents
- Better separation of concerns
- Easier testing and maintenance
- Can be developed and deployed independently

**How to Extract**:

1. **Create MCP server file** (e.g., `mcp.py`):

Use the [FastMCP](https://fastmcp.com) library to create an MCP server.

````python
from fastmcp import FastMCP

mcp = FastMCP("My Tools Server")

@mcp.tool
def GetUserInfo():
    """
    Get information about the user.
    
    Returns:
        A dictionary containing user information.
    """
    return {"name": "John", "email": "john@example.com"}

@mcp.tool
def CalculateSleepEfficiency(time_in_bed: int, time_asleep: int) -> float:
    """
    Calculate sleep efficiency percentage.
    
    Args:
        time_in_bed: Total minutes in bed
        time_asleep: Total minutes asleep
        
    Returns:
        Sleep efficiency as percentage
    """
    return round((time_asleep * 100) / time_in_bed, 1)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
````

1. **Run the MCP server**:

```bash
fastmcp run mcp.py -t streamable-http --port 8888
```

3. **Define MCP agent in your Playbooks program**:

```markdown
# ToolsAgent
This agent provides various Python tools.
remote:
  type: mcp
  url: http://127.0.0.1:8888/mcp
  transport: streamable-http

# MainAgent
Your main agent description.

## Main
### Steps
- Load user info from ToolsAgent
- Calculate sleep efficiency using ToolsAgent
- Tell user their sleep efficiency
```

**Example from insomnia.pb**:

```markdown
# MCP
This agent provides various python tools that the sleep coach will use.
remote:
  type: mcp
  url: http://127.0.0.1:8888/mcp
  transport: streamable-http

# Sleep Coach
You are a sleep coach helping users improve their sleep.

## Main
### Steps
- Load user info from MCP
- Get user's sleep efficiency from MCP
- Welcome user and use the info to help them
```

**When NOT to extract**:

- ✅ 1-3 Python playbooks that are tightly coupled to agent logic
- ✅ Python playbooks that call Markdown playbooks (requires `@playbook`)
- ✅ Python playbooks with triggers (requires `@playbook`)

**When to extract**:

- ✅ 4+ Python playbooks in single agent
- ✅ Pure utility functions (calculations, API calls, data transformations)
- ✅ Tools that could be reused by multiple agents
- ✅ Complex Python logic that benefits from separate testing

### 5. External Playbooks - Remote Tools

**Use when**: Integrating MCP servers, external APIs (roadmap)

**Structure**:
```markdown
# MCPAgent
remote:
  type: mcp
  transport: streamable-http
  url: http://localhost:8000/mcp

# LocalAgent
## Main
### Steps
- $weather = MCPAgent.get_weather(zipcode=98053)
- Tell user the $weather
```

**Key Points**:
- MCP server tools automatically become playbooks
- Call like any other playbook
- Framework handles transport and auth

---

## Decomposing Tasks into Playbooks

### Decomposition Strategy

1. **Identify distinct concerns**: What are the separable responsibilities?
2. **Look for reusability**: What might be called multiple times?
3. **Consider testing**: What would you want to test independently?
4. **Find boundaries**: Where do soft/hard logic boundaries exist?
5. **Separate I/O from logic**: User interaction vs computation

### Granularity Guidelines

**Too Fine-Grained** ❌
```markdown
## AskName
### Steps
- Ask user for name

## ThankUser($name)
### Steps
- Thank $name

## Main
### Steps
- Ask user for name
- Thank the user
```

**Appropriate** ✅
```markdown
## Main
### Steps
- Ask user for their $name
- Thank $name for providing their name
```

**Better Decomposition** ✅
```markdown
## ProcessOrder
### Steps
- Collect user info
- Process payment
- Fulfill order

## CollectUserInfo
### Steps
- Ask for $name, $email, $address; validate all fields
- Return collected info as dictionary

## ProcessPayment($user_info)
### Steps
- Calculate $amount and charge payment
- Return payment record
```

### When to Create Separate Playbooks

**Create separate playbook when**:

- ✅ Logic might be reused elsewhere
- ✅ Has clear single responsibility
- ✅ Could be triggered independently
- ✅ Needs Python for deterministic logic
- ✅ Represents distinct business process
- ✅ Makes main flow more readable

**Keep inline when**:

- ✅ Used only once
- ✅ Tightly coupled to parent context
- ✅ Simple, linear flow
- ✅ Would hurt readability to separate

---

## Natural Language vs Explicit Syntax

### The Spectrum of Explicitness

Playbooks supports a spectrum from pure natural language to Python-like explicit syntax. **Prefer natural language** unless explicitness aids clarity or correctness.

### Variable Assignment

**Natural Language** (Preferred):
```markdown
- Ask user for their order id
- Get order details from database
- Calculate shipping cost
```

**Explicit**:
```markdown
- $order_id = AskForOrderId()
- $order_details = GetOrderDetails($order_id)
- $shipping_cost = CalculateShipping($order_details.weight, $order_details.destination)
```

### When to Use Each Style

**Pure Natural Language**:
```markdown
- Greet user and ask what they need help with
- Find the most relevant article for their question
- Share the article with friendly explanation
```

- ✅ Clear intent
- ✅ One-time flow
- ✅ No complex data passing

**Variable Names** (add clarity):
```markdown
- Ask user for their $email and $password
- Validate $email format
- If $email is invalid
  - Tell user $email is not valid
```

- ✅ Value used multiple times
- ✅ The variable should become part of the agent's state
- ✅ Type helps LLM understand

**Explicit Calls** (precision needed):
```markdown
- $temp_c = ConvertToCelsius($temp_f)
- $weather = WeatherAgent.GetForecast(zipcode=$zipcode, units="metric")
- $summary = FormatWeather($weather, temperature=$temp_c)
```

- ✅ Exact parameters matter
- ✅ Cross-agent calls
- ✅ Return value used in computation

### Function Call Syntax Options

All of these are valid:

```markdown
# Natural language
- Get order status

# Explicit call with variable
- $status = GetOrderStatus(order_id=$order_id)

# Cross-agent call
- $status = OrderService.GetOrderStatus(order_id=$order_id)
```

**Guidelines**:

1. Start natural, add explicitness only when needed
2. Use `$variables` when value is referenced multiple times
3. Use explicit calls for cross-agent or when parameters matter
4. Type annotations helpful for complex data: `$results:list`, `$config:dict`

---

## Multi-Agent Programs

### When to Use Multiple Agents

**Use multiple agents when**:

- ✅ Different domains of expertise (TravelAdvisor, HotelAdvisor, FlightAdvisor)
- ✅ Different roles in process (Host, Player)
- ✅ Separation of concerns (Frontend, Backend, Database)
- ✅ Specialized models needed (FastAgent with GPT-4o-mini, ResearchAgent with Claude)
- ✅ Independent scaling or deployment
- ✅ Separation of LLM context and knowledge

**Use single agent when**:

- ✅ Shared context and state
- ✅ Simple workflow
- ✅ Tight coupling between components

### Creating Multiple Agents

Creating agents is easy in Playbooks. Simply add a new H1 tag and describe the agent.

```markdown
# PrimaryAgent
Description of primary agent

## Main
### Triggers
- At the beginning
### Steps
- Do primary work
- Call SpecializedAgent when needed

# SpecializedAgent  
Description of specialized agent

## ProcessTask($data)
public: true
### Steps
- Process $data with specialized logic
- Return result
```

### Agent Communication Methods

#### 1. Direct Public Playbook Calls

One agent directly calls another's public playbook:

```markdown
# TaxAgent
## GetTaxRate($income)
public: true
### Steps
- Calculate and return tax rate based on $income

# IncomeAgent
## ProcessIncome
### Steps
- Ask user for $income
- Get $tax_rate from TaxAgent
- Tell user their $tax_rate
```

Use for synchronous request-response with immediate return value.

#### 2. Natural Language Messaging

Send messages for asynchronous communication:

```markdown
# Manager
## AssignWork($task)
### Steps
- Tell WorkerAgent to perform $task

# WorkerAgent
## PerformTask($task)
### Steps
- Perform the task
```

Use for fire-and-forget communication and async workflows.

#### 3. Meetings - Multi-Party Coordination

Host creates meeting for multi-agent coordination:

```markdown
# RestaurantConsultant
## MenuRedesignMeeting
meeting: true
required_attendees: [HeadChef, MarketingSpecialist]

### Steps
- Introduce myself and explain meeting purpose
- Explain the process we'll follow
- While meeting is active
  - Facilitate discussion
  - Keep discussion on track
  - Enforce max 30 turns
- If consensus reached
  - Summarize decisions
  - End meeting
  - Return menu proposal
- Otherwise
  - Return failure reason

# HeadChef
## MenuRedesignMeeting
meeting: true

### Steps
- Introduce myself and propose signature dishes
- While meeting is active
  - Respond to questions and evaluate suggestions

# MarketingSpecialist
## MenuRedesignMeeting
meeting: true

### Steps
- Present market analysis
- While meeting is active
  - Evaluate proposals and suggest pricing
```

**To create meeting**:

```markdown
- Start a menu redesign meeting with HeadChef and MarketingSpecialist
```

**Meeting mechanics**:

- Each agent needs a playbook with `meeting: true`
- Same playbook name across all participating agents
- Host agent creates meeting, invites attendees
- Meeting provides shared communication channel
- Messages visible to all participants
- Meeting ends when host returns from meeting playbook

**When to use meetings**:

- ✅ Multiple agents need to coordinate
- ✅ Shared context across participants
- ✅ Back-and-forth discussion needed
- ✅ Consensus building

### Multi-Agent Best Practices

1. **Clear interfaces**: Mark playbooks `public: true` when designed for cross-agent calls
2. **Meaningful agent names**: `TaxAccountant` not `Agent2`
3. **Document cross-agent contracts**: What parameters, what returns
4. **Handle failures**: What if agent doesn't respond?
5. **Avoid circular dependencies**: Agent A → Agent B → Agent A can deadlock

---

## Triggers: Event-Driven Programming

Triggers are natural language conditions that cause playbooks to execute automatically - like CPU interrupts. They enable declarative, reactive behavior in your agents.

⚠️ **Use Sparingly**: Triggers add "magic" behavior that can make programs harder to understand. Only use them when they significantly simplify your code.

### Why Use Triggers?

Triggers eliminate repetitive coordination code by automatically invoking playbooks when conditions are met. The primary use case is **input validation** - you can validate user input automatically without cluttering your main flow with validation logic.

### When to Use Triggers

✅ **DO use triggers for**:

- **Input validation** - Automatically validate when user provides data
- **State monitoring** - React to threshold violations or state changes
- **Cross-cutting concerns** - Behavior that applies throughout execution
- **Entry points** - "At the beginning" to start your program

❌ **DON'T use triggers for**:

- Normal sequential logic (just use steps)
- One-time checks (inline them instead)
- Complex workflows (be explicit with function calls)
- When the trigger condition is unclear

### The Validation Pattern: Before & After

**WITHOUT Triggers**:

```markdown
## Main
### Steps
- Ask user for their $email
- Validate $email and keep asking until valid
- Process login with $email
```

**WITH Triggers** (cleaner):

```markdown
## Main
### Steps
- Ask user for their $email
- Process login with $email

## ValidateEmail
### Triggers
- When user provides email
### Steps
- If $email format is invalid
  - Tell user email is invalid and ask again
```

**Key Benefit**: Main flow stays clean. Validation happens automatically when user provides input, eliminating repetitive validation calls.

### Trigger Types

**Temporal**:

```markdown
### Triggers
- At the beginning
- After 5 minutes
- At the end
```

**State-Based**:

```markdown
### Triggers
- When $attempts > 3
- When $balance becomes negative
- When $order_status is "shipped"
```

**User Interaction**:

```markdown
### Triggers
- When user provides email
- When user asks about refund
- When user seems frustrated
```

**Execution Flow**:

```markdown
### Triggers
- After calling ProcessPayment
- Before ending program
```

**External Events**:

```markdown
### Triggers
- When payment webhook is received
- When inventory drops below threshold
```

**Agent Communication**:

```markdown
### Triggers
- When another agent asks about availability
- When Manager assigns new task
```

### Common Trigger Patterns

**Pattern 1: State Guard**

Monitor state and react to violations:

```markdown
## Main
### Steps
- Set $attempts to 0
- While not authenticated
  - Ask user for credentials
  - Increment $attempts
  - Authenticate user

## CheckAttemptLimit
### Triggers
- When $attempts > 5
### Steps
- Tell user they've exceeded maximum attempts
- End program
```

**Pattern 2: Intent Detection**

Respond to user intent automatically:

```markdown
## Main
### Steps
- Welcome user
- Have conversation about their issue
- Resolve the issue

## ProvideHelp
### Triggers  
- When user asks for help
- When user seems confused
### Steps
- Explain available options and how to use them
- Ask what specific help they need
```

**Important**: Triggers are evaluated after each step. The LLM determines when a trigger condition is met based on semantic understanding.

### Trigger Best Practices

1. **Be specific**: "When user provides email" not "When email"
2. **Avoid conflicts**: Don't create multiple triggers for same condition
3. **Document intent**: Explain why the trigger exists in playbook description
4. **Test edge cases**: What if trigger fires mid-execution?
5. **Keep it simple**: If you have more than 3-4 triggers total, reconsider your design
6. **Prefer explicit**: When in doubt, use explicit function calls instead of triggers

---

## Description Placeholders

Inject dynamic content into playbook descriptions using `{expression}` syntax.

### Basic Usage

```markdown
## ProcessOrder
Processing order {$order_id} for customer {$customer_name}.
Today's date is {date.today().strftime("%Y-%m-%d")}.
```

When playbook executes:
```
Processing order 12345 for customer Alice Smith.
Today's date is 2025-10-06.
```

### What You Can Use

**Variables**:

```markdown
## ReviewTransaction
Transaction {$transaction_id} with amount ${$amount}
```

**Results of Playbook Calls**:

```markdown
## AnswerQuestions  
Q1 Summary: {QuarterlySummary("Q1")}
Q2 Summary: {QuarterlySummary("Q2")}

### Steps
- Answer questions based on summaries above
```

**Python Expressions**:

```markdown
## AnalyzePerformance
Score: {round($score * 100, 2)}%
Status: {"Excellent" if $score > 0.9 else "Good"}
Timestamp: {timestamp.strftime("%Y-%m-%d %H:%M")}
```

**Special Variables**:

```markdown
## Debug
Current agent: {agent.klass}
Playbook: {call.playbook_name}
Current time: {timestamp}
```

### Common Patterns

**Contextual Dates**:

```markdown
## SummarizeOrder($order)
Summarize order considering today is {date.today().strftime("%Y-%m-%d")}

### Steps
- If order is overdue
  - Apologize for delay
```

**Conditional Context**:

```markdown
## CustomerService
{"Customer is VIP - provide premium service" if $customer.tier == "VIP" else ""}
```

### Best Practices

1. **Evaluate once**: Placeholders resolved when playbook starts, not re-evaluated
2. **Keep simple**: Complex logic belongs in Python playbooks
3. **Import dependencies**: `from datetime import date` in Python block if needed
4. **Security**: No `eval`, `exec`, `subprocess`, `__import__`

---

## Artifacts

### Artifacts - Efficient Long Content Handling

Artifacts implement pass-by-reference semantics for long text content or large objects. When large values are passed between playbooks using pass-by-value, the content gets duplicated in LLM context multiple times. Artifacts solve this by storing content once and passing only the reference.

**The Problem**: Large values passed between playbooks get duplicated:
- When sent as an argument
- As a local variable in the receiving playbook
- In the state sent to the LLM

**The Solution**: Artifacts work like lazy loading:
- Content stored once, referenced by name
- Automatically loaded into context when referenced
- Unloaded from context after returning from the playbook that loaded it

**Usage**:
```python
# Automatic artifact creation (>80 chars)
$document = ReadFile("doc.md")

# Explicit artifact creation
await SaveArtifact("$report", "Q3 Report", """some content...""")

```

👉 **[Complete Guide](artifacts.md)** - Detailed explanation, paged memory model, API reference, and usage notes

**Tip**: Minimize artifact context time by loading and using them in separate playbooks. The artifact unloads when the playbook returns, keeping context small for later processing.

---

## Common Patterns and Best Practices

### Pattern: Python ↔ Markdown Composition

````markdown
```python
@playbook
async def ProcessItem(item: dict) -> str:
    """Fetch and process data with complex logic."""
    data = external_api.get(item['id'])
    summary = await SummarizeItem(data)  # Call Markdown playbook
    return summary
```

## SummarizeItem($item)
### Steps
- Format $item as user-friendly summary
````

### Pattern: Batch Operations

```markdown
- For each $order in $pending_orders
  - ProcessSingleOrder($order)
```

### Pattern: Error Handling

```markdown
## SafeOperation
### Steps
- Try to process $data
- If operation fails
  - Log error
  - Tell user operation failed with reason
  - Return error status
- Otherwise
  - Tell user success
  - Return success status
```

### Pattern: Collecting Inputs from User

When your agent needs information from the user, always ask for all inputs at once and establish a clear conversation loop until all valid data is acquired:

```markdown
## Main
### Steps
- Ask user for $email and $pin, engage in a conversation till user provides valid values or gives up
- If user gives up, apologize and return
- Inform user that you were able to authenticate them
```

This pattern:

- **Asks for all required information upfront** - more efficient for the user
- **Includes a clear termination condition** - handles the case where user wants to exit
- **Validates both inputs before proceeding** - ensures data quality
- **Avoids sequential asking** - better user experience than asking one at a time

**Why this matters**: Asking for information piece by piece creates a poor user experience. Users appreciate knowing all requirements upfront.

### Pattern: Mock Backend Interactions with Python Playbooks

Think if a certain action would require backend interaction (databases, APIs, authentication services). If so, use Python playbooks to encapsulate that logic. Use mock implementations as necessary to aid in development:

````markdown
```python
@playbook
async def AuthenticateUser($email: str, $pin: str) -> bool:
    """Authenticate user with email and PIN.
    
    In production, this would call the actual authentication service.
    For now, using mock data for development.
    """
    # Mock implementation for development
    return $email == "test@test.com" and $pin == "1234"

@playbook  
async def FetchUserProfile($user_id: str) -> dict:
    """Fetch user profile from database.
    
    Production: Query user database
    Development: Return mock data
    """
    # Mock implementation
    return {
        "id": $user_id,
        "name": "Test User",
        "preferences": {"theme": "dark"}
    }
```


This pattern:

- **Separates backend logic** - keeps the workflow clean and focused
- **Enables rapid prototyping** - test workflows without backend dependencies  
- **Makes transition to production easier** - just swap mock with real implementation
- **Documents backend contracts** - clear interface for what backend needs to provide
- **Testable** - mock data allows thorough testing of workflows

**When to use Python playbooks for backend**:

- Database queries or updates
- External API calls
- Authentication/authorization checks
- Complex business logic calculations
- File I/O operations
- Any stateful operations

### Anti-Pattern: Using step bullets for listing items, implicit loops, and redundant instructions

Bad example:

```markdown
### Steps
- Tell user about the plan
  - Phase 1: Understanding and Decomposition
  - Phase 2: Hypothesis Generation  
  - Phase 3: Synthesis Assessment
- Use agent collaboration
- After each phase, ask MetaCognitionAgent if the phase was executed optimally
```

This anti-pattern has the following problems:
- Each bullet point under Steps must be a statement to execute. The Phase 1, Phase 2, Phase 3 bullets are not, so should be in the same bullet as "Tell user"
- Redundant instruction "Use agent collaboration" that can't be executed as a statement
- Implicit loop "After each phase"

Here's the correct way to write it:
```markdown
### Steps
- Tell user about the plan - Phase 1: Understanding and Decomposition, Phase 2: Hypothesis Generation, Phase 3: Synthesis Assessment
- Go through each phase in order
  - Execute the phase with agent collaboration until the phase is complete
  - Ask MetaCognitionAgent if the phase was executed optimally
```


### Best Practices Summary

**DO**:

- ✅ Write playbook descriptions for humans - explain what and why
- ✅ Use natural language unless explicitness helps
- ✅ Add `### Notes` for business rules
- ✅ Prefer Markdown for workflows, Python for logic
- ✅ Extract 4+ Python playbooks to MCP server
- ✅ Make cross-agent playbooks `public: true`
- ✅ Use triggers sparingly - mainly for input validation
- ✅ Handle edge cases and errors gracefully
- ✅ Use meaningful variable names
- ✅ Break complex playbooks into smaller ones
- ✅ Test with different user inputs mentally
- ✅ Ask for all required information at once with conversation loops
- ✅ Use mock Python playbooks for backend processes during development
- ✅ Each step bullet must be a complete executable statement.

**DON'T**:

- ❌ Over-engineer simple flows
- ❌ Create too many tiny playbooks
- ❌ Use Raw mode unless truly needed
- ❌ Ignore error cases
- ❌ Make circular agent dependencies
- ❌ Use explicit syntax when natural language is clear
- ❌ Forget to document cross-agent contracts
- ❌ Overuse triggers - prefer explicit calls when flow is clearer
- ❌ Use triggers for sequential logic
- ❌ Ask for inputs one at a time when you need multiple pieces of information
- ❌ Mix backend API calls directly into workflow steps

---

## Editing Existing Programs

### Surgical Editing Principles

When modifying existing Playbooks programs:

1. **Read and understand**: Review the file, understand its structure and intent
2. **Minimal changes**: Change only what's needed to achieve the goal
3. **Preserve style**: Match existing natural language vs explicit style
4. **Maintain consistency**: Keep variable naming and structure patterns
5. **Test mentally**: Think through execution flow after changes

### Common Edit Patterns

**Adding a new playbook**:
```markdown
## NewPlaybook($param)
Description

### Steps
- New logic
```

**Modifying steps**: Find the playbook, locate the specific step, update it, and ensure variable references still work.

---

## Understanding PBAsm Compilation

### Why PBAsm Matters

When you write Playbooks, the compiler transforms it to Playbooks Assembly Language (PBAsm):

- **Adds explicit types**: `$name` → `$name:str`
- **Adds line numbers**: Hierarchical (01, 01.01, 01.01.01)
- **Adds opcodes**: QUE (queue), CND (conditional), RET (return), YLD (yield)
- **Explicit yields**: Shows when LLM yields control
- **Trigger labels**: T1:BGN, T2:CND, etc.

### Compilation Example

**Source**: `- Ask user for their name`

**Compiled**: `- 01:QUE Say(user, Ask user for their $name:str); YLD for user`

Adds: line numbers (01), opcodes (QUE), explicit types ($name:str), yield points (YLD for user).

### Key PBAsm Concepts

**Opcodes**: QUE (queue operation), CND (conditional), RET (return), YLD (yield), EXE (execute), TNK (think), JMP (jump)

**Yield Reasons**: `for user` (wait for input), `for call` (execute queued calls), `for agent` (wait for message), `for exit` (end program)

**Line Numbers**: Hierarchical (01, 01.01, 01.02) enable jumps and track execution position

### Why This Helps You

1. **Debugging**: When user reports issues, think about PBAsm execution
2. **Precision**: Know that fuzzy NL gets converted to structured form
3. **Optimization**: Understand when LLM calls happen (at YLD points)
4. **Reasoning**: Picture how LLM executes line by line

### Don't Write PBAsm

- ❌ Never write PBAsm directly
- ✅ Write natural Playbooks language
- ✅ Compiler handles transformation
- ✅ Understanding PBAsm helps debugging and optimization

---

## Quick Reference

### Minimal Working Program

```markdown
# MyAgent
Description of what this agent does

## Main
### Triggers
- At the beginning
### Steps
- Greet user
- Ask user what they need help with
- Help them
- End program
```

### Complete Example

````markdown
# TaskAgent
You help users manage their tasks efficiently.

```python
@playbook
async def SaveTask(task: str) -> dict:
    """Save task to database (mock implementation)."""
    return {"id": "123", "task": task, "status": "pending"}
```

## Main
### Triggers
- At the beginning

### Steps
- Greet user
- Ask what they'd like to do
- If user wants to add a task
  - Add a new task
- If user wants to list tasks
  - Show all pending tasks
- End program

## AddTask
### Steps
- Ask user for $task_description
- Save the task
- Tell user task was added successfully

## ValidateTaskDescription
### Triggers
- When user provides task description

### Steps
- If $task_description is empty
  - Tell user task cannot be empty
  - Ask again
````

### Cheat Sheet

| Task | Code |
|------|------|
| Define agent | `# AgentName` |
| Define playbook | `## PlaybookName($param)` |
| Add trigger | `### Triggers`<br>`- When condition` |
| Add steps | `### Steps`<br>`- Step 1` |
| Variable | `$variable_name` |
| Typed variable | `$count:int` |
| Assignment | `$var = value` |
| Condition | `If condition`<br>`  - Then step` |
| Loop | `While condition`<br>`  - Loop step` |
| Return | `Return value` |
| End program | `End program` |
| Call playbook | `PlaybookName($arg)` |
| Cross-agent call | `OtherAgent.PlaybookName($arg)` |
| Python playbook | `@playbook`<br>`async def Name(): ...` |
| Public playbook | `public: true` |
| ReAct playbook | No `### Steps` section |
| Raw playbook | `execution_mode: raw` |
| Meeting playbook | `meeting: true` |
| Save artifact | `SaveArtifact("name", "desc", $content)` |
| Load artifact | `LoadArtifact("name")` |
| Placeholder | `{$variable}` or `{expression}` |

---

## Programming Principles (EXTREMELY IMPORTANT!)

**Core Principles** - When writing Playbooks programs:

1. **Understand intent**: What problem are you solving? What is the goal?
2. **Choose right types**: Markdown for workflows, Python for logic, ReAct for research
3. **Natural first**: Start with natural language, add explicitness only when clarity demands it
4. **Think decomposition**: Break into logical playbooks with clear responsibilities
5. **⚠️ Extract to MCP**: If you have 4+ Python playbooks, extract them to an MCP server using fastmcp and use an MCP agent as a proxy
6. **Handle errors**: Consider edge cases and failure modes
7. **Write idiomatically**: Follow patterns and conventions from examples - write code that reads like a human wrote it
8. **Document choices**: Explain intent in descriptions and comments
9. **Iterate**: Start simple, add complexity as needed

**For AI Assistants** - Additional guidance when helping users:

- **Think deeply**: Plan in detail and review the plan before writing any code
- **Teach while building**: Explain architectural choices to help users learn
- **Use triggers sparingly**: Mainly for input validation, not normal control flow
- **Optimal Playbooks**: Write idiomatic code that uses Playbooks capabilities optimally to produce minimal, clean, readable programs
- **Framework migrations**: When converting from LangGraph, CrewAI, etc., produce the same behavior but leverage Playbooks' higher-level abstractions and natural language specifications

**Remember**: You're writing Software 3.0 - programs that execute on LLMs. Embrace natural language while maintaining precision. The compiler and runtime handle the complexity.

Happy building! 🚀