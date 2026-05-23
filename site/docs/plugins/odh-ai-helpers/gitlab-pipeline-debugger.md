---
title: gitlab-pipeline-debugger
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# gitlab-pipeline-debugger

Debug and monitor GitLab CI/CD pipelines for merge requests. Check
pipeline status, view job logs, and troubleshoot CI failures using the
glab CLI. Supports auto-detection of the GitLab project from the local
git remote, or targeting a specific project via URL or -R flag. Can
parse full GitLab pipeline and job URLs to extract project paths and IDs.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![gitlab-pipeline-debugger diagram](gitlab-pipeline-debugger.svg)
</div>

## Arguments

```bash
/gitlab-pipeline-debugger [PIPELINE_URL] [-b] [-p] [-R]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PIPELINE_URL` |  | - | Full GitLab pipeline or job URL to debug |
| `-b` |  | - | Branch name to check pipeline for |
| `-p` |  | - | Specific pipeline ID to inspect |
| `-R` |  | `auto-detected from git remote` | GitLab project path to target |

## Usage

```bash
/gitlab-pipeline-debugger
/gitlab-pipeline-debugger https://gitlab.com/org/project/-/pipelines/123456
/gitlab-pipeline-debugger -b feature-branch
```
