---
title: lint-with-vale
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# lint-with-vale

Runs Vale style linting against documentation to check for style-guide
violations across Markdown, AsciiDoc, reStructuredText, HTML, XML, and
source-code comments. Checks for a `.vale.ini` (creating a temporary RedHat
config if none exists), runs `vale sync` to update style packages, then lints
files/directories/globs. Presents results errors-first, groups warnings and
suggestions, summarizes per file, and flags likely RedHat false positives
(technical terms, product names, code-block content, heading acronyms). Does
not auto-fix source files. Runs on Haiku.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![lint-with-vale diagram](lint-with-vale.svg)
</div>

## Arguments

```bash
/lint-with-vale <file|dir|glob>... [--minAlertLevel error|warning|suggestion] [--config <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `targets` | :material-check: | - | Files, directories, or --glob patterns to lint. |
| `--minAlertLevel` |  | - | Minimum alert level to report. |
| `--config` |  | - | Path to a specific .vale.ini config. |

## Usage

```bash
Lint the docs/ folder
vale --glob='*.{md,adoc}' docs/
vale --minAlertLevel=error README.md
```
