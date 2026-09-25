---
title: non-redhat-rpms
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# non-redhat-rpms

Use this skill to identify non-Red Hat RPM packages installed in container images or on the local machine. For containers, pulls images across multiple architectures and release tags; for local scans, inspects the host directly. Extracts RPM signing metadata and reports packages not signed with the Red Hat GPG key as CSV output. Use when auditing compliance, checking supply-chain provenance, or scanning for third-party RPMs in RHOAI component images.

**Plugin**: [odh-rpm](index.md) | **:material-check: User-invocable**

## Usage

```bash
/non-redhat-rpms
```
