# Writing Playbooks with AI Coding Assistants

AI coding assistants can significantly accelerate Playbooks development by understanding natural language instructions and generating idiomatic code. This guide shows you how to configure your AI assistant for optimal Playbooks programming.

---

## Why Use AI Assistants for Playbooks?

- **Natural language understanding**: AI assistants excel at translating intent into Playbooks' natural language syntax
- **Best practices enforcement**: Properly configured assistants follow Playbooks conventions and patterns
- **Faster development**: Generate boilerplate, suggest playbook decomposition, and write idiomatic code
- **Learning aid**: See how experienced Playbooks programmers would structure your agents

---

## Supported AI Coding Assistants

1. **[Cursor](https://cursor.com/)** - AI-first code editor (VS Code fork)
2. **[Windsurf](https://codeium.com/windsurf)** - AI-native IDE by Codeium
3. **[GitHub Copilot](https://github.com/features/copilot)** - Most widely adopted AI pair programmer
4. **[Devin](https://devin.ai/)** - Cognition's autonomous AI software engineer
5. **[OpenAI Codex](https://openai.com/index/introducing-codex/)** - GPT-5-Codex powered autonomous coding agent
6. **[Amazon Q Developer](https://aws.amazon.com/q/developer/)** - AWS-integrated coding assistant (formerly CodeWhisperer)
7. **[Google Gemini Code Assist](https://cloud.google.com/gemini/docs/codeassist/overview)** - Google Cloud's AI coding tool

---

## Prompt for AI Coding Assistants

Use these instructions with any AI coding assistant to ensure it generates optimal Playbooks code:

```
You are a Playbooks programmer. Download and read the Playbooks Programming Guide from 
https://playbooks-ai.github.io/playbooks-docs/programming-guide/index.md first.

When you have read and understood, just say "Ready"
```

---

## Configuration by Assistant

### Cursor

**Method 1: Using .cursorrules file**

Create a `.cursorrules` file in your project root with the instructions above.

**Method 2: Using Cursor Settings**

1. Open Cursor Settings (`Cmd/Ctrl + ,`)
2. Search for "Rules for AI"
3. Add the instructions above to the "Rules for AI" text area

---

### Windsurf

Create a `.windsurfrules` file in your project root with the instructions above.

---

### Claude Code

Create a `CLAUDE.md` file in your project root with the instructions above.

---

### GitHub Copilot

**Using workspace instructions (.github/copilot-instructions.md)**

Create `.github/copilot-instructions.md` with the instructions above.


---

### Devin / OpenAI Codex / Amazon Q / Gemini Code Assist


For autonomous or chat-based AI assistants, include the instructions in your initial prompt

---

## agents.md Format

Many AI coding assistants support the [agents.md](https://agents.md/) format for project-level AI configuration.

Create an `agents.md` file in your project root:

    # Playbooks Project Configuration

    ## Identity

    You are a Playbooks programming expert. Your role is to help developers write minimal, optimal, and idiomatic Playbooks programs following Software 3.0 principles.

    ## Context

    Playbooks is a framework where:
    - LLMs act as CPUs executing natural language instructions
    - Programs are up to 10x smaller than traditional agent frameworks
    - Soft logic (LLM reasoning) and hard logic (Python) run on the same call stack
    - Code compiles to verifiable PBAsm (Playbooks Assembly Language) for debugging

    ## Instructions

    1. **Always start by reading**: https://playbooks-ai.github.io/playbooks-docs/programming-guide/index.md
    2. **Follow the programming guide** for syntax, patterns, and best practices
    3. **Think from first principles**: How would this agent behave naturally?
    4. **Choose the right playbook types**:
    - Markdown playbooks for known workflows with explicit steps
    - Python playbooks for deterministic logic and external API calls
    - ReAct playbooks for dynamic reasoning and research tasks
    - MCP servers when you have 4+ Python playbooks
    1. **Prefer natural language** over explicit syntax unless clarity demands it
    2. **Write minimal code** - remove all unnecessary boilerplate
    3. **Explain architectural choices** to help developers learn

---

## Best Practices

### 1. Start with High-Level Intent

Instead of:
```
Create a function that calls an API and processes the response
```

Try:
```
Build a Playbooks agent that:
- Takes user's location
- Fetches weather data
- Provides personalized recommendations
- Handles errors gracefully
```

### 2. Ask for Explanations

Request that the AI explain its choices:
```
Build this agent and explain:
- Why you chose each playbook type
- When MCP extraction would be beneficial
- How the control flow works
```

### 3. Iterate Based on Behavior

Test the generated code and provide feedback:
```
The agent works but feels too rigid. Make it more conversational
while maintaining the same logic.
```

### 4. Request Idiomatic Patterns

```
Rewrite this to be more idiomatic Playbooks code. Use natural language
where possible and follow Software 3.0 principles. Leverage Playbooks capabilities optimally.
```

---

## Common Tasks

### Create a New Agent

```
I need a [customer support / data analysis / research] agent that [capabilities].
```

### Add a New Playbook

```
Add a playbook to my agent that [specific task]. Choose the right type
(Markdown/Python/ReAct) based on the task requirements.
```

### Extract to MCP Server

```
I have 5+ Python playbooks in this agent. Extract them to an MCP server
following Playbooks best practices.
```

### Debug Behavior

```
This agent isn't behaving as expected: [description of issue].
Review the code and suggest fixes following Playbooks conventions.
```

### Optimize for Conciseness

```
This agent works but the code is verbose. Refactor to be more concise
while maintaining clarity.
```

---

## Next Steps

- **Get started**: [Install Playbooks](index.md) and create your first agent
- **Learn patterns**: Study the [Programming Guide](../programming-guide/index.md)
- **Migrate existing code**: See [Migrating from Other Frameworks](migrating.md)
- **Explore examples**: Browse [Tutorials](../tutorials/index.md)

---

Happy building with AI! 🤖🚀

