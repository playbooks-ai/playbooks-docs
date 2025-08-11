# Playbooks Assembly Language (PBAsm)

The Playbooks Assembly Language (PBAsm) is a low-level, structured representation of Playbooks programs designed specifically for execution by Large Language Models. Just as traditional assembly languages use instruction sets optimized for CPU architectures, PBAsm uses an instruction set optimized for the unique capabilities and characteristics of LLMs as execution engines.

## The LLM as CPU Architecture

### Traditional CPU vs LLM Execution Engine

|  | **CPU Executing Assembly/Binary code** | **LLM Executing PBAsm code** |
|------------|-----------------------------------|-------------------------|
| **Instruction Format** | Binary opcodes (e.g., `0x89 0xE5` for MOV EBP, ESP) | Semantic instructions (e.g., `01:EXE Var[$name:str, "Alice"]`) |
| **Basic Instructions** | MOV, ADD, JMP, CALL, RET, CMP | EXE, TNK, QUE, CND, CHK, YLD, JMP, RET |
| **Memory Model** | Direct memory addresses, registers (EAX, EBX, ESP) | Short term memory with variables (`$name:str`, `$count:int`), Long term memory system |
| **Variable Assignment** | `MOV [0x1000], 42` (write to memory address) | `Var[$count:int, 42]` (semantic variable binding) |
| **Function Calls** | `PUSH params; CALL 0x4000; POP result` | `$result = FunctionName(param=$value); YLD call` |
| **Control Flow** | `CMP EAX, 0; JE label` (compare and jump) | `02:CND If $name is provided` (semantic condition) |
| **Loops** | `loop_start: DEC ECX; JNZ loop_start` | `03:CND While $i < 10` with nested steps |
| **Stack Operations** | `PUSH EAX; POP EBX` (explicit stack manipulation) | Implicit call stack managed by runtime |
| **Return Values** | Store in EAX register by convention | `04:RET $result` (explicit return statement) |
| **Interrupts** | INT 0x80 (system call), hardware IRQ | `Trigger["PlaybookName:01:EVT"]` (semantic events) |
| **Yielding Control** | Context switch via OS scheduler | `YLD user/call/exit` (explicit yield reasons) |
| **Line Addressing** | Absolute/relative addresses (0x4000, +10) | Hierarchical numbering (01, 01.01, 01.01.01) |
| **Conditional Execution** | Flag-based (ZF, CF, OF) after CMP | Natural language conditions evaluated by LLM |
| **Data Types** | Primitive (byte, word, dword, float) | Semantic types (str, int, float, bool, list, dict, artifact, memory) |
| **Error Handling** | Segfault, divide by zero, invalid opcode | Graceful degradation, runtime validation of outputs |
| **Debugging** | GDB breakpoints, register inspection | VSCode debugger - step debugging, variable inspection |
| **Side Effects** | Direct I/O port access, memory writes | Queued operations via QUE, verified by runtime |
| **Compilation** | Source → AST → Machine code | Playbooks → PBAsm → Runtime Context → LLM tokens |
| **Parallelism** | Out-of-order execution, SIMD | Queued operations can batch (multiple QUE before YLD) |
| **State Persistence** | CPU registers reset on context switch | Variables persist across YLD operations |
| **Program Counter** | EIP/RIP register points to next instruction | Runtime tracks current playbook line number (e.g. OrderStatus:01.03) |
| **Subroutines** | CALL pushes return address, RET pops | Playbook calls with QUE, across agents |
| **Execution Context** | CPU state (registers, flags, stack) | Conversation history, variable state, queued ops |

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

- `YLD call` - Execute queued function calls (including Say() calls)
- `YLD user` - Wait for user input (only after asking for input)
- `YLD agent` - Wait for input from another agent
- `YLD meeting` - Wait for input from a meeting you are participating in
- `YLD exit` - Terminate the program

## Structured Output Protocol

Unlike traditional assembly that modifies CPU registers, PBAsm instructions produce structured outputs that the runtime can parse and verify:

### Variable Operations
```
Var[$name, <value>]
```
Similar to how assembly instructions modify CPU registers, but operates on named variables with semantic meaning. Variables must include type annotations: `$varname:type` where type is one of: `str`, `int`, `float`, `bool`, `list`, `dict`, `artifact`.

### Function Calls
```
$result = PlaybookName(param1, param2=$value2) ← Standard Python syntax
$result = Call PlaybookName with param1, param2=$value2 ← Natural language syntax
Get $result from PlaybookName ← Implicit argument passing
$result = PlaybookName(task user specified, details=details of the task) ← Natural language arguments
```

### Trigger Events (LLM Interrupts)
```
### Triggers
- T1:BGN When program starts
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
### Triggers
- T1:CND When user provides their email address
- T2:BGN At the beginning  
- T3:EVT When payment processed event is received
- T4:EVT When Accountant agent is ready with the invoice
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
01:QUE Say(Present options); no yield needed
02:QUE Say(Ask user to select one); YLD user
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

## Conclusion

PBAsm represents a foundational step toward treating LLMs as first-class computational engines with their own optimized instruction sets, enabling the development of reliable, scalable, and maintainable AI agent systems. By providing a structured intermediate representation between natural language and LLM execution, PBAsm enables sophisticated tooling, analysis, and runtime optimization while maintaining the semantic richness that makes LLM-based computing powerful.

## Learn More

Explore different types of playbooks:

- [Markdown Playbooks](../playbook-types/markdown-playbooks.md) - How to write playbooks in markdown
- [ReAct Playbooks](../playbook-types/react-playbooks.md) - How to write playbooks in ReAct
- [Python Playbooks](../playbook-types/python-playbooks.md) - Using Python functions as playbooks