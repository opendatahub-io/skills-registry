---
title: test-plan-resolve-feedback
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-resolve-feedback

Read PR review comments from a published test plan, assess each against the
existing test plan content, and let the user decide which to apply. Processes
comments one at a time with assessment (aligns, conflicts, needs clarification,
already covered) and concrete change proposals. Commits and pushes approved
changes to the same branch with a descriptive commit message.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan-resolve-feedback diagram](test-plan-resolve-feedback.svg)
</div>

## Arguments

```bash
/test-plan-resolve-feedback <PR_URL>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PR_URL` | :material-check: | - | Full GitHub PR URL (e.g., https://github.com/owner/repo/pull/42) |

## Usage

```bash
/test-plan-resolve-feedback https://github.com/org/test-plans-repo/pull/42
```
