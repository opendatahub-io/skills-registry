---
title: security-diff-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# security-diff-review

Security-only review of the committed changes on a branch, PR or MR. One finder subagent looks for exploitable vulnerabilities the change introduces, one false-positive filter subagent per finding scores it, and only findings scoring 8 or more out of 10 are kept. Repos tune exclusions and precedents in REVIEW.md at the base ref.


**Plugin**: [code-review-skills](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Find exploitable vulnerabilities that a committed change introduces and keep only those an independent filter scores 8 or more out of 10 under the exclusion rules.</p>
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
        <li>Reports each kept finding with its file, line, severity, exploit scenario and recommendation, or says plainly that none were found.</li>
        <li>Says the review did not complete when the diff command is refused or the merge base is missing.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/code-review-skills/blob/aeba1914f60b23473fc8539aeeac572bd9d655f9/skills/security-diff-review/references/filter.md" title="opendatahub-io/code-review-skills@aeba1914f60b23473fc8539aeeac572bd9d655f9:skills/security-diff-review/references/filter.md">filter.md @ aeba191<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">evidence_completeness</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/code-review-skills/blob/aeba1914f60b23473fc8539aeeac572bd9d655f9/skills/security-diff-review/references/finder.md" title="opendatahub-io/code-review-skills@aeba1914f60b23473fc8539aeeac572bd9d655f9:skills/security-diff-review/references/finder.md">finder.md @ aeba191<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>The finder and filters are read-only and run nothing that executes the code under review.</li>
        <li>REVIEW.md overrides are read from the base ref only.</li>
        <li>An exclusion rule is a veto that no other check can override.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Bash, Read, Grep, Glob, Agent</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">git</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/code-review-skills/blob/aeba1914f60b23473fc8539aeeac572bd9d655f9/skills/security-diff-review/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/security-diff-review/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/code-review-skills/blob/aeba1914f60b23473fc8539aeeac572bd9d655f9/skills/security-diff-review/references/finder.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/security-diff-review/references/finder.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/code-review-skills/blob/aeba1914f60b23473fc8539aeeac572bd9d655f9/skills/security-diff-review/references/filter.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/security-diff-review/references/filter.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/security-diff-review
```
