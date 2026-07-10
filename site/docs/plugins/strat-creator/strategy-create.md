---
title: strategy-create
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-create

Creates strategies from approved RFEs by cloning them into the RHAISTRAT Jira project
and setting up local artifacts for refinement. It discovers RFE source data (local
`artifacts/rfe-tasks/` or Jira), applies a status + required-label gate (must have a
target-version/`strat-creator-3.x` label plus `rfe-creator-autofix-rubric-pass` or
`tech-reviewed`), and for each surviving RFE either imports an existing RHAISTRAT clone
(Path A) or creates a new one (Path B). It freezes an RFE snapshot in
`strat-originals/`, captures source-RFE comments that carry removed implementation
detail, writes a strategy stub to `artifacts/strat-tasks/` with the fixed
three-section skeleton, applies provenance labels, and records the ticket mapping.

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Clone approved RFEs into the RHAISTRAT Jira project and set up local artifacts for refinement.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">execute</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Creates RHAISTRAT issues from approved RFEs via Jira clone or manual creation.</li>
        <li>Writes local strategy stubs to artifacts/strat-tasks/ with correct frontmatter.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/strat-creator/blob/0e102d4d1c4a2747895c267b637cf8a33d5f93fc/.claude/skills/strategy-create/SKILL.md" title="opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-create/SKILL.md">SKILL.md @ 0e102d4<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not clone RFEs that have not been approved.</li>
        <li>Do not modify the source RFE issue in Jira.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, mcp__atlassian__searchJiraIssuesUsingJql, mcp__atlassian__getJiraIssue</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/strat-creator/blob/main/.claude/skills/strategy-create/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>.claude/skills/strategy-create/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![strategy-create diagram](strategy-create.svg)
</div>

## Arguments

```bash
/strategy-create [RHAIRFE-NNNN ...] [config-name] [--dry-run]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `RHAIRFE-NNNN` |  | - | One or more source RFE keys to process. If provided, all of them are processed without prompting; if omitted, available RFEs are listed for selection. |
| `config-name` |  | - | Pipeline config filename (e.g. road-to-production) used as the run identifier recorded in strat-skipped.md; defaults to manual. |
| `--dry-run` |  | - | Skip all external Jira writes — no cloning or issue edits. Reads still happen and local artifacts are still created (using STRAT-NNN naming with jira_key=null). |

## Usage

```bash
/strategy-create
/strategy-create RHAIRFE-1458 RHAIRFE-1595
/strategy-create RHAIRFE-1458 road-to-production
/strategy-create RHAIRFE-1458 --dry-run
```
