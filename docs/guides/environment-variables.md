---
title: Environment Variables
---

# Environment Variables

Playbooks reads configuration primarily from environment variables. The loader searches for `.env` and `.env.<environment>` files automatically.

## Environment file loading

At import time, Playbooks loads environment variables in this order:

1. `.env` in the project root (the directory where you run CLI)
2. `.env.<environment>` if present, where `<environment>` is taken from `ENV` or `ENVIRONMENT` (defaults to `development`)

## Model selection and API keys

- `MODEL`: Language model to use. Default: `claude-sonnet-4-20250514`.

:warning: Claude Sonnet 4.0 is the only LLM currently supported by Playbooks.

- Provider API keys (set the one matching your `MODEL`):
  - `ANTHROPIC_API_KEY` for Claude models
  - `OPENAI_API_KEY` for OpenAI models
  - `GEMINI_API_KEY` for Google Gemini models
  - `GROQ_API_KEY` for Groq models
  - `OPENROUTER_API_KEY` for OpenRouter models


- `COMPILER_MODEL`: Override the model used by the compiler stage (defaults to `MODEL` if unset)

## LLM response cache (optional)

- `LLM_CACHE_ENABLED` ("true"/"false"): Enable caching. Default: false
- `LLM_CACHE_TYPE`: `disk` (default) or other supported types
- `LLM_CACHE_PATH`: Directory path for disk cache when `disk` is used

## Langfuse tracing (optional)

- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_HOST` (e.g., `http://localhost:3000`)

