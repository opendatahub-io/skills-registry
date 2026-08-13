---
title: create-dsc
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# create-dsc

Create a DataScienceCluster (DSC) on an OpenShift cluster with RHOAI, waiting for Ready state

**Plugin**: [ai-safety-skills](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Create a DataScienceCluster resource on an OpenShift/RHOAI cluster, either from a custom YAML or auto-extracted from the operator CSV, and confirm it and all its component pods reach a healthy state.</p>
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
        <li>The DSC reaches Ready phase and redhat-ods-applications pods are Running/Completed.</li>
        <li>A pre-existing DSC is never overwritten without explicit user confirmation.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/create-dsc/SKILL.md" title="sheltoncyril/sheltons-toolkit@cec313e2f38d493acf8c8ad65bddb110903fb70a:skills/create-dsc/SKILL.md">SKILL.md @ cec313e<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Never apply a second DSC without deleting the existing one first — concurrent DSCs cause reconciliation conflicts.</li>
        <li>A custom DSC not named default-dsc must be flagged, since the wait logic looks for that exact name.</li>
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
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/create-dsc/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/create-dsc/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Usage

```bash
/create-dsc
```
