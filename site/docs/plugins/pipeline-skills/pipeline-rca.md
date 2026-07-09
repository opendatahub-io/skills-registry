---
title: pipeline-rca
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pipeline-rca

Performs root cause analysis for a single error group produced by
pipeline-grouping. Reads the group's trace logs and preprocessed errors,
investigates the failure against pipeline source at the exact commit SHA
(local git first, GitLab API fallback), and diagnoses *why* the failure
occurred rather than just what it looks like.

The skill is disciplined about evidence: it focuses on the first error
in each log (later errors are cascades), verifies its theory with a
cheap distinguishing check before committing to a diagnosis, lowers
confidence when verification isn't possible, and redacts credentials in
any quoted log lines. It emits content-fragment section files —
`error-overview.md` (symptom), `root-cause.md` (diagnosis and failure
chain), and optionally `resolution.md` and `feedback.md` — plus a
schema-validated `finding.json` carrying the confidence level, cascade
flag, group consistency, target repository for the fix, and every file
consulted. A deterministic outer script assembles these into the
per-group report.

**Inputs** (from `/workspace/`): `_context/rca-context.json`,
`pipeline-context.json`, `groups/<group_id>/jobs/.../trace.log` and
`errors.txt`, `_repos/` shallow clones. **Outputs**:
`<group_dir>/finding.json` and `<group_dir>/sections/*.md`.

**Plugin**: [pipeline-skills](index.md) | **:material-close: Internal**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Investigate the root cause of a CI/CD failure group by analyzing trace logs, source code, and build artifacts. Produce structured section files and a finding.json with classification metadata.</p>
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
        <li>Produces finding.json with all required fields valid against the schema.</li>
        <li>Produces sections/error-overview.md and sections/root-cause.md.</li>
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
        <li>Do not fabricate log lines or error messages not present in the evidence.</li>
        <li>Redact credentials, tokens, and API keys in all output.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Bash, Grep, Glob</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3, git, glab</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/pipeline-rca/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/pipeline-rca/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/pipeline-rca/references/finding.schema.json"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/pipeline-rca/references/finding.schema.json</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/pipeline-rca/references/error-overview-section-template.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/pipeline-rca/references/error-overview-section-template.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/pipeline-rca/references/rca-section-template.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/pipeline-rca/references/rca-section-template.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/pipeline-rca/references/resolution-section-template.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/pipeline-rca/references/resolution-section-template.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![pipeline-rca diagram](pipeline-rca.svg)
</div>

## Usage

Internal skill (`user-invocable: false`) — invoked once per error group by the
[pipeline-failure-analyzer](https://github.com/opendatahub-io/pipeline-failure-analyzer)
orchestrator inside the Claude Code container, not run interactively. A
deterministic outer script assembles the section files and `finding.json`
into the per-group report.
