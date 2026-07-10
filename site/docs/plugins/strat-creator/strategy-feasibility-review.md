---
title: strategy-feasibility-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-feasibility-review

An independent, adversarial reviewer (staff-engineer persona) that assesses a refined
strategy for technical feasibility, RFE alignment, and effort-estimate credibility.
Invoked by `strategy-review` in an isolated `context: fork`, it auto-detects local vs
CI mode, optionally grounds itself in architecture context, and checks whether the
approach can actually be built, whether it delivers what the RFE asks, whether the
T-shirt size is credible, whether hidden dependencies exist, and whether risks and
assumptions are properly separated with concrete mitigations. It emits a structured
per-strategy verdict (feasible / needs revision / infeasible).

**Plugin**: [strat-creator](index.md) | **:material-close: Internal**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Review strategy features for technical feasibility, implementation complexity, and effort estimate credibility.</p>
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
        <li>Produces a feasibility assessment for each strategy with recommendation.</li>
        <li>Grounds findings in architecture context when available.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/strat-creator/blob/0e102d4d1c4a2747895c267b637cf8a33d5f93fc/.claude/skills/strategy-feasibility-review/SKILL.md" title="opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-feasibility-review/SKILL.md">SKILL.md @ 0e102d4<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not approve strategies with fundamental technical flaws.</li>
        <li>Do not fabricate architecture constraints not present in the docs.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Grep, Glob</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/strat-creator/blob/main/.claude/skills/strategy-feasibility-review/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>.claude/skills/strategy-feasibility-review/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![strategy-feasibility-review diagram](strategy-feasibility-review.svg)
</div>

## Arguments

```bash
/strategy-feasibility-review [RHAISTRAT-NNNN]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `RHAISTRAT-NNNN` |  | - | A strategy key to review only that strategy. If omitted, all strategies in the tasks directory are reviewed. |

## Usage

```bash
/strategy-feasibility-review RHAISTRAT-1531
```
