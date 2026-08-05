---
title: fondue-onboarding
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# fondue-onboarding

Onboard a Python package into the fondue monorepo (builder/ and/or rhai-pipeline/) with configuration changes, linting, and git commit(s)


**Plugin**: [python-package-skills](index.md) | **:material-close: Internal**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Analyze package information, AI packaging analysis, and optional build failure details to configure a Python package in the fondue monorepo (builder/ and/or rhai-pipeline/) based on mode (combined or pipeline-only), then create the required git commit(s).</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">transform</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Commit count matches mode (1 for pipeline-only, 2 for combined).</li>
        <li>Requirements files created for all variant directories under rhai-pipeline/collections/onboarding/.</li>
        <li>In combined mode, builder configuration is created and .gitlab-triggers.yaml is included in the builder commit.</li>
        <li>make linter passes with no errors before every commit.</li>
        <li>Working tree is clean after the final commit.</li>
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
        <li>Only configure the package from context, not transitive dependencies.</li>
        <li>Do not stage the _run/ directory.</li>
        <li>In combined mode, builder and rhai-pipeline changes must be in separate commits.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Bash, Read, Grep, Glob</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3, git, make</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/python-package-skills/blob/main/skills/fondue-onboarding/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/fondue-onboarding/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Usage

```bash
/fondue-onboarding
```
