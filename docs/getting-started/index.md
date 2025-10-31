# Build Your First AI Agent in 10 Minutes

Welcome to Playbooks! In this quickstart, you'll build your first AI agent that greets users with natural language programming.

## Prerequisites

Before you begin:

- **Python 3.12+** is required
- **Anthropic API key** - Get yours at [console.anthropic.com](https://console.anthropic.com/settings/keys)
- See [Models](../reference/models.md) for information on other supported LLM providers

## Install Playbooks

Install the `playbooks` package using pip, poetry, or your preferred Python package manager:

```bash
pip install playbooks
```

## Create Your First Playbooks Program

Create a new file named `hello.pb` with the following content:

```markdown linenums="1"
# Greeting agent
This agent welcomes user to Playbooks AI, the world's first Software 3.0 tech stack.

## Greet
### Triggers
- At the beginning of the program
### Steps
- Ask the user for their name and engage in a conversation till user provides name without being pushy
- Welcome them to Playbooks AI
- Share a tasteful stand-up comedy bit incorporating the user
- End program
```

### Understanding the Program

This simple 11-line Playbooks program demonstrates the core concepts:

- **Agent definition** (line 1-2): Describes what the agent does
- **Playbook** (line 4): Named workflow that can be triggered and called
- **Triggers** (line 5-6): When the playbook should run (at program start)
- **Steps** (line 7-11): Natural language instructions executed by the LLM

Notice how readable this is – business users can understand exactly what the agent will do without knowing any code!

## Run the Program

Set your API key and run the program:

```bash
export ANTHROPIC_API_KEY=<your Anthropic API key here>
playbooks run hello.pb
```

The Playbooks runtime will:

1. **Compile** your `.pb` file to Playbooks Assembly Language (`.pbasm`)
2. **Load** the compiled program
3. **Execute** the steps, with the LLM following your natural language instructions
4. **Handle** the conversation interactively in your terminal

### Expected output
YMMV, but here's how it went for me. BTW, I take no responsibility for the AI's weak sense of humor:

```text
ℹ Loading playbooks from: ['hello-playbooks.pb']
  Compiling agent: Greeting agent

GreetingAgent: Hello there! Welcome to Playbooks AI - the world's first Software 3.0 tech stack! I'm excited to meet you. What's your name? I'd love to get to know you a bit!

User: how areyou

GreetingAgent: I'm doing wonderfully, thank you for asking! I'm really excited to be here helping people discover the amazing world of Playbooks AI. But I'm curious about you - I'd still love to know your name so I can give you a proper welcome! What should I call you?

User: what's in a name

GreetingAgent: Ah, a fellow philosopher! You're absolutely right - Shakespeare said 'What's in a name? That which we call a rose by any other name would smell as sweet.' But here's the thing - while a rose would still be beautiful, I'd love to know what to call YOU so our conversation feels more personal and warm. Even if it's just a nickname or what you'd like me to call you - anything works! What do you say?

User: ah sure, but first, what is your name

GreetingAgent: Fair enough! I'm GreetingAgent - though you can call me Greety if you'd like something more casual. I'm here to welcome folks to the amazing world of Playbooks AI and make sure everyone feels at home. Now that we've been properly introduced on my end, what should I call you? I promise the welcome will be worth it!

User: My name is Amol

GreetingAgent: Wonderful to meet you, Amol! Welcome to Playbooks AI - you're about to experience something truly revolutionary. This is the world's first Software 3.0 tech stack, where natural language becomes executable code and AI agents work together seamlessly. You're at the forefront of the future of software development!

GreetingAgent: So Amol walks into Playbooks AI... and the system says 'Welcome! You look like someone who's ready to revolutionize software!' Amol replies, 'How can you tell?' The system says, 'Well, you're here talking to an AI that just executed english instructions like a program - that's either revolutionary thinking or you're really lost!' But seriously Amol, you've got great timing - you're witnessing the birth of Software 3.0 where even my jokes are technically part of the program execution!
```

## What You Just Built

You've created a working AI agent using natural language programming. Here's what makes this different:

- **High-level thinking**: You described what the agent should do, not how to do it. No orchestration code, just behavior specification.
- **Natural exception handling**: The LLM will handle edge cases gracefully without explicit code for every contingency.
- **Readable by everyone**: Stakeholders can review and approve the agent's behavior directly - it's just natural language.
- **Verifiable execution**: Unlike prompt engineering, the runtime guarantees your steps execute in order. You can debug with breakpoints in VSCode.

## What's Next

<div class="grid cards" markdown>

- :material-book-open-variant: **Programming Guide**
  
    Learn the Playbooks language and framework
    
    [Read the guide →](../programming-guide/index.md)

- :material-school: **Tutorials**
  
    Build real agents with step-by-step examples
    
    [Try the tutorials →](../tutorials/index.md)

- :material-play: **vs Traditional Frameworks**
  
    See how Playbooks differs from LangGraph, CrewAI, AutoGen
    
    [Compare approaches →](../reference/playbooks-traditional-comparison.md)

- :material-microsoft-visual-studio-code: **Using AI Coding Assistants**
  
    Write Playbooks programs using Claude, Cursor, or GitHub Copilot
    
    [Configure assistants →](ai-assistants.md)

- :material-swap-horizontal: **Migrating from Other Frameworks**
  
    Convert existing agents to Playbooks
    
    [Migration guide →](migrating.md)

- :material-code-json: **Reference**
  
    Complete technical documentation
    
    [Browse docs →](../reference/index.md)

</div>