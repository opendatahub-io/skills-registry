---
title: docs-workflow-tech-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-tech-review

Orchestrator step for a single technical-accuracy review pass over the
documentation drafts, with optional code-grounded claim validation. When
code-learner analysis exists, it extracts verifiable claims from the drafts
(via a subagent), dispatches batched `code-questioner` agents (one per doc
file, in parallel) to verdict each claim (supported / partially / unsupported
/ no-evidence), and a merge agent assembles claim-validation.json — passed to
the `technical-reviewer` agent as pre-computed evidence. The reviewer emits
an `Overall technical confidence: HIGH|MEDIUM|LOW` line and severity counts;
the orchestrator drives the iteration loop. Iterations 2+ reuse prior
validation.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-tech-review diagram](docs-workflow-tech-review.svg)
</div>

## Arguments

```bash
/docs-workflow-tech-review <ticket> --base-path <path> [--repo <path>]...
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads writing/ output and code-analysis/). |
| `--repo` |  | - | Source code repo path(s) for code-grounded validation. First is primary; repeatable. |

## Usage

```bash
/docs-workflow-tech-review PROJ-123 --base-path .agent_workspace/proj-123
/docs-workflow-tech-review PROJ-123 --base-path .agent_workspace/proj-123 --repo /path/to/repo
```
