---
title: VSCode Extension
---

# VSCode Extension

Install the Playbooks VSCode extension (`playbooks`) for language support and debugging.

## Features

- Syntax highlighting for `.pb` and `.pbasm`
- Live Preview for `.pb`
- Diagnostics and document symbols
- Step-through debugging with breakpoints and call stack
- Basic configuration options (Python path, debug port, preview theme)

## Install

1. Open VSCode
2. Extensions (Cmd+Shift+X / Ctrl+Shift+X)
3. Search for `playbooks`
4. Install the Playbooks extension

## Use

- Open a `.pb` file to enable language features
- Live Preview: Cmd/Ctrl+Shift+V
- Run & Debug: open a `.pb` and add a Playbooks debug configuration

### Debug configuration

Add via Run and Debug UI or add to `launch.json`:

```json
{
  "type": "playbooks",
  "request": "launch",
  "name": "Launch Playbook",
  "program": "${file}",
  "stopOnEntry": true,
  "pythonPath": "python",
  "cwd": "${fileDirname}",
  "console": "integratedTerminal",
  "env": {
    "ANTHROPIC_API_KEY": "your-key"
  }
}
```

Tip: Run your program with the CLI in debug mode to attach: `playbooks run my.pb --debug --wait-for-client`.

See Observability & Debugging for server flags and workflows.


