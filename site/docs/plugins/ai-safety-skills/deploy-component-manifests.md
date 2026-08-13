---
title: deploy-component-manifests
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# deploy-component-manifests

Deploy custom component manifests into an OLM-deployed ODH/RHOAI operator via a kustomize overlay and PVC mount, with revert support

**Plugin**: [ai-safety-skills](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Mount a component&#x27;s local manifests into the running ODH/RHOAI operator pod via a PVC and CSV patch, so the operator manages a developer&#x27;s custom manifests instead of its built-in ones.</p>
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
        <li>The operator pod comes back healthy after the CSV patch and manifest copy, running the custom manifests.</li>
        <li>fsGroup is derived from the namespace&#x27;s actual supplemental-groups range rather than a fixed value, so it works under restricted SCCs (e.g. ROSA).</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/deploy-component-manifests/SKILL.md" title="sheltoncyril/sheltons-toolkit@cec313e2f38d493acf8c8ad65bddb110903fb70a:skills/deploy-component-manifests/SKILL.md">SKILL.md @ cec313e<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Never apply the CSV volumeMount patch if it is already present — duplicate mounts crash the pod.</li>
        <li>Revert must remove JSON-patch indices in descending order to avoid index-shift corruption.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Bash, Read, Write, AskUserQuestion</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">oc</span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/deploy-component-manifests/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/deploy-component-manifests/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/deploy-component-manifests/resources/component-map.json"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/deploy-component-manifests/resources/component-map.json</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/deploy-component-manifests
```
