---
hide:
  - toc
---

<div style="text-align: center;">
  <div class="centered-logo-text-group">
    <h1>
    <img src="assets/images/playbooks-logo.png" alt="Playbooks AI" style="width: 200px; height: 200px;">
    </h1>
  </div>
</div>

## What is Playbooks AI?

Playbooks AI is a novel framework for **building AI agents using Natural Language Programming**. 

- A new "english-like", semantically interpreted programming language
- Runtime for reliable, auditable and verifiable execution
- Seamless composition of complex workflows across natural language and Python

<div class="install-command-container">
  <p style="text-align:center;">
    Get started:
    <br/>
    <code>pip install playbooks</code>
  </p>
</div>

<p style="text-align:center;">
  <a href="get-started/quickstart/" class="md-button" style="margin:3px">Quickstart</a>
  <a href="tutorials/" class="md-button" style="margin:3px">Tutorials</a>
  <!-- <a href="api-reference/" class="md-button" style="margin:3px">API Reference</a> -->
  <a href="playbooks-language/" class="md-button" style="margin:3px">Playbooks Language</a>
</p>

---

## Learn more

<div class="grid cards" markdown>

-   :material-language-markdown: **Natural Language Programming**

    ---

    Create AI agents using natural language, with Markdown playbooks for step-by-step instructions,
    suitable for prescribed business processes. Mix prescribed workflows with dynamic planning.

    [**Learn about Playbooks Language**](playbooks-language/index.md)

-   :material-code-braces: **Python Integration**

    ---

    Turn any async Python function into a playbook with the `@playbook` decorator. Call other playbooks
    (including natural language playbooks) from Python and vice versa.

    [**Explore Python Playbooks**](playbook-types/python-playbooks.md)

-   :material-account-group: **Multi-Agent Architecture**

    ---

    Natively support multi-agent systems with agent-to-agent calls and messaging. Enable natural language 
    message passing and multi-turn dialogue between agents with direct playbook invocation.

    [**Discover Multi-Agent Systems**](tutorials/multi-agent-programming.md)

-   :material-bell-ring: **Event-Driven Programming**

    ---

    Use triggers for declarative event-driven programming. Playbooks are dynamically invoked when specified 
    conditions are met, including temporal, state-based, execution flow, user interaction, and external events.

    [**Explore Triggers**](triggers/index.md)

-   :material-magnify-scan: **Execution Observability**

    ---

    Playbooks framework tracks call stack and variables. Step-by-step execution is verified using static 
    analysis of the program, with fully inspectable LLM program execution.

    [**Learn about Observability**](observability/index.md)

-   :material-database: **Artifacts and State Management**

    ---

    Store and retrieve data with artifacts. Manage state across playbook executions and between agents.

    [**Manage Artifacts**](artifacts/index.md)

</div>

<div class="footer"></div>
