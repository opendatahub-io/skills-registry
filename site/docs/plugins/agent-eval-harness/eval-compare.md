---
title: eval-compare
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-compare

Discovers a directory of eval run artifacts and generates a self-contained tabbed HTML comparison report with model cards, quality/cost tables, per-case breakdowns, and LLM-written analysis.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Take a directory of eval run artifacts (summary.yaml, run_result.json, optional report.html and anova.json), discover and aggregate runs per model, and produce a self-contained tabbed HTML comparison report whose LLM-written analysis sections (verdict, badges, strengths, shared weaknesses, recommendations) are grounded in the per-case scores and cost data.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">analyze</span>
        <span class="skill-contract__chip skill-contract__chip--function">generate</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Runs the discover and generate subcommands of compare.py to find every subdirectory containing summary.yaml and emit index.html plus per-run report.html copies for iframe embedding.</li>
        <li>Replaces the generated placeholder sections (Bottom Line verdict, Where Each Model Shined, Shared Weaknesses, Recommendations) with analysis grounded in each run&#x27;s summary.yaml per-case scores, judge breakdowns, and cost data.</li>
        <li>Adds Best Value / Highly Variable / Not Viable badges only when they clearly apply, honoring the mutual-exclusivity rules (a highly variable model is never Best Value).</li>
        <li>Includes runs with missing run_result.json or report.html via graceful degradation, and aggregates repeated models as averages with min/max ranges.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/agent-eval-harness/blob/1559af5d404128ed3458d1a9bdb4580c76244b01/skills/eval-compare/SKILL.md" title="opendatahub-io/agent-eval-harness@1559af5d404128ed3458d1a9bdb4580c76244b01:skills/eval-compare/SKILL.md">SKILL.md @ 1559af5<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">evidence_completeness</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/agent-eval-harness/blob/1559af5d404128ed3458d1a9bdb4580c76244b01/skills/eval-compare/SKILL.md" title="opendatahub-io/agent-eval-harness@1559af5d404128ed3458d1a9bdb4580c76244b01:skills/eval-compare/SKILL.md">SKILL.md @ 1559af5<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not modify or write to any input/source file; only write to the output directory.</li>
        <li>Do not run evaluations or compute statistics — render pre-computed anova.json numbers only, never import scipy/statsmodels/pingouin.</li>
        <li>Do not explore the input directory manually (no ls/find); let compare.py handle all run discovery.</li>
        <li>Do not invent findings, badges, or verdicts unsupported by the per-case scores and cost data.</li>
        <li>Preserve graceful degradation and per-model aggregation (averages with min/max ranges) so partial or repeated runs are still included.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-compare/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-compare/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/agent-eval-harness/blob/v1.30.0/skills/eval-compare/scripts/compare.py"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/eval-compare/scripts/compare.py</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/eval-compare
```
