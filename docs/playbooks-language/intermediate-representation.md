# Intermediate Representation

The Playbooks Language is designed to be human-readable, but to execute it reliably, the system transpiles it into an Intermediate Representation (IR) format. This IR serves as a bridge between the natural language programming model and the execution engine.

## Purpose of the Intermediate Representation

The Intermediate Representation:

- Standardizes playbooks for consistent execution
- Preserves the semantics of the original playbooks
- Enables precise tracking of execution state
- Facilitates programmatic analysis and validation
- Allows for more efficient runtime processing

## Structure of the Intermediate Format

When a Playbooks program is transpiled, it follows a structured format:

````
# <AgentName>
<Agent description>

```python
@playbook and other functions
```

## <PlaybookName>(<params>) -> <returnVar | None>
<Playbook description>
### Triggers
T<n>:<BGN|CND|EVT> <trigger text>
### Steps
01:<CMD> ...  # two-digit numbering; dot-notation for sub-steps
... more steps ...
### Notes
N<n> <text>
````

## Trigger Representation

Triggers are standardized with specific codes:

| Code | Meaning | Description |
|------|---------|-------------|
| BGN  | Beginning | Trigger at the beginning of program execution |
| CND  | Conditional | Trigger when a condition is met |
| EVT  | Event | Trigger when an external event occurs |

Each trigger is numbered sequentially (`T1`, `T2`, etc.) for reference during execution.

## Command Codes

Each step in the intermediate format is assigned a three-letter command code that defines its purpose:

| Code | Meaning | Description |
|------|---------|-------------|
| EXE  | Execute | Perform an imperative action or assignment |
| QUE  | Queue | Queue a playbook or function call for execution |
| TNK  | Think | Think deeply step by step before continuing |
| CND  | Condition | Represent an `if`, `else`, `while`, or `for` condition |
| CHK  | Check | Apply a note or rule to the current context |
| RET  | Return | Return from the current playbook |
| JMP  | Jump | Jump to another step in the playbook |
| YLD  | Yield | Yield control, with different targets: user, call, return, exit |

## Line Numbering

The intermediate format uses a precise line numbering system:

- Top-level steps use two-digit numbers: `01`, `02`, `03`, etc.
- Sub-steps use dot notation: `01.01`, `01.02`, etc.
- Nested sub-steps add another level: `01.01.01`, etc.

For example, an if-condition with nested steps would be represented as:

```
03:CND If $total > 100
  03.01:EXE Apply $discount of 10%
  03.02:QUE Tell the user they received a discount
04:EXE Continue with checkout
```

## Transformation from Playbooks Language to Intermediate Format

- Agent names are converted to CamelCase without spaces: `CustomerService` instead of `Customer Service`
- Playbook names are also converted to CamelCase without spaces: `Greeting` instead of `Greet the user`
- Parameters are preserved with their `$` prefix
- Return values are explicitly declared in the playbook header
- Documentation is added if missing or incomplete
- Composite steps are expanded into individual steps
- Checks for notes are added as `CHK` steps at appropriate places

## Example Transformation

Here's an example of how a simple markdown playbook is transformed to the intermediate format:

### Original Markdown

```markdown
# Customer Support

## Greeting
This playbook greets the user and asks for their order number.

### Triggers
- At the beginning

### Steps
- Greet the user and ask for their order number
- If user provides an invalid order number
  - Ask them to try again
- Look up order status
- Tell the user their order status

### Notes
- Be polite and professional
```

### Transformed Intermediate Format

```
# CustomerSupport
This agent provides customer support services, helping users track orders and resolve issues.

## Greeting() -> None
This playbook greets the user and asks for their order number.
### Triggers
T1:BGN At the beginning
### Steps
01:QUE Greet the user and ask for their order number
02:YLD user
03:CND If user provides an invalid order number
  03.01:QUE Ask them to try again
  03.02:YLD user
  03.03:JMP 03 to check again
04:QUE Look up order status
05:QUE Tell the user their order status
06:RET
### Notes
N1 Be polite and professional
```

## Benefits of the Intermediate Format

1. **Standardization**: Consistent representation regardless of the original playbook style
2. **Clarity**: Explicit indication of step types and control flow
3. **Debugging**: Easier to track execution and identify issues
4. **Optimization**: Better performance through structured representation
5. **Interoperability**: Enables different execution engines and integrations

## Learn More

Explore different types of playbooks:

- [Markdown Playbooks](../playbook-types/markdown-playbooks.md) - How to write playbooks in markdown
- [ReAct Playbooks](../playbook-types/react-playbooks.md) - How to write playbooks in ReAct
- [Python Playbooks](../playbook-types/python-playbooks.md) - Using Python functions as playbooks 