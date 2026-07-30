---
title: eval-anova
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-anova

Fan a DoE matrix of agent configs across shared cases, then run repeated-measures/mixed-effects ANOVA (F, p, effect size) plus a cost/quality Pareto.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Run a full-factorial Design-of-Experiments comparison of agent configurations (models, thinking-effort, prompts, or other factors) across a fixed set of test cases by fanning /eval-run out over the matrix, then analyze the resulting standard runs with repeated-measures / mixed-effects ANOVA (F, p, effect size) and a cost/quality Pareto frontier, and render the comparison and statistics reports.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">orchestrate</span>
        <span class="skill-contract__chip skill-contract__chip--function">analyze</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Reads the eval.yaml matrix: block, expands the full-factorial grid (conditions x cases x replications), and with --dry-run prints the design and a cost estimate without executing.</li>
        <li>Drives /eval-run once per condition x replication so each cell lands as a standard run with its own summary.yaml, stamped with a condition.json recording its factor levels.</li>
        <li>Computes each case composite via the canonical harness reward composition (compose_reward) and writes anova.json containing the ANOVA result (method, F, p, effect size, significance), condition summaries, Pareto frontier, and per-case matrix.</li>
        <li>Selects repeated-measures ANOVA for single-factor designs and the mixed-effects model for multi-factor designs, restricting the analysis to cases present under every condition.</li>
        <li>Renders the /eval-compare comparison report and the statistics-forward report.py deep view from on-disk artifacts; --analyze-only re-analyzes existing runs (including externally produced ones) without re-executing.</li>
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
        <li>eval-run stays the single-condition primitive: eval-anova only loops it and must not re-implement workspace/execute/collect/score.</li>
        <li>Repeated-measures ANOVA assumes the same cases run under every condition; keep the design balanced by restricting to common cases and recording excluded cases rather than silently dropping them.</li>
        <li>Compute case composites via the canonical harness reward composition (compose_reward honouring eval.yaml reward:, else boolean-gate + normalised-numeric average); do not invent a scoring scheme.</li>
        <li>Do not auto-select plain one-way ANOVA when cases are reused across conditions.</li>
        <li>Report renderers (report.py, /eval-compare) read only on-disk summary.yaml / anova.json artifacts and never re-run the experiment.</li>
        <li>A failed matrix cell is logged and skipped so a partial matrix still yields an analysis over the cells that succeeded.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Bash, Write</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-anova/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-anova/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-anova/scripts/orchestrate.py"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-anova/scripts/orchestrate.py</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-anova/scripts/analyze.py"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-anova/scripts/analyze.py</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-anova/scripts/report.py"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-anova/scripts/report.py</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-anova/scripts/design.py"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-anova/scripts/design.py</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-anova/references/matrix-schema.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-anova/references/matrix-schema.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-anova/prompts/interpret-anova.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-anova/prompts/interpret-anova.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/eval-anova
```
