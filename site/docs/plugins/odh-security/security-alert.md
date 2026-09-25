---
title: security-alert
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# security-alert

Use this skill to filter a pre-fetched set of Hacker News stories down to those that report supply-chain security threats relevant to the Red Hat / RHEL ecosystem, Python (PyPI/pip), or JavaScript/TypeScript (npm/yarn/pnpm). Reads stories from stories.json in the workspace, performs semantic analysis (fetching HN threads when the title alone is ambiguous), and writes the stories worth alerting on to findings.json.

**Plugin**: [odh-security](index.md) | **:material-check: User-invocable**

## Usage

```bash
/security-alert
```
