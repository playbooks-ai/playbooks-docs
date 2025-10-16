# Migrating from Other Agent Frameworks

If you're coming from other agent frameworks like LangGraph, CrewAI, or AutoGen, this guide will help you translate your existing implementations into idiomatic Playbooks code. You can expect [significant reduction in complexity and code size](../../reference/playbooks-traditional-comparison/).

______________________________________________________________________

## Why Migrate to Playbooks?

| Benefit                    | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| **less code**              | Eliminate boilerplate and framework complexity          |
| **Natural language first** | Write agent behavior in plain English                   |
| **Soft + hard logic**      | Seamlessly mix LLM reasoning with deterministic Python  |
| **Verifiable execution**   | Compiled to auditable PBAsm for debugging               |
| **First principles**       | Built from the ground up for the LLM era (Software 3.0) |
| **No framework lock-in**   | Natural language programs are portable                  |

______________________________________________________________________

## Traditional Agent Frameworks

Playbooks can express the same agent behaviors as these popular frameworks:

| Framework                                                                 | Type                        | Playbooks Advantage                                          |
| ------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------ |
| **[LangGraph](https://langchain-ai.github.io/langgraph/)**                | State graph-based agents    | Replace complex state graphs with natural language workflows |
| **[CrewAI](https://www.crewai.com/)**                                     | Multi-agent collaboration   | Native multi-agent support without role/task boilerplate     |
| **[AutoGen](https://microsoft.github.io/autogen/)**                       | Multi-agent conversations   | Simpler agent communication with triggers                    |
| **[LangChain Agents](https://python.langchain.com/docs/modules/agents/)** | Classic agent patterns      | Natural language replaces chain composition                  |
| **[Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/)** | AI orchestration SDK        | Direct LLM execution vs orchestration layer                  |
| **[Haystack](https://haystack.deepset.ai/)**                              | NLP with agent capabilities | Focused on agents, not general NLP                           |
| **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)**            | Autonomous agents           | Structured playbooks vs autonomous loops                     |

______________________________________________________________________

## Migration Process

### Step 1: Understand Your Agent's Behavior

Before migrating code, understand:

- What does the agent do?
- What are the key workflows?
- What tools/functions does it use?
- How do agents communicate (if multi-agent)?

**Focus on behavior, not framework mechanics.**

### Step 2: If using AI coding assistants

1. Create a `playbooks` folder for the converted code

1. Copy prompt for your AI assistant from [here](../ai-assistants/#prompt-for-ai-coding-assistants)

1. Ask the AI assistant to convert the source implementation to Playbooks with the following prompt:

   ```text
   <prompt copied above>

   Read source implementation at <agent>.py carefully. Convert to an equivalent Playbooks program in playbooks/<agent>.pb. Create all new files in the playbooks folder. Create MIGRATION.md file at the end with before/after comparison include code size reduction.
   ```

   Use appropriate and file name.

### Step 3: If doing manual conversion

Use this mapping to translate concepts:

| Source Framework | Concept                           | Playbooks Equivalent                        |
| ---------------- | --------------------------------- | ------------------------------------------- |
| **LangGraph**    | State graph                       | Agent with variables                        |
|                  | Nodes                             | A playbook to represent a sequence of nodes |
|                  | Edges                             | Control flow in Steps                       |
|                  | State                             | Agent variables (`$variable`)               |
|                  | Tools                             | Python playbooks or MCP server              |
| **CrewAI**       | Crew                              | Multi-agent Playbooks program file          |
|                  | Agent roles                       | H1 agent definitions                        |
|                  | Tasks                             | H2 playbook definitions                     |
|                  | Tools                             | Python playbooks or MCP server              |
|                  | Process (sequential/hierarchical) | Triggers and control flow                   |
| **AutoGen**      | Agents                            | H1 agent definitions                        |
|                  | Conversations                     | Conversation loop in a playbook             |
|                  | Function calling                  | Python playbooks                            |
|                  | Group chat                        | Multi-party meetings                        |
| **LangChain**    | Agent                             | H1 agent definition                         |
|                  | Tools                             | Python playbooks or MCP server              |
|                  | ReAct agent                       | ReAct-type playbook                         |
|                  | Memory                            | Artifacts or variables                      |
|                  | Chains                            | Playbook Steps                              |

### Step 4: Test and Iterate

Run your Playbooks agent:

```bash
# export ANTHROPIC_API_KEY=<your Anthropic API key here>
# make sure python --version is 3.12+
cd playbooks
playbooks run <agent>.pb
```

Compare behavior with the original implementation and iterate.

______________________________________________________________________

## Next steps

- **Learn the language**: [Programming Guide](../../programming-guide/) - Comprehensive guide to writing effective Playbooks programs
- **Hands-on learning**: [Tutorials](../../tutorials/) - Step-by-step examples
- **Deep dive**: [Reference Documentation](../../reference/) - Detailed technical information

______________________________________________________________________

Happy migrating! 🚀
