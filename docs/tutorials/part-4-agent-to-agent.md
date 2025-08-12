---
title: Part 4 – Agent‑to‑Agent calls
---

# Part 4 – Agent‑to‑Agent calls

Audience: Intermediate

Goal: Make one agent call a public playbook on another agent.

## Run the example

```bash
playbooks run tests/data/multi-agent.pb -v
```

Observe:

- `FirstAgent.A(1024)` is a public Python playbook invoked from another agent
- Country info agent exposes public playbooks callable by others

Concepts:

- Public playbooks
- Cross‑agent calls with arguments and return values

Next: [Part 5 – Meetings](part-5-meetings.md).


