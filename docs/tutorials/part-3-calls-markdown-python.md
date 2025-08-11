---
title: Part 3 – Calling playbooks (Markdown ↔ Python)
---

# Part 3 – Calling playbooks (Markdown ↔ Python)

Audience: Intermediate

Goal: Compose Markdown and Python playbooks on one call stack.

## Run the examples

Markdown calls Python and back:

```bash
playbooks run tests/data/03-md-calls-python.pb
```

Python interop:

```bash
playbooks run tests/data/playbooks-python-interop.pb
```

Round‑trip:

```bash
playbooks run tests/data/04-md-python-md.pb
```

Concepts:

- `@playbook` Python functions
- Arguments and return values
- Mixed execution on a unified call stack

Next: Part 4 – Agent‑to‑Agent calls.


