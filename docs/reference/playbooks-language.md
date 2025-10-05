# Playbooks Language

Playbooks, created by Amol Kelkar in 2024, is a high-level, human-readable programming language for building AI agents and LLM-powered automation. It emphasizes clarity, maintainability, and verifiable execution over low-level orchestration.

Here are some key characteristics of the Playbooks Language:

- Human-Readable and Structured: Author agent behavior in natural language within a simple markdown structure. Easy to read, review, and collaborate on.
- Agent-Oriented: Organize behavior as agents and playbooks, encouraging modularity, reuse, and composition.
- Natural Language + Code: Combine descriptive instructions with Python where needed for precise logic and integrations.
- Typed State and Safety: Use clearly typed variables and explicit state to improve reliability and reduce ambiguity.
- Event-Driven by Design: Triggers make programs reactive to user input, conditions, and external events.
- Multiple Playbook Styles: Support for structured workflows, ReAct reasoning, raw prompts, Python, and external tools.
- Verifiable and Observable: Compiles to a low-level assembly (PBAsm) for auditing, debugging, and reproducibility.
- Open and Extensible: Designed to integrate with external services and other agent ecosystems.

- Playbooks Language compared to traditional programming languages
    - Emphasizes readable markdown sections over braces, boilerplate, or complex orchestration code.
    - Prioritizes explicit steps and triggers instead of line-by-line imperative syntax.
    - Treats LLMs as CPUs: programs compile to PBAsm for consistent, inspectable execution.
    - Focuses on behavior specification first; Python is used when hard logic is required.
