---
title: Playbooks CLI
---

# Playbooks CLI

The `playbooks` command-line interface lets you run and compile Playbooks programs.

## Usage

```bash
playbooks --version
playbooks <command> [options]
```

## Commands

### run

Run one or more Playbooks programs.

```bash
playbooks run [options] <program_paths...>
```

- `program_paths`: One or more `.pb` or `.pbasm` files

Options:

- `--application <module>`: Application module to use (default: `playbooks.applications.agent_chat`)
- `-v, --verbose`: Print the session log
- `--debug`: Start the debug server
- `--debug-host <host>`: Debug server host (default: `127.0.0.1`)
- `--debug-port <port>`: Debug server port (default: `7529`)
- `--wait-for-client`: Wait for a debug client to connect before starting execution
- `--stop-on-entry`: Stop at the beginning of playbook execution
- `--skip-compilation`: Skip compilation step (automatically skipped for `.pbasm` files)

Examples:

```bash
playbooks run hello.pb
playbooks run examples/chatbot.pb --debug --wait-for-client
playbooks run compiled/hello.pbasm --skip-compilation
# Mix compiled and source files
playbooks run compiled/hello.pbasm hello.pb
```

## See also

- [Run with CLI](../guides/run-with-cli.md)
- [VSCode Extension](../integrations/vscode.md)

### compile

Compile one or more Playbooks programs.

```bash
playbooks compile [options] <program_paths...>
```

Options:

- `--output <path>`: Output file path (if not specified, prints to stdout). Do not use when compiling multiple files.

Examples:

```bash
playbooks compile hello.pb
playbooks compile hello.pb --output hello.pbasm
```

## Exit codes

- `0`: Success
- Non-zero: Error (e.g., program load or compilation failure)


