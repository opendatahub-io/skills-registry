---
title: docs-workflow-requirements
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-requirements

Analyzes documentation requirements for a JIRA ticket using a two-pass
fanout. Pass 1 dispatches a `requirements-discoverer` agent to enumerate
requirements from JIRA, PRs, and specs into a JSON skeleton; pass 2 fans out
one `requirements-analyst` agent per requirement (all in a single parallel
message) for isolated deep analysis, each reading its own skeleton from disk
and writing a per-requirement JSON file. A merge agent then assembles the
standard requirements.md off the main thread. Also extracts discovered repos
from the JIRA graph (feeding automatic source resolution) and writes a
sidecar with the requirement count. Disk-based data flow keeps 15+ agent
results out of the orchestrator context.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-requirements diagram](docs-workflow-requirements.svg)
</div>

## Arguments

```bash
/docs-workflow-requirements <ticket> --base-path <path> [--pr <url>]... [--repo <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (writes requirements/ output). |
| `--pr` |  | - | PR/MR URL to include in analysis. Repeatable. |
| `--repo` |  | - | Source code repo path, passed to analyst agents for code verification. |

## Usage

```bash
/docs-workflow-requirements PROJ-123 --base-path .agent_workspace/proj-123
/docs-workflow-requirements PROJ-123 --base-path .agent_workspace/proj-123 --pr https://github.com/org/repo/pull/42 --repo /path/to/repo
```
