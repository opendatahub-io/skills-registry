---
title: odh-documentation
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-documentation

AsciiDoc documentation generation, validation, review, and ADR review

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Documentation](../../categories/documentation.md)
    - **Tags**: <span class="tag-pill">documentation</span> <span class="tag-pill">asciidoc</span> <span class="tag-pill">adr</span> <span class="tag-pill">review</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/adr-review`](adr-review.md) | Review an Architectural Decision Record (ADR) using a team of six specialist reviewer subagents and produce a consolidated report as both PDF and PPTX slide deck. Use this skill whenever the user asks to review, critique, audit, or get feedback on an ADR, architecture decision, design doc, or RFC — whether the input is a Markdown file, a .docx document, or pasted text. Trigger even if the user does not explicitly say "ADR"; phrases like "review this architecture decision", "critique this design doc", or "run the reviewer panel on this" should also invoke this skill. | :material-check: |
| [`/doc-gap`](doc-gap.md) | Use this skill to analyze context sufficiency for documentation generation. Reads workspace/context-package.json and produces workspace/gap-report.json with severity-rated gaps and a proceed/gather-more/stop recommendation. | :material-check: |
| [`/doc-gather`](doc-gather.md) | Use when you need to gather context for a Jira ticket or PR. Resolves ticket metadata, clones relevant repos, collects candidate files, runs filtering pipeline, and produces workspace/context-package.json. | :material-check: |
| [`/doc-generate`](doc-generate.md) | Use when you need to generate AsciiDoc documentation modules from gathered context. Reads context package and gap report, generates content, then self-validates with iterative correction (up to 3 retries). Produces generated files and workspace/generation-report.json. | :material-check: |
| [`/doc-pipeline`](doc-pipeline.md) | Use this skill to orchestrate the full documentation pipeline. Sequences doc-gather, doc-gap, doc-validate, doc-review, and doc-generate skills based on the requested pipeline mode. | :material-check: |
| [`/doc-plan`](doc-plan.md) | Use this skill to produce a STRAT-level documentation plan. Traverses a strategic initiative's child epics and stories to identify what documentation is needed, what type, and at what priority. | :material-check: |
| [`/doc-post`](doc-post.md) | Use this skill to post validation and review findings as comments on a GitHub PR or GitLab MR. Reads workspace findings files and formats them as inline or summary comments. | :material-check: |
| [`/doc-review`](doc-review.md) | Use this skill to perform adversarial review of AsciiDoc documentation against context sources. Checks factual accuracy, completeness, consistency, and hallucination. Produces workspace/review-findings.json. | :material-check: |
| [`/doc-validate`](doc-validate.md) | Use when you need to validate AsciiDoc documentation for technical accuracy using Extract-Identify-Validate pattern. Runs Vale, asciidoctor, lychee, YAML syntax checks, and LLM-powered cross-reference validation. Produces workspace/validation-findings.json. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-documentation@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-documentation` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
