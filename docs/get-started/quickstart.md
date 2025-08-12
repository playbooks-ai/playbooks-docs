# Quickstart

This quickstart guide will help you create and run your first Playbooks AI program. By the end, you'll have a simple interactive program that asks for your name and provides a personalized greeting.

## Prerequisites

Before you begin, make sure you have:

- Installed Playbooks AI (see the [Installation Guide](installation.md))
- An API key for Anthropic (Claude Sonnet 4.0) or another supported provider

## Step 1: Set Up Your Environment

First, you need to set up your environment variables to authenticate with Anthropic.

Create a `.env` file in your project root (the directory where you run CLI commands) and configure your API key and model:

```
# For Anthropic (Claude Sonnet 4.0)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
MODEL=claude-sonnet-4-20250514

# Cache LLM responses to disk
LLM_CACHE_TYPE="disk"
LLM_CACHE_ENABLED="true"
LLM_CACHE_PATH=".llm_cache" # for disk cache

# Langfuse (optional)
# LANGFUSE_SECRET_KEY="sk-lf-..."
# LANGFUSE_PUBLIC_KEY="pk-lf-..."
# LANGFUSE_HOST="http://localhost:3000"
```

Make sure to replace the placeholder with your actual API key.

:warning: Claude Sonnet 4.0 is the only LLM currently supported by Playbooks. Other frontier LLMs may work and can be selected by setting `MODEL` and the appropriate provider API key (see Reference > Configuration). The performance of other LLMs is not guaranteed.

### VSCode Support (optional)

For the best development experience, consider setting up VSCode with debugging support. See the [Installation Guide](installation.md#vscode-debugging-support) for instructions on installing the **Playbooks Language Support** extension, which provides debugging capabilities for your playbooks programs.

### Langfuse (optional)
You can specify Langfuse credentials for tracing the execution of your Playbooks programs. For developement environment, we recommend using the [docker compose setup for Langfuse](https://langfuse.com/self-hosting/docker-compose). After following these instructions, launch Langfuse at http://localhost:3000, create a new organization and project, and create a new secret key and public key to enable tracing.

## Step 2: Create Your First Playbooks program

Create a new file named `hello.pb` with the following content:

```markdown
# Personalized greeting
This program greets the user by name

## Greet
### Triggers
- At the beginning of the program
### Steps
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
playbooks run hello.pb
```

You should see output similar to:

```
Loading playbooks from: ['hello.pb']
Compiling hello.pb

PersonalizedGreeting: Hello! What's your name?

User: Amol

PersonalizedGreeting: Hello Amol! Welcome to Playbooks AI. I'm excited to help you explore what we can do together!


Execution finished, exiting...
Agent PersonalizedGreeting(agent 1000) stopped
```

Congratulations! You've successfully run your first Playbooks program.

### Alternative: Run with web server + playground

If you prefer a web UI:

1. Start the web server: `python -m playbooks.applications.web_server`
2. Open the HTML Playground and point it to your `hello.pb` (see Applications > HTML Playground)

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

### Optional: Compile to Playbooks Assembly

You can compile your program to `.pbasm` for inspection or to skip compilation at run time:

```bash
playbooks compile hello.pb --output hello.pbasm
```

Run a compiled program with the same agent chat application:

```bash
playbooks run hello.pbasm
```

## Next Steps

Now that you've run your first playbook, you can:

- Go through the [tutorials](../tutorials/index.md)
- Learn about [Triggers](../triggers/index.md) for more advanced event-based programming
- Learn how to create [multi-agent systems](../agents/index.md)
 - Explore [Markdown vs ReAct vs Raw Prompt](../playbook-types/index.md)
