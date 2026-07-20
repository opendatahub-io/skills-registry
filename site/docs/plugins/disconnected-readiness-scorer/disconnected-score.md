---
title: disconnected-score
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# disconnected-score

Score a repository's readiness for disconnected / air-gapped OpenShift
deployments. Runs all (or selected) rules from the repo root and produces
an aggregate score with per-rule findings. Supports auto-remediation
(--fix), rule selection (--rules), and multiple output formats (markdown
or JSON). Exits 0 for READY/WARNING, 1 for NOT READY.

**Plugin**: [disconnected-readiness-scorer](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Score an RHOAI component repository&#x27;s readiness for disconnected / air-gapped OpenShift deployments by running static-analysis rules for image manifest completeness, digest enforcement, runtime egress, and Python dependency validation.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">review</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Runs the selected rules against the target repository and reports findings per rule with severity.</li>
        <li>Produces a READY / NOT READY verdict with a markdown or JSON report.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--deterministic">deterministic</span>
        <span class="skill-contract__ref-placeholder"></span>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not modify the target repository unless auto-remediation is explicitly requested with --fix.</li>
        <li>Exclude test files, CI config, and linting rules from blocker-level findings.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Bash, Glob, Grep</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3, arch-analyzer</span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/disconnected-readiness-scorer/blob/main/skills/disconnected-score/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/disconnected-score/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![disconnected-score diagram](disconnected-score.svg)
</div>

## Arguments

```bash
/disconnected-score [--rules <list>] [--fix] [--report <format>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--rules` |  | `all` | Run only specified rules. Aliases: csv, tags, egress, python, manifest. |
| `--fix` |  | - | Attempt auto-remediation where possible (e.g., replace image tags with digests). |
| `--report` |  | `markdown` | Output format for the readiness report. |

## Usage

```bash
/disconnected-score
/disconnected-score --rules csv,tags
/disconnected-score --fix
/disconnected-score --report json
```
