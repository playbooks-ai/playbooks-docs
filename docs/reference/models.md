# Models

Playbooks is tested and optimized for the following models:

- Anthropic Claude Haiku 4.5 ("claude-haiku-4-5-20251001"): Lightweight, fast and cost-effective model for general purpose use.
    ```toml
    # playbooks.toml
    [model]
    provider = "anthropic"
    name = "claude-haiku-4-5-20251001"
    ```

- Anthropic Claude Sonnet 4.5 ("claude-sonnet-4-5-20250929"): Powerful, general purpose model for complex tasks, reasoning, multi-agent collaboration.
    ```toml
    # playbooks.toml
    [model]
    provider = "anthropic"
    name = "claude-sonnet-4-5-20250929"
    ```

- Anthropic Claude Opus 4.5 ("claude-opus-4-5-20251101"): Powerful, general purpose model for complex tasks, reasoning, multi-agent collaboration, multi-agent collaboration, dynamic playbook generation and goal driven workflows.
    ```toml
    # playbooks.toml
    [model]
    provider = "anthropic"
    name = "claude-opus-4-5-20251101"
    ```

- xAI Grok 4.1 Fast Non-Reasoning ("xai/grok-4-1-fast-non-reasoning"): Fast, non-reasoning model for general purpose use.
    ```toml
    # playbooks.toml
    [model]
    provider = "xai"
    name = "grok-4-1-fast-non-reasoning"
    ```

- PlaybooksLM (proprietary, Enterprise-grade model developed by Playbooks AI, contact us at [contact@runplaybooks.ai](mailto:contact@runplaybooks.ai) for more information)
    ```toml
    # playbooks.toml
    [model]
    provider = "playbooks"
    name = "playbookslm"
    ```

Playbooks framework uses complex prompts that are optimized for Anthropic models. As a result, other frontier LLMs such as GPT-5, Gemini 2.5 Pro and Grok 4 may work, but additional testing and tuning may be required. Our current focus is on improving the core capabilities of the framework and demonstrating a novel way of programming AI agents. We plan to add testing and support for other models gradually. 

:bulb: As of Nov 2025, we recommend using Grok 4.1 Fast Non-Reasoning ("xai/grok-4-1-fast-non-reasoning") for experimentation and development. If you are using meetings or complex multi-agent interactions, we recommend using Sonnet 4.5 or Opus 4.5.

For production use, you may continue using Grok 4.1 Fast, Haiku 4.5, Sonnet 4.5 or switch to PlaybooksLM for lower latency, lower cost and full control over data privacy & security. PlaybooksLM is a proprietary, Enterprise-grade model developed by Playbooks AI. Please contact us at [contact@runplaybooks.ai](mailto:contact@runplaybooks.ai) for more information.


## Configuring LLM Providers in Playbooks

### API Key-Based Providers

For providers that use API keys (OpenAI, Anthropic, Google AI, Groq, OpenRouter), set the model in `playbooks.toml` and the corresponding API key as an environment variable.

**Example 1: Anthropic (Claude)**

```toml
# playbooks.toml
[model]
provider = "anthropic"
name = "claude-sonnet-4-5-20250929"
temperature = 0.2
```

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Example 2: OpenAI (GPT-4)**

```toml
# playbooks.toml
[model]
provider = "openai"
name = "gpt-5"
temperature = 0.2
```

```bash
export OPENAI_API_KEY="sk-..."
```

**Example 3: Google AI (Gemini API)**

```toml
# playbooks.toml
[model]
provider = "google"
name = "gemini-pro"
temperature = 0.2
```

```bash
export GEMINI_API_KEY="..."
```

---

### Credential-Based Providers (No API Key Required)

For cloud providers that use IAM/credential-based authentication, set the model with the provider prefix and configure cloud credentials via standard mechanisms.

**Example 4: Google Vertex AI**

```toml
# playbooks.toml
[model]
provider = "vertex_ai"
name = "vertex_ai/gemini-1.5-flash"
temperature = 0.2
```

```bash
# Authenticate via gcloud
gcloud auth application-default login

# Set project and location
export VERTEXAI_PROJECT="your-project-id"
export VERTEXAI_LOCATION="us-central1"
```

**Example 5: AWS Bedrock**

```toml
# playbooks.toml
[model]
provider = "bedrock"
name = "bedrock/anthropic.claude-v2"
temperature = 0.2
```

```bash
# Set AWS credentials
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_REGION_NAME="us-east-1"

# Or use IAM roles in AWS environment (no env vars needed)
```

**Example 6: Claude on Vertex AI**

```toml
# playbooks.toml
[model]
provider = "vertex_ai"
name = "vertex_ai/claude-sonnet-4"
temperature = 0.2
```

```bash
# Uses gcloud ADC, NOT ANTHROPIC_API_KEY
gcloud auth application-default login
export VERTEXAI_PROJECT="your-project-id"
export VERTEXAI_LOCATION="us-central1"
```

---

### Separate Compilation Model

You can use a different (often cheaper/faster) model for compilation:

```toml
# playbooks.toml
[model]
provider = "anthropic"
name = "claude-sonnet-4-5-20250929"
temperature = 0.2

[model.compilation]
provider = "vertex_ai"
name = "vertex_ai/gemini-1.5-flash"
temperature = 0.3
```

---

### Quick Reference

| Provider | `provider` | `name` example | Environment Variable |
|----------|------------|----------------|---------------------|
| OpenAI | `openai` | `gpt-4` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `claude-sonnet-4-5-20250929` | `ANTHROPIC_API_KEY` |
| Google AI | `google` | `gemini-pro` | `GEMINI_API_KEY` |
| Groq | `groq` | `groq/llama-2-70b` | `GROQ_API_KEY` |
| OpenRouter | `openrouter` | `openrouter/meta-llama/...` | `OPENROUTER_API_KEY` |
| **Vertex AI** | `vertex_ai` | `vertex_ai/gemini-1.5-flash` | gcloud ADC + `VERTEXAI_PROJECT`, `VERTEXAI_LOCATION` |
| **AWS Bedrock** | `bedrock` | `bedrock/anthropic.claude-v2` | AWS credential chain |
| **SageMaker** | `sagemaker` | `sagemaker/your-endpoint` | AWS credential chain |