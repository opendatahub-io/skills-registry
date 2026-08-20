---
title: configure-disconnected
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# configure-disconnected

Configure the RHCL operator for disconnected/air-gapped OpenShift environments (WASM shim patching, pull secret propagation, mirror registry)

**Plugin**: [ai-safety-skills](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Point the RHCL operator&#x27;s WASM shim and pull secret at a disconnected environment&#x27;s mirror registry, then verify the subscription env vars, pull secret, and operator pods reflect the change.</p>
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
        <li>The subscription&#x27;s RELATED_IMAGE_WASMSHIM and PROTECTED_REGISTRY reflect the mirror registry after the script runs.</li>
        <li>The mirror registry URL is always used without a scheme prefix.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/configure-disconnected/SKILL.md" title="sheltoncyril/sheltons-toolkit@cec313e2f38d493acf8c8ad65bddb110903fb70a:skills/configure-disconnected/SKILL.md">SKILL.md @ cec313e<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Never assume the Subscription&#x27;s namespace equals the CSV&#x27;s namespace; resolve it directly.</li>
        <li>Never include http:// or https:// in the mirror registry value passed to the script.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Bash, Read, AskUserQuestion</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">oc, jq</span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/configure-disconnected/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/configure-disconnected/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Usage

```bash
/configure-disconnected
```
