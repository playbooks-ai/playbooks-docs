# Playbooks Assembly Language

The Playbooks Language is designed to be human-readable, but to execute it reliably and enable interoperability across different implementations, the system compiles it into a Playbooks Assembly Language (PAL) format. This specification serves as the canonical representation for LLM-executed programs, enabling multiple implementations and tools to target the same runtime format.

## Purpose of the Playbooks Assembly Language

The Playbooks Assembly Language:

- Provides a canonical format for representing LLM-executed programs
- Enables interoperability between different authoring tools (markdown, visual designers, etc.)
- Allows multiple runtime implementations to execute the same programs
- Supports tooling ecosystem development around a common format

## Ecosystem Benefits

The PAL enables a rich ecosystem where:

- **Visual workflow designers** can generate programs targeting the PAL
- **Different authoring tools** (markdown, YAML, GUI builders) can compile to the same format
- Implementations using **other frameworks** such as LangGraph, Google Agent Development Kit, Autogen, etc can be converted into PAL format
- **Multiple runtime implementations** can execute PAL programs, enabling specialized execution runtimes for different use cases, hardwares, etc.
- **Analysis tools** can work with any PAL-compliant program
- **Debugging and monitoring tools** have a consistent format to target

## Structure of the Playbooks Assembly Language

When a Playbooks program is compiled to PAL format, it follows a structured representation:

## Trigger Representation

Triggers are standardized with specific codes:

| Code | Meaning | Description |
|------|---------|-------------|
| BGN  | Beginning | Trigger at the beginning of program execution |
| CND  | Conditional | Trigger when a condition is met |
| EVT  | Event | Trigger when an external event occurs |

Each trigger is numbered sequentially (`T1`, `T2`, etc.) for reference during execution.

## Command Codes

Each step in the assembly format is assigned a three-letter command code that defines its purpose:

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

The assembly format uses a precise line numbering system:

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

## Transformation from Playbooks Language to Playbooks Assembly Language

- Agent names are converted to CamelCase without spaces: `CustomerService` instead of `Customer Service`
- Playbook names are also converted to CamelCase without spaces: `Greeting` instead of `Greet the user`
- Parameters are preserved with their `$` prefix
- Return values are explicitly declared in the playbook header
- Documentation is added if missing or incomplete
- Composite steps are expanded into individual steps
- Checks for notes are added as `CHK` steps at appropriate places

## Example Transformation

Here's an example of how a simple markdown playbook is transformed to the PAL format:

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

### Corresponding Playbooks Assembly Language

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

## Benefits of the Playbooks Assembly Language

1. **Interoperability**: Multiple authoring tools can target the same runtime format
2. **Ecosystem**: Enables rich tooling ecosystem around a canonical specification
3. **Runtime Flexibility**: Multiple runtime implementations can execute PAL programs
4. **Standardization**: Consistent representation regardless of the original authoring method
5. **Tool Development**: Visual designers, IDEs, and other tools can generate PAL-compliant programs
6. **Clarity**: Explicit indication of step types and control flow
7. **Debugging**: Easier to track execution and identify issues across different tools
8. **Optimization**: Better performance through structured representation

## Learn More

Explore different types of playbooks:

- [Markdown Playbooks](../playbook-types/markdown-playbooks.md) - How to write playbooks in markdown
- [ReAct Playbooks](../playbook-types/react-playbooks.md) - How to write playbooks in ReAct
- [Python Playbooks](../playbook-types/python-playbooks.md) - Using Python functions as playbooks 