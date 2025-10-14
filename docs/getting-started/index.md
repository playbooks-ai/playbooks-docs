# 10 mins to your first AI Agent

:warning: Playbooks requires Python 3.12+.

:warning: Playbooks requires [Anthropic API key](https://console.anthropic.com/settings/keys) to run. See [Models](../reference/models.md) for more information on supported models.

## (3 mins) Install Playbooks

To get started with Playbooks AI, you need to install the `playbooks` package using pip, poetry, or your favorite Python package manager.

```
pip install playbooks
```

## (5 mins) Create Your First Playbooks program

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

This simple Playbooks program:

- Defines a "Greeting" agent
- Defines a "Greet" playbook that triggers at the beginning of program execution
- Specifies steps to ask for the user's name and engage in a conversation till user provides name without being pushy, welcome them to Playbooks AI, share a tasteful stand-up comedy bit incorporating the user, and end program

## (2 mins) Run the program

```bash
export ANTHROPIC_API_KEY=<your Anthropic API key here>
playbooks run hello.pb
```

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

## Next Steps

- Learn how to write effective Playbooks programs with the [Programming Guide](../programming-guide/index.md)
- If you're coming from LangGraph, CrewAI, or other frameworks, check out [Migrating from Other Frameworks](migrating.md)
- Explore [Tutorials](../tutorials/index.md) for hands-on examples
- Browse the [Reference Documentation](../reference/index.md) for detailed information