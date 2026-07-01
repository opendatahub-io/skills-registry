---
title: docs-workflow-create-merge-request
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-create-merge-request

Orchestrator step that commits, pushes, and opens a merge request (GitLab)
or pull request (GitHub) for the generated documentation. Runs
`create_merge_request.sh`, which resolves git context and platform, creates a
`<ticket>` feature branch if on main/master, reads the file list from the
writing step's manifest, commits with a `docs(<ticket>):` message, pushes
with `--force-with-lease`, derives the title from the requirements output,
checks for an existing open MR/PR, and creates one via `gh`/`glab` (with
GitLab fork detection). Skipped in `--draft` mode. Replaces the older
prepare-branch/commit/create-mr trio.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-create-merge-request diagram](docs-workflow-create-merge-request.svg)
</div>

## Arguments

```bash
/docs-workflow-create-merge-request <ticket> --base-path <path> [--draft] [--repo-path <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads writing/step-result.json). |
| `--draft` |  | `false` | Skip all git operations (draft mode). |
| `--repo-path` |  | - | Target docs repo (must already be on a feature branch). |

## Usage

```bash
/docs-workflow-create-merge-request PROJ-123 --base-path .agent_workspace/proj-123
```
