---
title: create-component-onboarding-jira
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# create-component-onboarding-jira

Interactively collects ODH/RHOAI component onboarding parameters from the
user through a guided Q&A flow with product-aware conditional logic, generates
a validated component_onboarding_details.yaml, and creates or updates a Jira
ticket with the YAML attached. When no Jira URL is provided, automatically
creates a new ticket by cloning the product-specific onboarding template
(ODH: RHOAIENG-35683, RHOAI: RHOAIENG-17225). For RHOAI, auto-derives
repo_branch from target_rhoai_version, fetches the repo README to suggest
component descriptions, and validates Dockerfile digest pinning. Supports
both ODH (CI and Release builds) and RHOAI (with architecture selection,
release categories, and operator manifest handling).

**Plugin**: [aiops-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![create-component-onboarding-jira diagram](create-component-onboarding-jira.svg)
</div>

## Arguments

```bash
/create-component-onboarding-jira [JIRA_URL]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `JIRA_URL` |  | - | Existing Jira ticket URL to update (e.g. https://redhat.atlassian.net/browse/RHOAIENG-1234). If omitted, creates a new ticket by cloning the product-specific onboarding template. |

## Usage

```bash
/create-component-onboarding-jira
/create-component-onboarding-jira https://redhat.atlassian.net/browse/RHOAIENG-12345
```
