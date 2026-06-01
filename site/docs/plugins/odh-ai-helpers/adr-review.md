---
title: adr-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# adr-review

Review an Architectural Decision Record (ADR) using a panel of six
specialist reviewer sub-agents running in parallel. The reviewers cover
Context & Problem Framing, Technical Soundness, Operational & Reliability,
Security & Compliance, Cost & Performance, and Consequences & Reversibility.
After the panel runs, a human-in-the-loop step lets the user agree, disagree,
or refine each finding before synthesis. Produces consolidated outputs as
both a detailed PDF report and a scannable PPTX slide deck. Handles
Markdown files, .docx documents, and directories of multiple ADRs.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![adr-review diagram](adr-review.svg)
</div>

## Arguments

```bash
/adr-review <ADR_PATH>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ADR_PATH` | :material-check: | - | Path to an ADR file (.md or .docx) or a directory containing multiple ADRs |

## Usage

```bash
/adr-review /path/to/adr.md
/adr-review /path/to/adr-directory/
```
