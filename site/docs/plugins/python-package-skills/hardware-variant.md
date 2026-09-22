---
title: hardware-variant
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# hardware-variant

Resolve free-text hardware requirements to one allowed accelerator variant

**Plugin**: [python-package-skills](index.md) | **:material-close: Internal**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Resolve package-request hardware requirements to exactly one allowed accelerator variant and emit a schema-valid verdict.</p>
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
        <li>Produces .hardware-variant-verdict.json with exactly verdict, variant, and reason fields.</li>
        <li>Selects only an allowed variant or reports unresolved when no valid variant can be selected.</li>
        <li>Validates the verdict against the hardware variant schema.</li>
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
        <li>Use only the supplied hardware context and never network or repository evidence.</li>
        <li>Keep the reason to one sentence and do not create other artifacts.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Bash, Read, Write</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">uv, python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/python-package-skills/blob/main/skills/hardware-variant/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/hardware-variant/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/python-package-skills/blob/main/skills/hardware-variant/references/output-format.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/hardware-variant/references/output-format.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/python-package-skills/blob/main/skills/hardware-variant/schemas/hardware-variant-verdict.json"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/hardware-variant/schemas/hardware-variant-verdict.json</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/hardware-variant
```
