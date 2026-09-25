---
title: odh-rpm
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-rpm

RPM build failure analysis and non-Red Hat RPM detection

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Tags**: <span class="tag-pill">rpm</span> <span class="tag-pill">containers</span> <span class="tag-pill">compliance</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/non-redhat-rpms`](non-redhat-rpms.md) | Use this skill to identify non-Red Hat RPM packages installed in container images or on the local machine. For containers, pulls images across multiple architectures and release tags; for local scans, inspects the host directly. Extracts RPM signing metadata and reports packages not signed with the Red Hat GPG key as CSV output. Use when auditing compliance, checking supply-chain provenance, or scanning for third-party RPMs in RHOAI component images. | :material-check: |
| [`/rpm-examine`](rpm-examine.md) | Analyze RPM build.log failures | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-rpm@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-rpm` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
