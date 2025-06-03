# Playbooks Assembly Language

The Playbooks Assembly Language (PBASM) is a low-level, structured representation of Playbooks programs designed specifically for execution by Large Language Models. Just as traditional assembly languages use instruction sets optimized for CPU architectures, PBASM uses an instruction set optimized for the unique capabilities and characteristics of LLMs as execution engines.

## The LLM as CPU Architecture

### Traditional CPU vs LLM Execution Engine

Traditional assembly languages target CPUs that operate on:
- Binary data in registers and memory
- Precise arithmetic and logical operations  
- Deterministic branching based on flags
- Direct memory addressing

PBASM targets LLMs that operate on:
- Semantic understanding of natural language instructions
- Contextual reasoning and inference capabilities
- Probabilistic decision-making under uncertainty
- Conversational state and dialogue management
- Structured output generation that can be parsed and verified

### The LLM Execution Model

The LLM execution engine has several key characteristics that inform PBASM's design:

1. **Semantic Processing**: Unlike CPUs that manipulate binary data, LLMs process meaning and context
2. **Structured Output**: LLMs can generate parseable, structured responses that the runtime can verify
3. **Asynchronous Operations**: LLMs can queue operations and yield control while waiting for external calls
4. **Context Awareness**: LLMs maintain conversational state and can apply rules contextually
5. **Reasoning Capability**: LLMs can think through problems step-by-step before taking action

## The PBASM Instruction Set

PBASM's instruction set is specifically designed for these LLM characteristics:

### Core Instructions

| Instruction | Purpose | LLM Operation | Runtime Verification |
|-------------|---------|---------------|---------------------|
| **EXE** | Execute imperative action/assignment | Process semantic instruction, update state | Parse variable assignments, validate state changes |
| **TNK** | Think deeply step by step | Engage reasoning capabilities before proceeding | Verify structured thinking output |
| **QUE** | Queue playbook/function call | Prepare asynchronous operation | Parse function calls with parameters |
| **CND** | Conditional/loop construct | Evaluate semantic conditions and control flow | Track conditional logic and execution paths |
| **CHK** | Apply contextual note/rule | Incorporate business rules into context | Verify rule application |
| **RET** | Return from playbook | Complete function execution with optional value | Parse return values |
| **JMP** | Jump to specific line | Transfer execution control | Validate line number targets |
| **YLD** | Yield control to runtime | Pause execution, transfer control | Parse yield targets (user/call/return/exit) |

### Yield Reasons

The **YLD** instruction includes specific reasons that define why the LLM is yielding control:

- `YLD user` - Wait for user input
- `YLD call` - Wait for queued function calls to complete  
- `YLD return` - Return from current playbook
- `YLD exit` - Exit the entire program

## Structured Output Protocol

Unlike traditional assembly that modifies CPU registers, PBASM instructions produce structured outputs that the runtime can parse and verify:

### Variable Operations
```
Var[$name, <value>]
```
Similar to how assembly instructions modify CPU registers, but operates on named variables with semantic meaning.

### Function Calls
```
$result = FunctionName(param1=$value1, param2=$value2)
```
Unlike traditional CALL instructions that use memory addresses, PBASM uses semantic function names with typed parameters.

### Trigger Events (LLM Interrupts)
```
Trigger["PlaybookName:LineNumber:CommandCode"]
```
PBASM's interrupt system - the LLM can signal semantic events that interrupt normal execution flow and trigger other playbooks to execute, similar to how hardware/software interrupts work in traditional CPUs.

### Communication
```
Say("message to user")
```
Direct semantic output to users, leveraging the LLM's natural language generation capabilities.

### Artifacts
```
SaveArtifact($name, "summary", "content")
LoadArtifact("artifact_name")
```
Persistent storage operations that maintain context across execution sessions.

## Compilation from Natural Language

### Source Format (Playbooks Language)
```markdown
## GreetUser
This playbook greets the user and asks for their name.

### Triggers
- At the beginning

### Steps
- Greet the user and ask for their name
- If name is provided
  - Thank the user by name
- Otherwise
  - Ask for their name again
```

### Compiled Format (PBASM)
```
## GreetUser() -> None
This playbook greets the user and asks for their name.
### Triggers
- T1:BGN At the beginning
### Steps
- 01:QUE Ask user for their $name:str
- 02:YLD user
- 03:CND If $name is provided
  - 03.01:QUE Thank the user by $name
  - 03.02:YLD call
- 04:CND Otherwise
  - 04.01:QUE Ask for their $name again
  - 04.02:YLD user
- 05:RET
```

