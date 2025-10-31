---
hide:
  - toc
---
<div align="center">
   <h1>
   <picture>
      <img alt="Playbooks AI" src="assets/images/playbooks-logo-dark.png#gh-dark-mode-only" width=200 height=200>
      <img alt="Playbooks AI" src="assets/images/playbooks-logo.png#gh-light-mode-only" width=200 height=200>
   </picture>
  <h2 align="center">LLM is your new CPU<br/>Welcome to Software 3.0</h2>
</div>

> **Playbooks is a framework and runtime for building verifiable multi-agent AI systems with Natural Language Programs.**

Describe what your agents should do, not how to do it. Focus on agent behavior at a high level while the LLM handles implementation details and edge cases. Mix natural language and Python seamlessly on the same call stack. Get verifiable execution, full observability, and programs that business users can actually read and approve.

Here's a complete **29-line Playbooks program** that orchestrates natural language and Python code together. Notice how the `Main` playbook (line 4) calls Python function `process_countries` (line 20), which then calls natural language playbook `GetCountryFact` (line 27).
````markdown linenums="1" title="country-facts.pb"
# Country facts agent
This agent prints interesting facts about nearby countries

## Main
### Triggers
- At the beginning
### Steps
- Ask user what $country they are from
- If user did not provide a country, engage in a conversation and gently nudge them to provide a country
- List 5 $countries near $country
- Tell the user the nearby $countries
- Inform the user that you will now tell them some interesting facts about each of the countries
- process_countries($countries)
- End program

```python
from typing import List

@playbook
async def process_countries(countries: List[str]):
    for country in countries:
        # Calls the natural language playbook 'GetCountryFact' for each country
        fact = await GetCountryFact(country)
        await Say("user", f"{country}: {fact}")
```

## GetCountryFact($country)
### Steps
- Return an unusual historical fact about $country
````

This accomplishes the same task as implementations that are [significantly longer and more complex using traditional agent frameworks](reference/playbooks-traditional-comparison.md#traditional-framework-implementation-272-lines).

## What is Software 3.0?

Software 3.0 is the evolution from hand-coded algorithms (Software 1.0) and learned neural network weights (Software 2.0) to **natural language as the primary programming interface**. 

In Playbooks, you write programs in human language that execute directly on large language models. The LLM acts as a semantic CPU that interprets and runs your instructions. Instead of translating business logic into formal code syntax or training models on data, you describe what you want in natural language, mix it seamlessly with Python when needed, and get verifiable, observable execution. 

This changes how you build AI systems: business stakeholders can read and approve the actual program logic, AI systems become transparent rather than black boxes, and sophisticated agent behaviors become accessible without sacrificing control or understanding.


## Why Playbooks?

**:material-brain: Think at a Higher Level**
: Focus on what your agent should do, not implementation mechanics. Define complex, nuanced behaviors without getting lost in orchestration details. The framework handles the low-level execution.

**:material-auto-fix: Natural Exception Handling**
: The LLM handles edge cases and exceptional conditions smoothly without explicit code for every contingency. Your agents adapt to unexpected situations naturally.

**:material-sitemap: Powerful Abstractions**
: Multi-agent meetings for complex coordination. Triggers for event-driven behavior. Seamless mixing of natural language and Python. Abstractions that would take hundreds of lines in other frameworks are built-in.

**:material-eye-check: Readable by Everyone**
: Business stakeholders can read and approve the actual program logic. No more "black box" AI systems. What you write is what executes.

**:material-shield-check: Verifiable & Observable**
: Unlike prompt engineering where you hope the LLM follows instructions, Playbooks guarantees verifiable execution. Step debugging in VSCode, detailed execution logs, full observability.


## Get Started in 10 Minutes

Build your first AI agent with Playbooks. You'll need Python 3.12+ and an [Anthropic API key](https://console.anthropic.com/settings/keys).

### Install Playbooks

```bash
pip install playbooks
```

### Create and Run Your First Agent

Create a file `hello.pb`:

```markdown
# Greeting agent
This agent welcomes users to Playbooks AI

## Greet
### Triggers
- At the beginning of the program
### Steps
- Ask the user for their name
- Welcome them to Playbooks AI, the world's first Software 3.0 tech stack
- End program
```

Run it:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
playbooks run hello.pb
```

That's it! You've just built and run your first AI agent with natural language programming.

### Run the Country Facts Example

Try the more advanced example from above:

```bash
playbooks run country-facts.pb
```

You can also use the **Playground** for interactive development:

```bash
playbooks playground
```

The Playground provides a visual interface to run programs, view execution logs, and iterate quickly.

### Step Debugging in VSCode

For production development, install the **Playbooks Language Support** extension:

1. Open VSCode Extensions (Ctrl+Shift+X / Cmd+Shift+X)
2. Search for "Playbooks Language Support"
3. Click Install

Now you can set breakpoints and step through your agent's execution, just like traditional code!

## Learn More

<div class="grid cards" markdown>

- :material-rocket: **Quickstart Guide**
  
    Build your first agent
    
    [Get started →](getting-started/index.md)

- :material-book-open-variant: **Programming Guide**
  
    Learn the Playbooks language and framework
    
    [Read the guide →](programming-guide/index.md)

- :material-school: **Tutorials**
  
    Build real agents with step-by-step examples
    
    [Try the tutorials →](tutorials/index.md)

- :material-play: **vs Traditional Frameworks**
  
    See how Playbooks compares to LangGraph, CrewAI, AutoGen
    
    [Compare approaches →](reference/playbooks-traditional-comparison.md)

- :material-code-json: **Reference**
  
    Complete technical documentation
    
    [Browse docs →](reference/index.md)

- :material-microsoft-visual-studio-code: **Using AI Coding Assistants**
  
    Write Playbooks programs using Claude, Cursor, or GitHub Copilot
    
    [Configure assistants →](getting-started/ai-assistants.md)

</div>
