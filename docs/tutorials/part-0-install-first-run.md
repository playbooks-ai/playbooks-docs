---
title: Part 0 – Install and first run
---

# Part 0 – Install and first run

Audience: Beginners

Goal: Install Playbooks and run your first program.

## 1. Install

Follow the [Installation](../get-started/installation.md). Verify with:

```bash
playbooks --version
```

## 2. Configure environment

Create `.env` in your project root:

```ini
MODEL=claude-sonnet-4-20250514
ANTHROPIC_API_KEY=your_key
```

## 3. Run hello world

Use the example provided in the repository:

```bash
playbooks run tests/data/01-hello-playbooks.pb
```

Expected: The agent prints a greeting and exits.

Next: Proceed to [Part 1 – User interaction](part-1-user-interaction.md).


