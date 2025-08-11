---
title: FAQs
---

# Frequently Asked Questions

## What Python and OS are supported?

- Python 3.12+
- macOS, Linux, Windows (WSL recommended on Windows)

## Which models are supported?

- Optimized/tested: `claude-sonnet-4-20250514`
- Others may work: set `MODEL` and the provider key (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY`)

## How do I set API keys?

- Create a `.env` with `MODEL` and the matching provider key. The loader reads `.env` and `.env.<ENV>` automatically.

## How do I run a program?

```bash
playbooks run path/to/program.pb -v
```

You can pass multiple files and mix compiled + source:

```bash
playbooks run a.pbasm b.pb
```

## What is `.pbasm`? How do I compile?

- PBASM is the intermediate representation. Compile with:

```bash
playbooks compile program.pb --output program.pbasm
```

Run compiled files directly:

```bash
playbooks run program.pbasm --skip-compilation
```

## Where is the compilation cache?

- Next to the source file in `.pbasm_cache/` with versioned filenames. Delete the folder to force recompilation.

## Can I use different models for compilation and execution?

- Set `COMPILER_MODEL` to override the compile-time model (falls back to `MODEL`).

## How do I debug?

Use the `playbooks` VSCode extension to step-debug. See [VSCode](integrations/vscode.md) for setup.

## Is there a web UI?

- Yes. Start the Web Server and open the HTML Playground. See [Web Server](applications/web-server.md) and [HTML Playground](applications/playground.md).

## How do I use examples?

- Run any program in `tests/data`:

```bash
playbooks run tests/data/01-hello-playbooks.pb
```

## How do I enable Langfuse tracing?

- Set `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_HOST`. See [Langfuse integration](integrations/langfuse.md).

## VSCode language support?

- Install the `playbooks` extension for syntax highlighting, preview, diagnostics, and debugging.

## Where to report issues or get help?

- Open an issue on GitHub (`playbooks-ai/playbooks`).

## Troubleshooting

- Model errors or unexpected behavior
    - Set `MODEL=claude-sonnet-4-20250514` to use the default tested model
    - For other providers, set matching API key and model name

- `ImportError: No module named playbooks`
    - Activate your virtualenv and reinstall: `pip install playbooks`
    - Ensure you’re launching VSCode/terminal from the same environment

- Program not found / glob returns nothing
    - Check paths and quotes. Try absolute paths or expand globs: `playbooks run "tests/data/*.pb"`

- Stale compilation results
    - Delete `.pbasm_cache` next to your `.pb` files to force recompilation
    - Optionally precompile with `playbooks compile foo.pb --output foo.pbasm` and run the `.pbasm`

- VSCode language features not active
    - Install the `playbooks` extension and reopen a `.pb` file
    - Ensure the workspace uses the correct Python interpreter
