---
title: product-design-harness
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# product-design-harness

Use when a product direction, feature, workflow, experiment, launch, feedback signal, automation, or scale decision needs judgment before execution or the next iteration.

**Plugin**: [ux3-product-design-harness](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Review a supplied product direction across User, Evidence, and Business flows before choosing a bounded next action. Programmatic measurement here covers only the structured review and linked handoff contract checks implemented by check_review.py; it does not establish evidence truth, product viability, safety certification, or host authorization enforcement.</p>
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
        <li>Emit a structured review containing the three flow judgments, canonical verdict, next action, execution boundary, and stop conditions.</li>
        <li>Use check_review.py to check review schema and deterministic verdict, weakest-flow, and evidence-tier consistency; use its --context-pack mode when validating a linked continue handoff. This declares the verifier, not a measured passing result.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--verifier_backed">verifier_backed</span>
        <a class="skill-contract__ref" href="https://github.com/cis2042/ux3-product-design-harness/blob/48965c6b501f61ebbb8130c9c2e4f9af08922b9f/skills/product-design-harness/resources/scripts/check_review.py" title="cis2042/ux3-product-design-harness@48965c6b501f61ebbb8130c9c2e4f9af08922b9f:skills/product-design-harness/resources/scripts/check_review.py">check_review.py @ 48965c6<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Do not implement during the review; a verify verdict permits only its stated proof step.</li>
        <li>Do not average flow verdicts or convert human-owned decisions into a machine score.</li>
        <li>Keep the original User, Evidence, and Business flow meanings and declared execution boundary; this contract does not repair the pinned source&#x27;s known override-padding defect.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3 with jsonschema</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">documents</span><span class="skill-contract__code-val">skills/product-design-harness/SKILL.md, skills/product-design-harness/resources/docs/CONTRACTS.md</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/cis2042/ux3-product-design-harness/blob/48965c6b501f61ebbb8130c9c2e4f9af08922b9f/skills/product-design-harness/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/product-design-harness/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/cis2042/ux3-product-design-harness/blob/48965c6b501f61ebbb8130c9c2e4f9af08922b9f/skills/product-design-harness/resources/scripts/check_review.py"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/product-design-harness/resources/scripts/check_review.py</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/cis2042/ux3-product-design-harness/blob/48965c6b501f61ebbb8130c9c2e4f9af08922b9f/skills/product-design-harness/resources/schemas/review-result.schema.json"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/product-design-harness/resources/schemas/review-result.schema.json</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/cis2042/ux3-product-design-harness/blob/48965c6b501f61ebbb8130c9c2e4f9af08922b9f/skills/product-design-harness/resources/schemas/context-pack.schema.json"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/product-design-harness/resources/schemas/context-pack.schema.json</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/cis2042/ux3-product-design-harness/blob/48965c6b501f61ebbb8130c9c2e4f9af08922b9f/skills/product-design-harness/resources/docs/CONTRACTS.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/product-design-harness/resources/docs/CONTRACTS.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/product-design-harness
```
