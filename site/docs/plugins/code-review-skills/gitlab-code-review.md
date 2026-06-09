---
title: gitlab-code-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# gitlab-code-review

Perform a structured AI code review of a GitLab merge request. Reviews all
commits in the branch since the base branch, produces a strict-schema JSON
review (summary, positive aspects, severity-tagged inline comments, optional
fix prompt), and posts the results to the GitLab MR via the review.py script
— or displays them in the terminal when run locally. Reviews only the
committed diff (ignores uncommitted changes), filters suggestion-level
comments via chill mode, and deduplicates against previous reviews. Accepts
optional free-text review instructions that override the default review
guidelines.

**Plugin**: [code-review-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![gitlab-code-review diagram](gitlab-code-review.svg)
</div>

## Arguments

```bash
/gitlab-code-review [additional review instructions]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `additional review instructions` |  | - | Free-text guidance that overrides the default review guidelines (e.g., focus areas, standards to enforce, severity emphasis). Substituted into the review prompt via $ARGUMENTS. |

## Usage

```bash
/gitlab-code-review
/gitlab-code-review focus on security and error handling
/gitlab-code-review only flag critical and major issues
```
