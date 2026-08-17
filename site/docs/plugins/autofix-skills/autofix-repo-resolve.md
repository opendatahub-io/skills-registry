---
title: autofix-repo-resolve
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# autofix-repo-resolve

Decide which repository a Jira bug ticket is actually about when its
description and comments mention several. Reads .autofix-context/ticket.json
and .autofix-context/repo-candidates.json, classifies every candidate URL as
target, contextual, negative, or unclear, then writes a verdict with the
chosen target, a confidence level, and the reasoning behind it. Text analysis
only — never clones or otherwise accesses a candidate repository. The verdict
is schema-validated by write_json.py and validate_verdict.py.

**Plugin**: [autofix-skills](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Decide which single repository a Jira bug ticket is actually about when its description and comments mention several, classifying every candidate URL and recording the chosen target with a confidence level and reasoning.</p>
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
        <li>Writes .autofix-context/repo-resolve-verdict.json with target_url, confidence, reasoning, and a classification for every candidate URL.</li>
        <li>Classifies each candidate as target, contextual, negative, or unclear rather than only naming the winner.</li>
        <li>Passes scripts/write_json.py schema validation and scripts/validate_verdict.py, correcting the JSON and re-validating on failure.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--verifier_backed">verifier_backed</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/autofix-skills/blob/fcabad95d8d15b0f3873fa7361afd08ff586c9c0/skills/autofix-repo-resolve/scripts/validate_verdict.py" title="opendatahub-io/autofix-skills@fcabad95d8d15b0f3873fa7361afd08ff586c9c0:skills/autofix-repo-resolve/scripts/validate_verdict.py">validate_verdict.py @ fcabad9<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Text analysis only: never clone or otherwise access any candidate repository.</li>
        <li>Classify every candidate URL, not just the selected target.</li>
        <li>Parse Jira markup links as well as plain URLs when reading candidates out of ticket text.</li>
        <li>Treat a matching Jira component name as a signal only, never as the sole basis for high confidence.</li>
        <li>Still name the most likely candidate when confidence is low, recording the ambiguity in reasoning.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Bash</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">uv</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">task_input<span class="skill-contract__privacy">organization_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/autofix-skills/blob/fcabad95d8d15b0f3873fa7361afd08ff586c9c0/skills/autofix-repo-resolve/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/autofix-repo-resolve/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/autofix-skills/blob/fcabad95d8d15b0f3873fa7361afd08ff586c9c0/skills/autofix-repo-resolve/schemas/repo-resolve-verdict.json"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/autofix-repo-resolve/schemas/repo-resolve-verdict.json</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/autofix-skills/blob/fcabad95d8d15b0f3873fa7361afd08ff586c9c0/skills/autofix-repo-resolve/scripts/validate_verdict.py"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/autofix-repo-resolve/scripts/validate_verdict.py</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/autofix-skills/blob/fcabad95d8d15b0f3873fa7361afd08ff586c9c0/skills/autofix-repo-resolve/scripts/write_json.py"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/autofix-repo-resolve/scripts/write_json.py</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/autofix-repo-resolve
```
