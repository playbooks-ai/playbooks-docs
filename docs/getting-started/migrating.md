# Migrating from Other Agent Frameworks

If you're coming from other agent frameworks like LangGraph, CrewAI, or AutoGen, you can use AI coding assistants to help translate your existing agent implementations into idiomatic Playbooks code. This guide shows you how. You can expect 60-90% reduction in code size and significant reduction in complexity.

---

## Why Migrate to Playbooks?

- **10x less code**: Eliminate boilerplate and framework complexity
- **Natural language first**: Write agent behavior in plain English
- **Soft + hard logic**: Seamlessly mix LLM reasoning with deterministic Python
- **Verifiable execution**: Compiled to auditable PBAsm for debugging
- **First principles**: Built from the ground up for the LLM era (Software 3.0)

---

## Supported Source Frameworks

Playbooks can express the same agent behaviors as these popular frameworks:

1. **[LangGraph](https://langchain-ai.github.io/langgraph/)** - State graph-based agents from LangChain
2. **[CrewAI](https://www.crewai.com/)** - Multi-agent collaboration framework
3. **[AutoGen](https://microsoft.github.io/autogen/)** - Microsoft's multi-agent conversation framework
4. **[LangChain Agents](https://python.langchain.com/docs/modules/agents/)** - Classic LangChain agent implementations
5. **[Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/)** - Microsoft's AI orchestration SDK
6. **[Haystack](https://haystack.deepset.ai/)** - NLP framework with agent capabilities
7. **[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** - Autonomous agent framework

---

## AI Coding Assistants

These AI coding assistants can help you migrate your agent code to Playbooks:

1. **[Cursor](https://cursor.com/)** - AI-first code editor (VS Code fork)
2. **[Windsurf](https://codeium.com/windsurf)** - AI-native IDE by Codeium
3. **[GitHub Copilot](https://github.com/features/copilot)** - Most widely adopted AI pair programmer
4. **[Devin](https://devin.ai/)** - Cognition's autonomous AI software engineer
5. **[OpenAI Codex](https://openai.com/index/introducing-codex/)** - GPT-5-Codex powered autonomous coding agent
6. **[Amazon Q Developer](https://aws.amazon.com/q/developer/)** - AWS-integrated coding assistant (formerly CodeWhisperer)
7. **[Google Gemini Code Assist](https://cloud.google.com/gemini/docs/codeassist/overview)** - Google Cloud's AI coding tool

---

## Migration Instructions

1. git clone the source agent implementation and open it in your favorite IDE
2. Create a `playbooks` folder in the root of the project where you will create the converted Playbooks program
3. Provide these instructions to the AI coding assistant

    ```
    You are a Playbooks programmer. Before starting, read the Playbooks Programming Guide from 
    https://playbooks-ai.github.io/playbooks-docs/programming-guide/index.md first. 

    Key principles:
    - Write minimal, optimal, idiomatic Playbooks programs
    - Use Markdown playbooks for structured workflows
    - Use Python playbooks for deterministic logic and external APIs
    - Use ReAct playbooks for dynamic research and reasoning
    - Extract 4+ Python playbooks into MCP servers
    - Sparingly use triggers for event-driven behavior and multi-agent communication for collaboration
    - Prefer natural language over explicit syntax
    - Think from first principles: LLMs as CPUs, Software 3.0

    Produce a MIGRATION.md file with code size comparison and instructions on how to run the Playbooks program (note Playbooks requires Python 3.12+ and ANTHROPIC_API_KEY environment variable).

    ====

    Convert the <agent>.py agent implementation to playbooks program at playbooks/<agent>.pb. Create all new files in the playbooks/ folder.
    ```

    Replace <agent> with the name of the source agent.

4. Let the coding assistant cook! It will create the playbooks/<agent>.pb file, potentially with other files like an MCP server, a README.md file, and a requirements.txt file, etc.
5. Review the generated code and make any necessary adjustments
6. Start the MCP server, if applicable
7. Run the Playbooks program to ensure it works as expected
---

## Configuration for Each AI Assistant

### Cursor

**Method 1: Using .cursorrules file**

Create a `.cursorrules` file in your project root with the instructions above.

**Method 2: Using Cursor Settings**

1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Search for "Rules for AI"
3. Add the instructions above to the "Rules for AI" text area

---

### Windsurf

Create a `.windsurfrules` file in your project root with the instructions above.


---

### GitHub Copilot

**Using workspace instructions (.github/copilot-instructions.md)**

Create `.github/copilot-instructions.md` with the instructions above.

---

## agents.md Format

Many AI coding assistants support the [agents.md](https://agents.md/) format. Create an `agents.md` file in your project root with the instructions above.
