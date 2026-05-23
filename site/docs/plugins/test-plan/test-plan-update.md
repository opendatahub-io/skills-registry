---
title: test-plan-update
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-update

Update an existing test plan with new documentation (ADR, API specs, design docs).
Re-runs the 3 parallel analyzers with original + new material, uses the merge
sub-agent to intelligently integrate findings while preserving user edits, resolves
gaps, re-runs quality review, and optionally regenerates test cases. Bumps the
version number automatically.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan-update diagram](test-plan-update.svg)
</div>

## Arguments

```bash
/test-plan-update <SOURCE> <NEW_DOC_PATH> [<NEW_DOC_PATH>...]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `SOURCE` | :material-check: | - | Test plan location: local directory path, GitHub branch URL, or GitHub PR URL |
| `NEW_DOC_PATH` | :material-check: | - | One or more paths to new documentation files (ADR, API spec, design doc) |

## Usage

```bash
/test-plan-update ~/Code/collection-tests/mcp_catalog adr.pdf
/test-plan-update https://github.com/org/repo/pull/42 api-spec.md design.md
```
