# LLM is your new CPU Welcome to Software 3.0

**Build multi‑agent AI systems** with ease with Python code running on CPU and **natural language code running on LLM**.

Stop writing prompts and hoping that the LLM will follow them faithfully. Instead, get **verifiable natural language program execution** with Playbooks.

Playbooks is an innovative framework for building and executing AI agents using "playbooks" – structured workflows defined in natural language and Python code. Created by [Amol Kelkar](https://www.linkedin.com/in/amol-kelkar/), the framework is part of the world's first Software 3.0 tech stack, Playbooks AI. It includes a **new programming language** (markdown-formatted .pb files) that are compiled to Playbooks Assembly Language (.pbasm files), that are then executed by the Playbooks Runtime.

Unlike other AI agent frameworks, **Playbooks programs are highly readable**. Business users can understand, change, and approve agent behavior specified in natural language; while developers benefit from the flexibility of running Python code on CPU and natural lanuage code on LLM, on the same call stack, and with full observability and control.

______________________________________________________________________

Here is an example Playbooks program. It contains both Python and natural language "playbooks", i.e. functions. Notice how natural language playbook `Main` (line 4) calls (line 13) a Python playbook `process_countries` (line 20), which in turn calls (line 23) a natural language playbook `GetCountryFact` (line 27).

Here is **country-facts.pb**, an example Playbooks program. This **29 line, highly readable Playbooks program** accomplishes the same task as implementations that are [significantly longer and more complex using traditional agent frameworks](reference/playbooks-traditional-comparison/).

````markdown
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
````

## GetCountryFact($country)

### Steps

- Return an unusual historical fact about $country

````

## Try out Playbooks in 10 minutes

You will need Python 3.12+ and your Anthropic API key.

### 1. Install Playbooks

```text
pip install playbooks
````

### 2. Run example program

Use one of the following methods -

#### a. Playbooks CLI

```bash
ANTHROPIC_API_KEY=sk-ant-... playbooks run country-facts.pb
```

#### b. Playbooks Playground

```bash
ANTHROPIC_API_KEY=sk-ant-... playbooks playground
```

Put your program path and click "Run Program". You can turn on "Execution Logs" to see the program execution details.

#### c. Python API

```python
from playbooks import Playbooks

pb = Playbooks(["country-facts.pb"]) # absolute or relative path
await pb.initialize()
await pb.program.run_till_exit()
```

### 3. Step debugging in VSCode (Optional)

Install the **Playbooks Language Support** extension for Visual Studio Code:

1. Open VSCode
1. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
1. Search for "Playbooks Language Support"
1. Click Install

The extension provides debugging capabilities for playbooks programs, making it easier to develop and troubleshoot your AI agents. Once the plugin is installed, you can open a playbooks .pb file and start debugging!

## Let's build something amazing with Playbooks!

- **Quickstart** - your first playbook\
  [Start here →](getting-started/)
- **Tutorials** - learn by doing\
  [How it works →](tutorials/)
- **Playbooks vs Traditional Frameworks** - see the difference\
  [Compare approaches →](reference/playbooks-langgraph-comparison.md)
