---
title: validate-component-onboarding-jira
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# validate-component-onboarding-jira

Pre-flight validation tool for ODH/RHOAI component onboarding. Given a Jira
issue URL (or just a key like RHOAIENG-1234), fetches issue details, downloads
the component_onboarding_details.yaml attachment, and validates it against the
JSON Schema. Cross-validates repo_branch for RHOAI (must match target version
pattern), checks Dockerfile digest pinning for RHOAI components (all FROM
instructions must use @sha256 digests), and updates Jira with validation results
(labels: validation-successful/validation-failed, status: In Progress on success).
Any failure is a hard blocker with a clear error message and Jira comment.

**Plugin**: [aiops-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![validate-component-onboarding-jira diagram](validate-component-onboarding-jira.svg)
</div>

## Arguments

```bash
/validate-component-onboarding-jira <JIRA_URL>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `JIRA_URL` | :material-check: | - | Jira ticket URL or key (e.g. RHOAIENG-1234) containing the component_onboarding_details.yaml attachment to validate. |

## Usage

```bash
/validate-component-onboarding-jira https://redhat.atlassian.net/browse/RHOAIENG-12345
/validate-component-onboarding-jira RHOAIENG-12345
```
