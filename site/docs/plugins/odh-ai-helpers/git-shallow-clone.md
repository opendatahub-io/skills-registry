---
title: git-shallow-clone
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# git-shallow-clone

Perform a shallow clone of a Git repository to a temporary location
for local analysis instead of using web APIs. Uses a helper script that
prints the clone path to stdout for downstream consumption.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![git-shallow-clone diagram](git-shallow-clone.svg)
</div>

## Arguments

```bash
/git-shallow-clone <REPOSITORY_URL> [TAG_OR_BRANCH]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `REPOSITORY_URL` | :material-check: | - | URL of the Git repository to clone |
| `TAG_OR_BRANCH` |  | `HEAD` | Git tag or branch to shallow-clone |

## Usage

```bash
/git-shallow-clone https://github.com/psf/requests.git
/git-shallow-clone https://github.com/psf/requests.git v2.28.0
```
