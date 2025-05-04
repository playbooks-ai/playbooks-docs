# Quickstart

This quickstart guide will help you create and run your first Playbooks AI program. By the end, you'll have a simple interactive program that asks for your name and provides a personalized greeting.

## Prerequisites

Before you begin, make sure you have:

- Installed Playbooks AI (see the [Installation Guide](installation.md))
- An API key for either Anthropic (Claude) or OpenAI (GPT-4)

## Step 1: Set Up Your Environment

First, you need to set up your environment variables to authenticate with the LLM provider of your choice.

Create a `.env` file in your text editor and configure your API key and model:

```
# For Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here
MODEL=claude-3-7-sonnet-latest

# OR for OpenAI
# OPENAI_API_KEY=your_openai_api_key_here
# MODEL=gpt-4o
```

Make sure to uncomment the appropriate API key and model for the service you're using, and replace the placeholder with your actual API key.

## Step 2: Create Your First Playbooks program

Create a new file named `hello.md` with the following content:

```markdown
# Personalized greeting
This program greets the user by name

## Greet
## Triggers
- At the beginning
## Steps
- Ask the user for their name
- Say hello to the user by name and welcome them to Playbooks AI
- End program
```

This simple Playbooks program:

- Defines a "Personalized greeting" agent
- Defines a "Greet" playbook that triggers at the beginning of program execution
- Specifies steps to ask for the user's name and respond with a personalized greeting

## Step 3: Run Your Playbooks program

Now, run your program:

```bash
python src/playbooks/applications/agent_chat.py hello.md --verbose

# or

playbooks hello.md --application AgentChat --verbose
```

You should see output similar to:

```
Loading playbooks from: ['hello.md']
Transpiled playbook content

╭─ PersonalizedGreeting ────╮
│ Hello! What is your name? │
╰───────────────────────────╯

User: hey, my name is Amol

╭─ PersonalizedGreeting ───────────────╮
│ Hello Amol! Welcome to Playbooks AI. │
╰──────────────────────────────────────╯
Execution finished. Exiting...
```

Congratulations! You've successfully run your first Playbooks program.

## Understanding What's Happening

Let's break down what happened:

1. The Playbooks AI framework loaded your markdown file and transpiled it into an executable format
2. The AgentChat application was launched, which provides a simple command-line chat interface
3. The application started executing the program
4. The playbook with the "At the beginning" trigger was automatically executed
5. The agent followed the steps defined in your playbook:
   - Asked for your name
   - Processed your response
   - Generated a personalized greeting
   - Ended the program

## Next Steps

Now that you've run your first playbook, you can:

- Go through the [tutorials](/tutorials)
- Learn about [Triggers](../triggers/index.md) for more advanced event-based programming
- Learn how to create [multi-agent systems](/agents/multi-agents.md)
