---
title: docs-workflow-security-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-security-review

Orchestrator step that runs a security/PII scan of the documentation drafts
before publication. Determines the source files from the writing sidecar,
runs the deterministic `pii_scanner.py` (validating well-formed JSON output),
then applies the `docs-review-security` Layer-2 agent checklist for patterns
regex can't catch. Builds a report and writes a sidecar with scanner/agent
finding counts broken down by category (ip, email, credential, url, mac,
internal_hostname). Iteration logic is owned by the orchestrator.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-security-review diagram](docs-workflow-security-review.svg)
</div>

## Arguments

```bash
/docs-workflow-security-review <ticket> --base-path <path>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads writing/ output). |

## Usage

```bash
/docs-workflow-security-review PROJ-123 --base-path .agent_workspace/proj-123
```
