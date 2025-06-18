# Playbooks Assembly Language (PBAsm)

The Playbooks Assembly Language (PBAsm) is a low-level, structured representation of Playbooks programs designed specifically for execution by Large Language Models. Just as traditional assembly languages use instruction sets optimized for CPU architectures, PBAsm uses an instruction set optimized for the unique capabilities and characteristics of LLMs as execution engines.

## The LLM as CPU Architecture

### Traditional CPU vs LLM Execution Engine

Traditional assembly languages target CPUs that operate on:
- Binary data in registers and memory
- Precise arithmetic and logical operations  
- Deterministic branching based on flags
- Direct memory addressing

PBAsm targets LLMs that operate on:
- Semantic understanding of natural language instructions
- Contextual reasoning and inference capabilities
- Probabilistic decision-making under uncertainty
- Conversational state and dialogue management
- Structured output generation that can be parsed and verified

### The LLM Execution Model

The LLM execution engine has several key characteristics that inform PBAsm's design:

1. **Semantic Processing**: Unlike CPUs that manipulate binary data, LLMs process meaning and context
2. **Structured Output**: LLMs can generate parseable, structured responses that the runtime can verify
3. **Asynchronous Operations**: LLMs can queue operations and yield control while waiting for external calls
4. **Context Awareness**: LLMs maintain conversational state and can apply rules contextually
5. **Reasoning Capability**: LLMs can think through problems step-by-step before taking action

## The PBAsm Instruction Set

PBAsm's instruction set is specifically designed for these LLM characteristics:

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

- `YLD user` - Wait for user input (only after asking for input)
- `YLD call` - Execute queued function calls (including Say() calls)
- `YLD exit` - Exit the entire program

## Structured Output Protocol

Unlike traditional assembly that modifies CPU registers, PBAsm instructions produce structured outputs that the runtime can parse and verify:

### Variable Operations
```
Var[$name, <value>]
```
Similar to how assembly instructions modify CPU registers, but operates on named variables with semantic meaning. Variables must include type annotations: `$varname:type` where type is one of: `str`, `int`, `float`, `bool`, `list`, `dict`.

### Function Calls
```
$result = FunctionName(param1=$value1, param2=$value2)
```
Unlike traditional CALL instructions that use memory addresses, PBAsm uses semantic function names with typed parameters. All function calls must be wrapped in backticks and use valid Python syntax.

### Trigger Events (LLM Interrupts)
```
Trigger["PlaybookName:LineNumber:CommandCode"]
```
PBAsm's interrupt system - the LLM can signal semantic events that interrupt normal execution flow and trigger other playbooks to execute, similar to how hardware/software interrupts work in traditional CPUs.

## Compilation from Playbooks Language

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

### Compiled Format (PBAsm)
```
## GreetUser() -> None
This playbook greets the user and asks for their name.
### Triggers
- T1:BGN At the beginning
### Steps
- 01:QUE Say(Greet the user and ask for their $name:str); YLD user
- 02:CND If $name is provided
  - 02.01:QUE Say(Thank the user by $name); YLD call
- 03:CND Otherwise
  - 03.01:QUE Say(Ask for their $name:str again); YLD user
- 04:RET
```

## Line Numbering and Control Flow

PBAsm uses a hierarchical line numbering system that enables precise control flow:

- **Top-level steps**: `01`, `02`, `03`
- **Sub-steps**: `01.01`, `01.02`, `01.03`
- **Nested sub-steps**: `01.01.01`, `01.01.02`

This enables:
- **Precise jumping**: `JMP 01` to return to a specific line (used in loops)
- **Conditional nesting**: Clear structure for if/else and loops
- **Error recovery**: Ability to resume at specific execution points

## Trigger System: LLM Interrupts

PBAsm includes a sophisticated interrupt system that leverages the LLM's ability to recognize semantic patterns. Like traditional CPU interrupts, PBAsm triggers can interrupt normal execution flow when specific conditions are met:

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

## Key Patterns and Best Practices

### Function Call Patterns

**Simple function call:**
```
01:QUE $result:dict = GetWeather(city=$city); YLD call
```

**Nested function calls (decomposed):**
```
01:QUE $temp:str = FuncB(x=$x); YLD call
02:QUE $result:dict = FuncA(param=$temp); YLD call
```

**Cross-agent calls:**
```
01:QUE $weather:dict = WeatherAgent.GetCurrentWeather(zip=98053); YLD call
```

**Batch call processing (concurrent execution):**
```
01:EXE Initialize empty $results:dict
02:CND For each $item in $items:list
  02.01:QUE ProcessItem(item=$item); do not yield
03:YLD call to execute all queued calls concurrently
04:EXE Collect results into $results:dict by item id
```

### User Interaction Patterns

**Single question:**
```
01:QUE Say(Ask user for their $name:str); YLD user
```

**Multi-turn conversation:**
```
01:QUE Say(Welcome and ask how to help); YLD user
02:QUE Say(Continue conversation to meet criteria); YLD user; done after criteria met
```

**Enqueue multiple messages:**
```
01:QUE Say(Here are the options); no yield needed
02:QUE Say(Which would you prefer?); YLD user
```

### Metadata and Public Playbooks

Agents and playbooks can include metadata in YAML format:

```
# AgentName
metadata:
  model: claude-sonnet-4.0
  author: name@example.com
---
Agent description

## PlaybookName
metadata:
  public: true
---
Playbook description
```

Public playbooks are exposed for cross-agent communication and included in the generated `public.json`.

## Advantages of PBAsm

1. **Semantic Precision**: Natural language instructions with assembly-like precision
2. **Interoperability**: Multiple authoring tools can target PBAsm
3. **Analysis capability**: Static analysis tools can examine PBAsm programs
4. **Runtime flexibility**: Different LLM runtimes can execute the same PBAsm code
5. **Debugging support**: Clear execution model enables sophisticated debugging tools
6. **Concurrent execution**: Support for batched operations and asynchronous calls
7. **Cross-agent communication**: Built-in support for multi-agent systems

## Comparison with Traditional Assembly

| Aspect | Traditional Assembly | Playbooks Assembly |
|--------|---------------------|-------------------|
| **Target CPU** | Microprocessor | Large Language Model (LLM) |
| **Data Types** | Binary, integer, float | string, number, boolean, list, dict, null |
| **Instructions** | MOV, ADD, JMP, CALL | EXE, TNK, QUE, CND, CHK, RET, JMP, YLD |
| **Control Flow** | Flags, conditional jumps | Semantic conditions, natural language triggers |
| **Interrupts** | Hardware/software interrupts | Semantic triggers, event-driven playbook invocation |
| **I/O** | Port access, interrupts | Conversation (Say), artifacts, multi-agent communication |
| **Concurrency** | Thread management | Queued operations with YLD call |

## Conclusion

PBAsm represents a foundational step toward treating LLMs as first-class computational engines with their own optimized instruction sets, enabling the development of reliable, scalable, and maintainable AI agent systems. By providing a structured intermediate representation between natural language and LLM execution, PBAsm enables sophisticated tooling, analysis, and runtime optimization while maintaining the semantic richness that makes LLM-based computing powerful.

## Learn More

Explore different types of playbooks:

- [Markdown Playbooks](../playbook-types/markdown-playbooks.md) - How to write playbooks in markdown
- [ReAct Playbooks](../playbook-types/react-playbooks.md) - How to write playbooks in ReAct
- [Python Playbooks](../playbook-types/python-playbooks.md) - Using Python functions as playbooks