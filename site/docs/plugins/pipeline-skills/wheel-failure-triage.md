---
title: wheel-failure-triage
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# wheel-failure-triage

Collects structured wheel failures across GitLab build pipelines and
prepares one self-contained audit child job for PFA. Every occurrence
keeps its originating `source_pipeline_url` and producer job URL.
Shared descendants are followed once, and artifact requests use the
producing project's ID. Collection and missing evidence errors remain
visible in the report.

**Inputs**: GitLab CI pipeline context and original bootstrap artifacts.
**Outputs**: `failures.json`, `audit.yml`, the standalone audit CLI, and
the PFA pipeline response after notification.

**Plugin**: [pipeline-skills](index.md) | **:material-close: Internal**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Collect wheel failures from a root GitLab pipeline and its build descendants, prepare one audit child, and start PFA after the audit completes while preserving links to the originating pipelines.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">orchestrate</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>failures.json retains every occurrence&#x27;s source_pipeline_url and producer.job_url with available diagnostics.</li>
        <li>audit.yml defines one audit job that fails for a nonempty report and passes for a clean report.</li>
        <li>notify starts PFA after the audit completes, or uses the root pipeline when launch fails, and records the response.</li>
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
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">evidence_completeness</code>
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
        <li>Keep collection deterministic; do not group failures with an LLM or create audit jobs per failure group.</li>
        <li>Retain explicit collection and evidence errors rather than silently dropping them.</li>
        <li>Follow shared descendants once and read artifacts from the producing job&#x27;s project.</li>
        <li>Preserve the originating pipeline URL separately from the audit pipeline URL.</li>
        <li>Use BOT_PAT for GitLab API access and PFA pipeline creation; honor notification suppression settings.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Bash, Read</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/wheel-failure-triage/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/wheel-failure-triage/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/wheel-failure-triage/scripts/wheel_failure_triage.py"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/wheel-failure-triage/scripts/wheel_failure_triage.py</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/pipeline-skills/blob/main/skills/wheel-failure-triage/scripts/wheel_triage.py"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/wheel-failure-triage/scripts/wheel_triage.py</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

Internal CI workflow. Invoke the bundled `wheel_failure_triage.py` CLI
with `prepare`, `audit`, or `notify`. The collector copies the audit CLI
into its artifacts so the child uses only Python's standard library.
API collection and PFA handoff use `BOT_PAT`; `prepare` and `notify`
also require `requests` and `PyYAML`.
