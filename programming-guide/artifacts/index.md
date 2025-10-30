# Artifacts in Playbooks

Artifacts implement pass-by-reference semantics suitable for variables holding large amounts of text. If large values are passed between playbooks using pass-by-value, the content gets duplicated in LLM context multiple times, which makes the program execution slower and more expensive. Artifacts solve this by storing content once and passing only the reference.

______________________________________________________________________

## What Are Artifacts?

An artifact is a variable holding named reference to large text content. Just like a variable, it has a name (like `$report`) and value. In addition, it also has a short one-line summary describing its content. Artifacts are automatically created when a value longer than a threshold is returned from a playbook or when a variable is set to a long value. When created, the content is added to LLM context so the LLM can reference the content by its name. Once the playbook returns, the content is removed from LLM context. However, if the artifact is referenced again later, it will be loaded back into LLM context automatically.

______________________________________________________________________

## Context Duplication Problem

When large values are passed between playbooks as regular variables, the content appears in LLM context multiple times. Consider this flow:

```markdown
- Load $document = ReadFile("doc.md")     # Content in context
- Process $document                       # Content duplicated when sent
- Analyze $document                       # Content duplicated when sent
- Review $document                        # Content duplicated when sent
```

The content gets duplicated as it's sent as an argument, appears as a local variable in the receiving playbook, and shows up again in the state sent to the LLM.

Artifacts fix this by implementing pass-by-reference. Instead of passing the content, only the artifact name is passed:

```markdown
- Load $document = ReadFile("doc.md")     # Artifact created automatically (content loaded into context)
- Process $document                       # Only name sent
- Analyze $document                       # Only name sent
- Review $document                        # Only name sent
```

All playbooks reference the same artifact by name, so the content exists once.

### How Context Loading Works

Think of it like lazy loading. When you create an artifact by returning large content, that content goes into context for the current playbook. The playbook can work with it normally. When the playbook returns, the runtime unloads the content from context to keep things efficient—but the artifact still exists as a reference (name + summary) in the current state. For example, the following state is sent to LLM -

```text
"variables": {
    "$a_2bc92b04": "Output from ReadText(file1.txt)",
    "$summary": "Summary of text from file1.txt"
  },
```

Note that the two artifacts are are listed with their summaries. These can be used as normal variables. For example,

```markdown
- Show $summary to the user
```

When the playbook that created/loaded the artifact returns, the runtime automatically unloads the artifact from context. However, the artifact still exists as a reference (name + summary) in the current state.

Later, when you reference that artifact again in another playbook, the runtime will automatically load it back into context. For example,

```markdown
- Get the list of laws mentioned in file1.txt
```

Here, the a_2bc92b04 artifact is referenced again by the LLM. The runtime will automatically load it back into context.

The key insight is that artifact names are always available (they're in the state), so you can reference them freely. The content gets loaded automatically when needed, keeping context lean while still giving the LLM access to large data whenever it needs it.

______________________________________________________________________

## Automatic Artifact Creation

When a playbook returns a value longer than a threshold (configurable via `artifact_result_threshold` in `playbooks.toml`), Playbooks automatically creates an artifact:

```python
@playbook
async def ReadFile(path: str) -> str:
    with open(path) as f:
        return f.read()  # if longer than artifact_result_threshold, auto-creates artifact with name $a_<hash>
```

The artifact name is based on a content hash, which keeps names stable across runs and prevents duplicate artifacts and cache misses.

## Explicit Artifact Creation

For important content, create artifacts with meaningful names using `SaveArtifact()`:

```python
@playbook
async def GenerateReport(data: dict) -> str:
    report = "content\n"*100
    await SaveArtifact("$report", "100 lines of content", report)
    return "$report"
```

This makes the code more readable and the artifact's purpose clearer.

______________________________________________________________________

## Artifact API

### SaveArtifact(name, summary, value)

Create an artifact with an explicit name. The function signature is `async def SaveArtifact(name: str, summary: str, value: str) -> str`. The `name` parameter is the variable name (with or without `$` prefix), `summary` is a one-line description, and `value` is the content as a string. It returns the artifact name.

### LoadArtifact(artifact_name)

Force-load an artifact's content into context. In most cases, this happens automatically when you reference an artifact. Use this only when you want to explicitly ensure content is in context before it's needed.

The function signature is `async def LoadArtifact(artifact_name: str)`. It returns None.

### Artifact Properties (Python)

When working with artifacts in Python, access the name, summary, and full content via `artifact.name`, `artifact.summary`, and `artifact.value`.

______________________________________________________________________

## Usage Notes

Artifacts work transparently with playbook arguments and returns, so you can pass them around just like regular variables. Content is automatically loaded back into context when you reference an artifact, keeping things efficient without requiring explicit management. Use meaningful names for important content via `SaveArtifact()`, while hash-based auto-generated names are fine for temporary artifacts since they're stable across runs. If needed, adjust the character threshold for automatic artifact creation in `playbooks.toml` under `artifact_result_threshold`.
