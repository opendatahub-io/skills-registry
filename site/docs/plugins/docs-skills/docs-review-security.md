---
title: docs-review-security
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-review-security

Two-layer scan for sensitive data that must not ship in published docs.
Layer 1 runs the deterministic `pii_scanner.py` regex scanner for real IP
addresses, credentials, internal hostnames, emails, and MAC addresses.
Layer 2 applies an agent checklist for patterns regex can't catch —
customer-specific names in YAML/JSON examples, internal Jira keys / wiki /
Slack references, real person or organization names, case/account numbers,
and LUN WWIDs. Reports each finding with file, line, category, severity, and
a safe replacement. Reused by the pipeline's security-review step.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-review-security diagram](docs-review-security.svg)
</div>

## Arguments

```bash
/docs-review-security <file>... | --docs-dir <path> [--scan-dirs <dirs>] [--file-types <exts>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `files / --docs-dir` | :material-check: | - | Files to scan, or a docs directory (with optional --scan-dirs and --file-types). |

## Usage

```bash
Scan this file for PII and sensitive data
pii_scanner.py scan --docs-dir docs --file-types .adoc,.md
```