## Line Numbering and Control Flow

PBASM uses a hierarchical line numbering system that enables precise control flow:

- **Top-level steps**: `01`, `02`, `03`
- **Sub-steps**: `01.01`, `01.02`, `01.03`
- **Nested sub-steps**: `01.01.01`, `01.01.02`

This enables:
- **Precise jumping**: `JMP 01` to return to a specific line
- **Conditional nesting**: Clear structure for if/else and loops
- **Error recovery**: Ability to resume at specific execution points

## Trigger System: LLM Interrupts

PBASM includes a sophisticated interrupt system that leverages the LLM's ability to recognize semantic patterns. Like traditional CPU interrupts, PBASM triggers can interrupt normal execution flow when specific conditions are met:

### Trigger Types
- **BGN** (Beginning): Execute when program starts
- **CND** (Conditional): Execute when semantic conditions are met
- **EVT** (Event): Execute on external events

### Trigger Registration and Handling
```
T1:CND When user provides their email address
T2:BGN At the beginning  
T3:EVT When payment is processed
```

The LLM continuously monitors these semantic conditions during execution. When a trigger condition is met, it interrupts the current playbook execution, saves the current state, and invokes the triggered playbook - much like how a CPU handles interrupts.

### Interrupt Handling Flow

1. **Normal Execution**: LLM processes instructions sequentially
2. **Condition Detection**: After each step, LLM evaluates trigger conditions  
3. **Interrupt Signal**: If condition is met, LLM signals `Trigger["PlaybookName:Line:Code"]`
4. **State Preservation**: Current execution context is maintained
5. **Handler Invocation**: Triggered playbook begins execution
6. **Return/Continue**: After handling, execution resumes or transfers control

This interrupt-driven architecture enables reactive, event-driven AI systems that can respond to changing conditions without polling - a fundamental advance in AI agent architecture.

## Runtime Execution Contract

The PBASM runtime contract ensures deterministic execution despite the probabilistic nature of LLMs:

### Output Format
```
recap – one-sentence summary of current state
plan  – one-sentence immediate goal
`Var[$name, <value>]`
`Step["Playbook:LineNumber:CommandCode"]`
trig? <no | `Trigger["PB:Ln:Code"]`>
yld <user | call | return | exit>
```

### Verification Rules
1. **Structured parsing**: All outputs must be parseable by the runtime
2. **Variable tracking**: State changes must be explicitly declared
3. **Trigger evaluation**: Must check for triggers after each step
4. **Execution tracing**: Each step must be logged with precise line numbers
5. **Control flow**: Must use proper yield statements for control transfer

## Advantages of PBASM
- **Interoperability**: Multiple authoring tools can target PBASM
- **Analysis capability**: Static analysis tools can examine PBASM programs
- **Runtime flexibility**: Different LLM runtimes can execute the same PBASM code
- **Debugging support**: Clear execution model enables sophisticated debugging tools

## Comparison with Traditional Assembly

| Aspect | Traditional Assembly | Playbooks Assembly |
|--------|---------------------|-------------------|
| **Target CPU** | Microprocessor | Large Language Model (LLM) |
| **Data Types** | Binary, integer, float | string, number, boolean, list, dict, artifact |
| **Instructions** | MOV, ADD, JMP, CALL | EXE, TNK, QUE, CND, CHK, YLD |
| **Control Flow** | Flags, conditional jumps | Semantic conditions, natural language triggers |
| **Interrupts** | Hardware/software interrupts, exception handlers | Semantic triggers, event-driven playbook invocation |
| **I/O** | Port access, interrupts | Conversation, structured output, multi-agent communication, MCP, A2A, Playbooks protocol, etc. |

## Conclusion

PBASM represents a foundational step toward treating LLMs as first-class computational engines with their own optimized instruction sets, enabling the development of reliable, scalable, and maintainable AI agent systems.

## Learn More

Explore different types of playbooks:

- [Markdown Playbooks](../playbook-types/markdown-playbooks.md) - How to write playbooks in markdown
- [ReAct Playbooks](../playbook-types/react-playbooks.md) - How to write playbooks in ReAct
- [Python Playbooks](../playbook-types/python-playbooks.md) - Using Python functions as playbooks 