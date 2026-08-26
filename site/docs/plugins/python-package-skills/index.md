---
title: python-package-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-package-skills

AI skills for Python package onboarding into the RHAI distribution pipeline. End-to-end automation covering packaging investigation, license checking, security auditing, build failure analysis, fondue monorepo onboarding, probe test creation, Jira context summarization, and executive summary generation. Designed to run inside a Claude Code container as part of the package-onboarding CI pipeline.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Repository**: [opendatahub-io/python-package-skills](https://github.com/opendatahub-io/python-package-skills)
    - **Tags**: <span class="tag-pill">python-packaging</span> <span class="tag-pill">onboarding</span> <span class="tag-pill">fondue</span> <span class="tag-pill">investigation</span> <span class="tag-pill">security</span> <span class="tag-pill">license</span> <span class="tag-pill">testing</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/executive-summary`](executive-summary.md) | Create a concise 2-3 line executive summary of a package onboarding outcome | :material-close: internal |
| [`/failure-analysis`](failure-analysis.md) | Analyze a build failure for a Python package in the RHAI pipeline and produce a structured diagnosis report | :material-close: internal |
| [`/fondue-onboarding`](fondue-onboarding.md) | Onboard a Python package into the fondue monorepo (builder/ and/or rhai-pipeline/) with configuration changes, linting, and git commit(s) | :material-close: internal |
| [`/jira-context-summary`](jira-context-summary.md) | Summarize Jira ticket context for a package onboarding request with actionable requirements and blockers | :material-close: internal |
| [`/license-check`](license-check.md) | Check Python package license compatibility with redistribution in Red Hat AI distribution pipeline | :material-close: internal |
| [`/packaging-investigation`](packaging-investigation.md) | Investigate a Python package for enterprise packaging and distribution readiness with structured analysis and verdict | :material-close: internal |
| [`/probe-test-onboarding`](probe-test-onboarding.md) | Create probe tests for a Python package in the wheels-test repository with git commit | :material-close: internal |
| [`/security-audit`](security-audit.md) | Run a security audit on a Python package with risk rating and structured verdict | :material-close: internal |

## Installation

**Claude Code**

```bash
/plugin install python-package-skills@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `python-package-skills` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
