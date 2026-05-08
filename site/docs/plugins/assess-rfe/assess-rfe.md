---
title: assess-rfe
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# assess-rfe

Assess RFEs against quality criteria using a structured rubric. Supports
single-input mode (Jira key, file path, URL, raw text) and bulk mode
(wildcard pattern) with 30 concurrent parallel scorer agents.

**Plugin**: [assess-rfe](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![assess-rfe diagram](assess-rfe.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `input` | :material-check: | — | RFE to assess — accepts multiple input formats |

## Usage

```
/assess-rfe RHAIRFE-1234
/assess-rfe /path/to/document.md
/assess-rfe https://some-url
/assess-rfe RHAIRFE-*
```
