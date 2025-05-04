# Observability

Playbooks AI provides comprehensive observability capabilities to help you monitor, debug, and optimize your AI agents. This is essential for building reliable and trustworthy AI systems, especially in production environments.

## Overview

The observability features in Playbooks AI enable you to:

- Monitor playbook execution and performance
- Track LLM interactions and token usage
- Debug complex agent workflows
- Gain insights into agent decision-making processes
- Measure and optimize costs
- Ensure compliance and auditability

## LangFuse Integration

Playbooks AI integrates with [LangFuse](https://langfuse.com), an open-source observability platform specifically designed for LLM applications. LangFuse provides tracing, evaluation, and analytics for your AI agents.

### Setting Up LangFuse

To enable LangFuse integration, you need to:

1. Deploy your own LangFuse instance [using docker compose](https://langfuse.com/self-hosting/docker-compose) or set up an account on [LangFuse Cloud](https://cloud.langfuse.com).
2. Configure your environment variables in the `.env` file
    ```
    # LangFuse Configuration
    LANGFUSE_ENABLED=true
    LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
    LANGFUSE_SECRET_KEY=your_langfuse_secret_key
    LANGFUSE_HOST=your_langfuse_instance_url
    ```

## What Playbooks AI Traces

When LangFuse integration is enabled, Playbooks AI automatically traces:

1. **Playbook Executions**: Each markdown and Python playbook run with timing and context
2. **LLM Interactions**: Prompts, completions, tokens, and latency
3. **User Interactions**: Messages and responses
4. **Agent State Changes**: Variables and context updates
5. **Errors and Exceptions**: Problems encountered during execution

## Viewing and Analyzing Data

After integrating with LangFuse, run a Playbooks program and then view the traces in the LangFuse dashboard.