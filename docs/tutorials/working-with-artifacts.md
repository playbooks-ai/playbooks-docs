# Working with Artifacts

In this tutorial, you'll learn how to create, store, and manage data using artifacts in Playbooks AI.

> :warning: Support for artifacts is under active development and is subject to change.

## Objective

By the end of this tutorial, you'll understand:

- What artifacts are and why they're useful
- How to create and save artifacts
- How to load and use artifacts in playbooks
- How to share artifacts between agents

## Prerequisites

- Completion of [Python Playbooks](python-playbooks.md)
- Understanding of variables and data manipulation

## What Are Artifacts?

Artifacts in Playbooks AI are similar to variables, but their values are **not** included in LLM calls by default. This makes them suitable for storing large data objects. Artifacts need to be explicitly loaded for their content to be included in LLM calls.

For now, artifacts support text content only. Support for other types of content, such as images, will be added in the future.

Artifacts are useful for:

- Storing data that for use within a given session, such as results of a web search
- Sharing large amounts of data between playbooks or agents
- Storing created reports and documents

>:bulb: Use artifacts to keep LLM token usage low.

## Creating and Saving Artifacts

You can create artifacts using the `SaveArtifact` function:

```markdown
## CreateReport
### Steps
- $report = SaveArtifact("sales_report.md", 2-3 line summary of sales report, 10-20 page long sales report)
- Tell the user that the sales report has been created
- Share $report with the user
```

The `SaveArtifact` function takes three parameters:

1. `name`: A unique identifier for the artifact (often with a file extension)
2. `summary`: A brief summary of what the artifact contains
3. `content`: The actual content to store in the artifact (can be text, JSON, or other data)

## Loading Artifacts

You can load artifacts using the `LoadArtifact` function:

```markdown
## ViewReport
### Steps
- $report = LoadArtifact("sales_report.md")
- Tell the user "Here is the sales report: Artifact[sales_report.md]"
```

The `LoadArtifact` function returns an artifact object.

## Artifact References

When you want to refer to an artifact without loading its entire content, you can use artifact references:

```markdown
## ShareReport
### Steps
- Tell the user: "Here is your report: Artifact[sales_report.md]"
```

This will display a link or reference to the artifact in the user interface, allowing the user to access it directly.

Alternatively, you can ask Playbooks to share an artifact object with the user:

```markdown
- Share $report with the user
```

You can also ask Playbooks to share an artifact by name:

```markdown
- Share sales_report.md with the user
```

## When is an artifact included in an LLM call?

### When a new artifact is created
When a new artifact is created, it is included in the subsequent LLM call.

### When an artifact is loaded
When an artifact is loaded using LoadArtifact, it is included in the subsequent LLM call.

## Using Artifacts in Python Playbooks

You can use SaveArtifact and LoadArtifact in Python playbooks.

````
```python
@playbook
async def CompileReports(report_names: list[str]) -> str:
    compiled_report = []
    for report_name in report_names:
        report = await LoadArtifact(report_name)
        compiled_report.append(report.content[:100])

    compiled_report = "\n".join(compiled_report)
    await SaveArtifact("compiled_report.md", "Compiled Report", compiled_report)
    return "Artifact[compiled_report.md]"
```
````

In this example, the `CompileReports` playbook loads the reports and saves the compiled report as an artifact. It then returns reference to the compiled report.

## Sharing Artifacts Between Agents

>:warning: Sharing artifacts between agents is not yet supported.

## Best Practices for Working with Artifacts

- **Use meaningful names**: Choose artifact names that describe their content
- **Provide good descriptions**: Include detailed descriptions to help Playbooks runtime select appropriate artifact

## Exercises

1. Write a RAG agent that stores intermediate search results as artifacts

## Next Steps

Congratulations! You've now completed the basic tutorials for Playbooks AI.

To continue learning, explore these topics:

- [Multi-Agent Systems](../multi-agent-systems/index.md)
- [Playbooks Assembly Language](../playbooks-language/playbooks-assembly-language.md)