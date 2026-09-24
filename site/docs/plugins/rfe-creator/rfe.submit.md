---
title: rfe.submit
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.submit

Push RFEs to Jira via deterministic Python scripts (scripts/submit.py)
using the REST API with Basic Auth. Creates new RHAIRFE tickets for new
RFEs or updates existing tickets for fetched RFEs, then rebuilds
artifacts/rfes.md and reports results. Applies labels automatically based
on pipeline outcomes (auto-created, auto-revised, split-original,
split-result, needs-attention, rubric-pass, and the three mutually
exclusive feasibility verdicts). Non-interactive by design -- invoking the
skill is the confirmation, no dry-run approval step. Requires JIRA_SERVER,
JIRA_USER, and JIRA_TOKEN environment variables.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Create or update RHAIRFE Jira tickets from reviewed RFE artifacts using deterministic REST API calls.</p>
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
        <li>Creates or updates RHAIRFE Jira tickets from the reviewed RFE artifacts.</li>
        <li>Applies pipeline-outcome labels and rebuilds artifacts/rfes.md.</li>
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
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Route all Jira writes through the deterministic Python scripts (REST plus Basic Auth), not LLM tool-calling.</li>
        <li>Keep the three feasibility labels mutually exclusive.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/main/.claude/skills/rfe.submit/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe.submit/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![rfe.submit diagram](rfe.submit.svg)
</div>

## Arguments

```bash
/rfe.submit [--dry-run] [--artifacts-dir <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--dry-run` |  | - | Validate locally without writing to Jira |
| `--artifacts-dir` |  | `artifacts` | Path to the artifacts directory |

## Usage

```bash
/rfe.submit
/rfe.submit --dry-run
```
