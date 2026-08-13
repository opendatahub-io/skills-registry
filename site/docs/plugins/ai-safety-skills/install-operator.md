---
title: install-operator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# install-operator

Install any individual RHOAI dependency operator on an OpenShift cluster using install-operator.sh

**Plugin**: [ai-safety-skills](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Install one of 16 supported RHOAI dependency operators via OLM, with optional channel/source/version overrides, and confirm its CSV reaches Succeeded.</p>
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
        <li>The requested operator&#x27;s CSV reaches Succeeded phase in its expected namespace.</li>
        <li>Positional script arguments are built correctly even when only a subset of channel/source/version overrides is given.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/install-operator/SKILL.md" title="sheltoncyril/sheltons-toolkit@cec313e2f38d493acf8c8ad65bddb110903fb70a:skills/install-operator/SKILL.md">SKILL.md @ cec313e<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Never reorder or flag-ify the script&#x27;s positional arguments — it only accepts NAME CHANNEL SOURCE VERSION in that order.</li>
        <li>Never run the install as a bounded foreground call — Manual-approval installs can exceed typical foreground timeouts.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Bash, Read, AskUserQuestion</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">oc, git</span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/install-operator/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/install-operator/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Usage

```bash
/install-operator
```
