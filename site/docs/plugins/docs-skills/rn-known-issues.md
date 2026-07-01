---
title: rn-known-issues
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rn-known-issues

Audits known-issue status for a release version. Infers the previous GA
version from the target (z-stream / GA / EA patterns), then runs four JQL
queries (via the Atlassian MCP, falling back to `jira-reader`) to find new
known issues still open, new ones already resolved in-cycle, previously
documented ones now resolved (candidates to move to Fixed Issues), and
previously documented ones still open (carry-forward). Checks each issue's
Release Note Text field for real content beyond the template skeleton, and
produces a categorized markdown report. Defaults to the RHOAIENG project.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rn-known-issues diagram](rn-known-issues.svg)
</div>

## Arguments

```bash
/rn-known-issues <fix-version> [--project <KEY>] [--previous <version>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `fix-version` | :material-check: | - | Target fix version (e.g., rhoai-3.4.1). |
| `--project` |  | `RHOAIENG` | Jira project key. |
| `--previous` |  | - | Previous GA version to compare against (auto-inferred if omitted). |

## Usage

```bash
Check known issues for rhoai-3.4.1
Run rn-known-issues for rhoai-3.5 --project RHOAIENG
Check known issues for rhoai-3.4.2 --previous rhoai-3.3
```
