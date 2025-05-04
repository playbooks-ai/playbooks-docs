# Anatomy of a Playbook

In this tutorial, you'll learn about the structure of a basic Playbooks AI program and understand the components that make up a playbook.

## Objective

By the end of this tutorial, you'll understand:

- The basic structure of a markdown playbook
- How to define a playbook with steps
- How triggers control playbook execution
- How to create and run a simple "Hello World" playbook

## Prerequisites

- [Playbooks AI installed](../get-started/installation.md)
- Basic familiarity with markdown

## The Structure of a Playbook

A Playbooks AI program consists of one or more playbooks written in markdown format. Let's break down the structure of a basic "Hello World" playbook:

```markdown
# Hello world
This is a hello world demo for the playbooks system

## Hello world demo
This playbooks demo prints a hello playbooks message

### Triggers
- At the beginning

### Steps
- Greet the user with a hello playbooks message
- Tell the user that this is a demo for the playbooks system
- Say goodbye to the user
- End program
```

Let's examine each part:

### 1. Program Title and Description

```markdown
# Hello world
This is a hello world demo for the playbooks system
```

- The top-level heading (`#`) defines the program title
- The text immediately following defines the program description

### 2. Playbook Definition

```markdown
## Hello world demo
This playbooks demo prints a hello playbooks message
```

- Second-level headings (`##`) define individual playbooks within the program
- The text immediately following describes what this playbook does

### 3. Triggers Section

```markdown
### Triggers
- At the beginning
```

- The "Triggers" section (denoted by `### Triggers`) defines when this playbook should execute
- In this example, `At the beginning` means this playbook will run as soon as the program starts

### 4. Steps Section

```markdown
### Steps
- Greet the user with a hello playbooks message
- Tell the user that this is a demo for the playbooks system
- Say goodbye to the user
- End program
```

- The "Steps" section (denoted by `### Steps`) defines what the playbook should do
- Each bullet point (`-`) represents a discrete step in natural language
- Steps are executed in the order they are listed
- The last step `End program` terminates the program execution

## Creating Your First Playbook

Let's create your first playbook:

1. Create a new file named `hello.md` with the following content:

```markdown
# Hello world
This is a hello world demo for the playbooks system

## Hello world demo
This playbooks demo prints a hello playbooks message

### Triggers
- At the beginning

### Steps
- Greet the user with a hello playbooks message
- Tell the user that this is a demo for the playbooks system
- Say goodbye to the user
- End program
```

2. Run your playbook:

```bash
python -m playbooks.applications.agent_chat hello.md --verbose
```

3. You should see output similar to:

```
Loading playbooks from: ['hello.md']
Transpiled playbook content

╭─ HelloWorld ───────────────────────────────────────────────────╮
│ Hello! Welcome to Playbooks AI!                                │
│                                                                │
│ This is a demonstration of the Playbooks system, which allows  │
│ you to create AI agents using natural language programming.    │
│                                                                │
│ Thank you for trying out this demo. Goodbye!                   │
╰────────────────────────────────────────────────────────────────╯
Execution finished. Exiting...
```

## Understanding the Execution

When you run the playbook:

1. The Playbooks AI framework loads and parses your markdown file
2. It transpiles the natural language into an executable format
3. It identifies playbooks with triggers that match the current state (in this case, "At the beginning")
4. It executes the steps in order, generating appropriate responses for each step
5. When it reaches the "End program" step, execution terminates

## Variables in Playbooks

Playbooks can also use variables to store and manipulate data. Variables are denoted with a `$` prefix. We'll explore variables in more detail in later tutorials.

## Best Practices

When creating playbooks:

- Give your playbooks descriptive titles that explain their purpose
- Break complex processes into multiple playbooks with clear responsibilities
- Use clear, concise natural language for your steps
- Use triggers to control when playbooks execute
- End your program explicitly with the "End program" step

## Exercises

1. Modify the "Hello World" playbook to ask for the user's name and include it in the greeting
2. Create a playbook that tells a short joke or story
3. Try creating a playbook with multiple sets of steps and see what happens

## Next Steps

Now that you understand the basic structure of a playbook, you're ready to learn about [Adding Triggers](adding-triggers.md) to control when your playbooks execute. 