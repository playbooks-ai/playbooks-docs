# Observability & Debugging

Playbooks AI provides comprehensive observability capabilities to help you monitor, debug, and optimize your AI agents. This is essential for building reliable and trustworthy AI systems, especially in production environments.

## Overview

The observability features in Playbooks AI enable you to:

- Monitor playbook execution and performance
- Track LLM interactions and token usage
- Debug complex agent workflows
- Gain insights into agent decision-making processes
- Measure and optimize costs
- Ensure compliance and auditability

## Debug server

Run any program with a built-in debug server:

```bash
playbooks run my.pb --debug --wait-for-client --stop-on-entry
```

Flags:

- `--debug`: start the server
- `--debug-host` / `--debug-port`: address (default `127.0.0.1:7529`)
- `--wait-for-client`: pause until a client attaches
- `--stop-on-entry`: break at the first step

Attach from VSCode using the Playbooks debug configuration (see Integrations > VSCode). You can set breakpoints in `.pb`, step, and inspect the call stack.

## Session logs and events

Playbooks emits structured session logs and an event bus stream:

- Session logs: step execution, variable updates, playbook calls, LLM requests/responses
- Event bus: subscribe to `*` to print all events in a custom app; the Web Server and Playground consume this stream to visualize execution in real time

## Web Server & Playground

Start the server and open the HTML Playground to visualize agent messages and logs live. See Applications > Web Server and > HTML Playground for details.

## LangFuse Integration

Playbooks AI integrates with [LangFuse](https://langfuse.com), an open-source observability platform specifically designed for LLM applications. LangFuse provides tracing, evaluation, and analytics for your AI agents.

### Setting Up LangFuse

To enable LangFuse integration, you need to:

1. Deploy your own LangFuse instance [using docker compose](https://langfuse.com/self-hosting/docker-compose) or set up an account on [LangFuse Cloud](https://cloud.langfuse.com).
2. Configure your environment variables in the `.env` file
    ```
    # LangFuse Configuration
    LANGFUSE_SECRET_KEY=your_langfuse_secret_key
    LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
    LANGFUSE_HOST=http://localhost:3000
    ```

## What Playbooks AI Traces

When LangFuse integration is enabled, Playbooks AI automatically traces:

1. **Playbook Executions**: Each markdown and Python playbook run with timing and context
2. **LLM Interactions**: Prompts, completions, tokens, and latency
3. **User Interactions**: Messages and responses
4. **Agent State Changes**: Variables and context updates
5. **Errors and Exceptions**: Problems encountered during execution

## Viewing and analyzing data

After integrating with LangFuse, run a Playbooks program and then view the traces in the LangFuse dashboard.