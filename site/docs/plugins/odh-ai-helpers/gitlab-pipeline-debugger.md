<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# gitlab-pipeline-debugger

Debug and monitor GitLab CI/CD pipelines for merge requests. Check
pipeline status, view job logs, and troubleshoot CI failures using glab CLI.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![gitlab-pipeline-debugger diagram](gitlab-pipeline-debugger.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repository_url` |  | `auto-detected from git remote` | GitLab repository URL or branch name |
| `--p` |  | — | Specific pipeline ID to inspect |

## Usage

```
/gitlab-pipeline-debugger
/gitlab-pipeline-debugger https://gitlab.com/org/repo
```
