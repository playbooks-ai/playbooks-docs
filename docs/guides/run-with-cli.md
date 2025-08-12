---
title: Run with CLI
---

# Run with CLI

Run Playbooks programs from the command line.

## Basics

```bash
playbooks run program.pb
```

Multiple source files:

```bash
playbooks run compiled/program1.pbasm program2.pb
```

## Compile

```bash
playbooks compile program.pb --output program.pbasm
```

## Debug server
Used by the Visual Studio Code extension for Playbooks debugging.

```bash
playbooks run program.pb --debug --wait-for-client --stop-on-entry
```


## See also

- [Playbooks CLI](../applications/cli.md)
- [VSCode Extension](../integrations/vscode.md)
- [Observability & Debugging](../observability/index.md)

