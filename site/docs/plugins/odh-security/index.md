---
title: odh-security
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-security

Supply-chain security alerting and OCI image CVE comparison

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Generic
    - **Category**: [Security Review](../../categories/security.md)
    - **Tags**: <span class="tag-pill">cve</span> <span class="tag-pill">supply-chain</span> <span class="tag-pill">oci</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/oci-cve-checker`](oci-cve-checker.md) | Use this skill to compare CVE vulnerabilities between two OCI container images and generate reports showing fixed and new CVEs. | :material-check: |
| [`/security-alert`](security-alert.md) | Use this skill to filter a pre-fetched set of Hacker News stories down to those that report supply-chain security threats relevant to the Red Hat / RHEL ecosystem, Python (PyPI/pip), or JavaScript/TypeScript (npm/yarn/pnpm). Reads stories from stories.json in the workspace, performs semantic analysis (fetching HN threads when the title alone is ambiguous), and writes the stories worth alerting on to findings.json. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-security@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-security` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
