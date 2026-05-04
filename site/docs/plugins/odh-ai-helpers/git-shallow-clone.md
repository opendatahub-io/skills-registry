<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# git-shallow-clone

Perform a shallow clone of a Git repository to a temporary location
for local analysis instead of using web APIs.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![git-shallow-clone diagram](git-shallow-clone.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repository_url` | :material-check: | — | URL of the Git repository to clone |
| `tag_or_branch` |  | `HEAD` | Git tag or branch to shallow clone |

## Usage

```
/git-shallow-clone https://github.com/psf/requests.git
/git-shallow-clone https://github.com/psf/requests.git v2.28.0
```
