---
title: pipeline-grouping
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pipeline-grouping

Groups failed CI/CD pipeline jobs by shared root cause. Reads the
preprocessed `errors.txt` for every failed job listed in the job
manifest, identifies distinct failure patterns, and clusters jobs whose
errors point to the same underlying cause — merging across collections
and pipeline actions when the errors match, splitting within a collection
when they differ (biasing toward splitting when uncertain, since each
group spawns one downstream RCA task).

Rather than emitting JSON directly, the skill drives the `grouper.py`
CLI to build groups incrementally in a work file and then `finalize`s
it, which validates that every expected job ID is assigned to exactly
one group before writing `grouping.json`. If open Jira tickets are
provided in `recent-tickets.json`, it also checks each group against
them and writes `dedup-results.json` for matches, so recurring failures
reuse an existing ticket instead of filing a duplicate.

**Inputs** (from `/workspace/`): `_context/grouping-context.json`,
`jobs/<id>-<name>/errors.txt`, optional `recent-tickets.json`.
**Outputs**: `grouping.json`, optional `dedup-results.json`.

**Plugin**: [pipeline-skills](index.md) | **:material-close: Internal**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Read preprocessed error files for all failed jobs, identify distinct failure patterns, and group jobs by shared root cause into grouping.json.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">analyze</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Produces grouping.json with all expected job IDs assigned to groups.</li>
        <li>Each group has a human-readable summary and representative error messages.</li>
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
        <li>Every expected job ID must appear in exactly one group.</li>
        <li>Do not modify job trace logs or error files.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Bash, Grep, Glob</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/pipeline-grouping/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/pipeline-grouping/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/pipeline-grouping/scripts/grouper.py"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/pipeline-grouping/scripts/grouper.py</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![pipeline-grouping diagram](pipeline-grouping.svg)
</div>

## Usage

Internal skill (`user-invocable: false`) — invoked by the
[pipeline-failure-analyzer](https://github.com/opendatahub-io/pipeline-failure-analyzer)
orchestrator inside the Claude Code container, not run interactively. The
orchestrator prepares the `/workspace/` inputs and reads back `grouping.json`.
