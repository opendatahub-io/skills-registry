---
title: autofix-research
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# autofix-research

Investigate a Jira spike ticket with no associated repository. Reads the
ticket context, researches the topic using available files and codebase
search, and writes structured findings to autofix-output/.autofix-verdict.json.
Limited to read-only investigation (no Bash) — notes limitations in
observations if external access would be needed.

**Plugin**: [autofix-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![autofix-research diagram](autofix-research.svg)
</div>

## Usage

```bash
/autofix-research
```
