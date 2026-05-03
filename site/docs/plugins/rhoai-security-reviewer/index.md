<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rhoai-security-reviewer

Consensus-based security review for RHOAI strategy documents (STRATs). An orchestrator spawns three independent reviewers to identify security risks, then synthesizes findings with confidence tagging based on cross-reviewer agreement. Covers 39 catalog patterns across auth, data protection, cryptographic compliance, network security, supply chain, and infrastructure.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: jctanner
    - **Category**: [Security Review](../../categories/security.md)
    - **Repository**: [jctanner/ai-first-pipeline](https://github.com/jctanner/ai-first-pipeline)
    - **Tags**: security, review, strat, threat-modeling, fips, compliance, consensus

## Pipeline

<div class="diagram-container" markdown>
![rhoai-security-reviewer pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/strat-security-review`](strat-security-review.md) | Multi-reviewer consensus orchestrator for security review of STRAT documents. Extracts threat surfaces, spawns three independent security-reviewer instances, synthesizes findings with confidence levels, and produces a final verdict (PASS/CONCERNS/FAIL). | :material-check: |
| [`/security-reviewer`](security-reviewer.md) | Individual security reviewer that assesses RHOAI strategy documents against 39 catalog patterns covering authentication, data protection, cryptographic compliance, network security, supply chain, and infrastructure. Uses a two-phase discovery-then-filter approach with severity classification. | :material-check: |

## Installation

```bash
/plugin install rhoai-security-reviewer@opendatahub-skills
```
