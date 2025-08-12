---
title: Langfuse
---

# Langfuse Integration

You can enable tracing of Playbooks executions with Langfuse.

## Setup

1. Deploy Langfuse (e.g., using their Docker Compose setup)
2. Create an organization and project
3. Generate a secret key and public key
4. Configure environment variables in your `.env`:

```ini
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=http://localhost:3000
```

Playbooks will include tracing spans when configured.

## See also

- [Observability & Debugging](../observability/index.md)

