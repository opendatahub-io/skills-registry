---
title: aiops-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# aiops-skills

Component onboarding automation for ODH and RHOAI on the Konflux CI/build
platform. Provides an interactive create-then-validate pipeline: collect
onboarding parameters through guided Q&A, generate a validated
component_onboarding_details.yaml, create or update Jira tickets with the
YAML attached, and validate existing onboarding tickets against a JSON Schema
with cross-checks for branch naming, Dockerfile digest pinning, and
product-specific requirements.

Supports both ODH (CI and Release builds with optional release tags) and
RHOAI (architecture selection, release categories, target version-derived
branch naming, and operator manifest handling). All Jira operations use
deterministic Python scripts run via uv with Atlassian REST API authentication
(JIRA_USER_EMAIL + JIRA_API_TOKEN). When no Jira URL is provided, the create
skill automatically clones a product-specific template ticket (ODH: RHOAIENG-35683,
RHOAI: RHOAIENG-17225).


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Repository**: [opendatahub-io/aiops-infra](https://github.com/opendatahub-io/aiops-infra)
    - **Tags**: <span class="tag-pill">devops</span> <span class="tag-pill">testops</span> <span class="tag-pill">odh</span> <span class="tag-pill">rhoai</span> <span class="tag-pill">konflux</span> <span class="tag-pill">onboarding</span> <span class="tag-pill">ci-cd</span> <span class="tag-pill">release</span> <span class="tag-pill">automation</span>

## Pipeline

<div class="diagram-container" markdown>
![aiops-skills pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/create-component-onboarding-jira`](create-component-onboarding-jira.md) | Interactively collect component onboarding parameters and create/update a Jira ticket | :material-check: |
| [`/validate-component-onboarding-jira`](validate-component-onboarding-jira.md) | Pre-flight validation for ODH component onboarding — fetches Jira, downloads YAML, validates against schema | :material-check: |

## Installation

```bash
/plugin install aiops-skills@opendatahub-skills
```

## Architecture

Two skills form a create-then-validate pipeline for component onboarding:

create-component-onboarding-jira runs an 8-step interactive flow: parse input
and check prerequisites (uv, jq, Jira credentials), set up a working directory,
optionally fetch existing Jira details, collect parameters via guided Q&A with
product-aware conditional logic (ODH vs RHOAI), generate YAML via
generate_onboarding_yaml.py, validate against JSON Schema via
validate_yaml_schema.py, check Dockerfile digest pinning for RHOAI via
check_dockerfile_digests.py, create or update a Jira ticket (cloning
product-specific templates if no URL provided) via update_jira_issue.py, and
report results.

validate-component-onboarding-jira runs a 6-step validation flow: check
prerequisites, create working directory from Jira URL via init_workdir.sh,
fetch issue details via fetch_jira_details.py, download YAML attachment via
download_jira_attachment.py, validate against schema with cross-checks (branch
naming for RHOAI, Dockerfile digest pinning), and update Jira with
validation-successful or validation-failed labels via update_jira_issue.py.

Both skills use deterministic Python scripts (run via uv) for all Jira API
operations and YAML schema validation. The component_onboarding_details.schema.json
defines conditional requirements based on product_context (ODH vs RHOAI) and
is_operator fields. Shared scripts: init_workdir.sh (working directory setup),
check_prerequisites.sh (tool and env var checks), fetch_jira_details.py,
update_jira_issue.py, validate_yaml_schema.py, check_dockerfile_digests.py.
