---
title: query-code
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# query-code

Answers a natural-language question about a previously `learn-code`-analyzed
codebase. Resolves the analysis (by `--repo` path/URL or by scanning
`.agent_workspace/` for an ONBOARDING.md), offers to run learn-code first if
no analysis exists, loads the detection/registry/summaries/relationships/
onboarding context, and dispatches a `code-questioner` agent that can also
Read/Grep the actual source to produce a file:line-grounded answer, saved as
a timestamped Markdown file under the analysis workspace.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![query-code diagram](query-code.svg)
</div>

## Arguments

```bash
/query-code <question> [--repo <path|url>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `question` | :material-check: | - | The question to answer (quote it). |
| `--repo` |  | - | Repository path or URL (optional if a single analysis exists). |

## Usage

```bash
/query-code "How does authentication work?" --repo /path/to/repo
/query-code "What modules depend on the database layer?"
```
