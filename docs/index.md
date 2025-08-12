---
hide:
  - toc
---

<div style="text-align: center;">
  <div class="centered-logo-text-group">
    <h1>
    <img src="assets/images/playbooks-logo.png#gh-light-mode-only" alt="Playbooks AI" style="width: 200px; height: 200px;">
    <img src="assets/images/playbooks-logo-dark.png#gh-dark-mode-only" alt="Playbooks AI" style="width: 200px; height: 200px;">
    </h1>
  </div>
</div>

## Playbooks AI — Natural Language Programs, Verifiable Control, Multi-Agent

**Playbooks AI** introduces a programming paradigm where you define AI agent behavior through **clear, human-readable instructions**, crafted in plain English inside markdown “playbooks” that look like recipes, and are fully executable. Playbooks AI is a software stack for the [**Software 3.0**](https://www.youtube.com/watch?v=LCEmiRjPEtQ) era that seamlessly combines traditional code (Software 1.0), data-trained models (Software 2.0) and behavior defined directly in plain English, executed by LLMs as if they were CPUs (Software 3.0).

This isn't just prompting and hoping the LLM does the right thing - it’s **Natural Language Programming**. Business users can read, tweak, and approve the specification directly; while developers benefit from consistency, auditability, and full visibility into execution paths.

<div style="display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-start;">
  <div style="flex: 1 1 360px; min-width: 320px; background-color: white; border-radius: 8px;">
    <img alt="Playbooks program example" src="https://www.runplaybooks.ai/_next/image?url=%2Fimages%2Fplaybooks-ai-example-program.png&w=2048&q=75" style="width: 100%; border-radius: 8px; padding: 12px;" />
    <p style="text-align:center; font-size: 0.9rem; margin-top: 6px;">Natural Language Playbooks program (support.pb)</p>
  </div>
  <div style="flex: 1 1 360px; min-width: 320px; background-color: white; border-radius: 8px;">
    <img alt="VS Code debugger showing step-by-step execution" src="https://www.runplaybooks.ai/_next/image?url=%2Fimages%2Fplaybooks-ai-vscode-debugger.png&w=2048&q=75" style="width: 100%; border-radius: 8px; padding: 12px;" />
    <p style="text-align:center; font-size: 0.9rem; margin-top: 6px;">Step debugging compiled program (support.pbasm)</p>
  </div>
</div>

### How It Works

* **Hybrid stack of English + Python**: Seamlessly combine high-level natural-language steps with embedded Python logic (e.g., for system integration, data processing) and execute on a unified call stack.
* **Event-driven triggers**: Define reactive workflows using natural-language conditions (like “when X happens, run Y playbook”), radically simplifying the specification of complex workflows. See [Triggers](triggers/index.md).
* **Reliability + Flexibility**: Every execution is trackable - variables, call stacks, decisions, runtime flow - ensuring compliance, reproducibility, and confidence in agent behavior. At the same time, using LLMs as CPUs means programs are executed intelligently with common sense and high-level instructions.
* **Multi-agent**: Build systems of collaborating agents with public playbooks and messaging, simply by asking agents to do things or getting agents to participate in multi-party meetings. See [Agents](agents/index.md).
* **Dynamic generation of playbooks**: Let agents reason over context and objectives, then create new playbooks on the fly to tackle novel tasks. Thanks to the [Playbooks Runtime](runtime/index.md), execution of these dynamically generated playbooks is fully trackable and auditable. Learn more in [Dynamic Playbook Generation](advanced/dynamic-playbook-generation.md).
* **Observer agents**: Specialized overseers that monitor other agents step-by-step, catching deviations before any action takes effect, and steering them back on course for injectable governance over multi-agent systems. See [Observer Agents](advanced/observer-agents.md).

---

### Why It Matters

| Participant                       | Benefit                                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Business Users**                | Can author and refine playbooks in natural language. Transparency and control sit at the specification level. |
| **Developers & Engineers**        | Gain a reliable runtime instead of black box LLM prompt execution, with observability, testability, triggers, multi-agent coordination, and audit-ready outputs.          |
| **Governance & Compliance Teams** | Source is English-readable, version-controlled, and verifiable—ideal for reviews, sign-offs, and traceability.                 |
| **Product Strategy**              | Empowers rapid iteration - tune behaviors by editing `.pb` files, experiment safely, reuse logic, and scale confidently.         |


Under the hood, Playbooks provides a [Common Language Specification (CLS)](advanced/cls.md) and a [Common Language Runtime (CLR)](runtime/clr.md) - the “LLMOS” that validates and supervises program execution.

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
  <a href="guides/" class="md-button" style="margin:3px">Guides</a>
  <a href="playbooks-language/" class="md-button" style="margin:3px">Language</a>
</p>

## Quick example

```markdown
# Customer support agent
A demo customer support agent for Playbooks AI
 
## Greet the user
In this playbook, the customer support agent welcomes the user
### Triggers
- At the beginning
### Steps
- Tell user about yourself
- Ask the user for their name
- Say hello to the user by name
- Welcome user to Playbooks AI and say goodbye
- End program
```

### Run it

Save the example as `support.pb`, then run:

```bash
pip install playbooks
playbooks run support.pb
```

---

## Pick your path

Choose your starting point - each tile is a direct jump into docs with just enough context to know it’s right for you.

<div class="grid cards" markdown>

* :material-language-markdown: **Explore Playbooks Language**<br/>
  Write and refine agent behavior in plain English that anyone can understand and update.<br/>
  [Get started →](playbooks-language/index.md)

* :material-code-braces: **Build with Python**<br/>
  Add integrations, custom logic, or optimized computation—bridge English specs with code.<br/>
  [Learn how →](playbook-types/python-playbooks.md)

* :material-account-group: **Design Multi-Agent Systems**<br/>
  Create agents that collaborate, share context, and run public or exported playbooks.<br/>
  [See patterns →](agents/index.md)

* :material-bell-ring: **Automate with Triggers**<br/>
  Run playbooks automatically on schedules, events, or user actions.<br/>
  [Set up triggers →](triggers/index.md)

* :material-magnify-scan: **Gain Full Observability**<br/>
  Inspect every step, replay runs, debug deterministically, and keep audit-ready logs.<br/>
  [View tools →](observability/index.md)

* :material-shield-check: **Control Autonomy & Safety**<br/>
  Set guardrails, approvals, and per-step autonomy to keep agents aligned with intent.<br/>
  [Configure controls →](observability/index.md)

</div>


<div class="footer"></div>
