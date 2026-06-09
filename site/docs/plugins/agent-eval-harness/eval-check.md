---
title: eval-check
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-check

Full-harness configuration health check. Inventories all skills, commands,
CLAUDE.md, and hooks (via harness_inventory.py), reads each skill's full
SKILL.md plus project CLAUDE.md files, and analyzes the configuration as a
single system. Produces an informational report with findings across five
categories: content overlap (duplicated rules between skills), trigger overlap
(descriptions that activate for the same tasks), CLAUDE.md duplication (rules
already in CLAUDE.md that are restated in skills), type misclassification
(skills that should be hooks, commands, or CLAUDE.md rules), and structural
issues (missing descriptions, overly broad triggers, commands shadowing
built-ins). Read-only -- modifies no skills/config and writes only the report
(refusing paths outside the project root). Skips cross-component analysis for
single-skill projects.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-check diagram](eval-check.svg)
</div>

## Arguments

```bash
/eval-check [--output <path>] [--include-global]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--output` |  | `harness-report.md` | Where to write the health check report. Must resolve within the project root. |
| `--include-global` |  | `false` | Also scan ~/.claude/CLAUDE.md (user-global config). Opt-in for privacy. |

## Usage

```bash
/eval-check
/eval-check --include-global
/eval-check --output eval/health-report.md
```
