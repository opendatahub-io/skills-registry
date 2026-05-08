---
title: rhoai-security-reviewer
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rhoai-security-reviewer

Consensus-based security review system for RHOAI strategy documents (STRATs).
Rather than relying on a single reviewer pass, this plugin uses an orchestrator
that extracts a mechanical threat surface inventory from the STRAT, then spawns
three independent security reviewers running in isolated forked contexts. Each
reviewer checks the STRAT against all 39 catalog risk patterns covering
authentication, data protection, cryptographic compliance (FIPS 140-3),
network security, supply chain, infrastructure, multi-tenant isolation,
agentic AI security, MCP security, and upstream component risk. Reviewers
also perform creative exploration for risks not covered by the catalog.

The orchestrator synthesizes reviewer findings using confidence tagging based
on cross-reviewer agreement: risks found by all three reviewers are HIGH
confidence, by two are MEDIUM, and by one are LOW. Severity is resolved by
majority vote. The final output includes a verdict (PASS / CONCERNS / FAIL),
a full review with consensus findings, and an actionable security requirements
file that is automatically attached to the Jira ticket. The system also
cross-references findings against a 47-item NFR checklist derived from 422
prior STRAT reviews, and adds idempotency labels to Jira for pipeline
integration.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: jctanner
    - **Category**: [Security Review](../../categories/security.md)
    - **Repository**: [jctanner/ai-first-pipeline](https://github.com/jctanner/ai-first-pipeline)
    - **Tags**: <span class="tag-pill">security</span> <span class="tag-pill">review</span> <span class="tag-pill">strat</span> <span class="tag-pill">threat-modeling</span> <span class="tag-pill">fips</span> <span class="tag-pill">compliance</span> <span class="tag-pill">consensus</span>

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

## Architecture

The plugin follows a two-skill architecture with a clear separation of concerns:

1. **strat-security-review** (orchestrator): Manages the full review lifecycle.
   It fetches the STRAT from Jira via Atlassian MCP, performs mechanical threat
   surface extraction (endpoints, services, data flows, credentials, CRDs,
   trust boundaries, RBAC, dependencies, agent/MCP surfaces), determines the
   review tier (Light / Standard / Deep), and spawns three isolated reviewer
   instances. After synthesis, it writes two output files (full review +
   requirements), attaches the requirements file to Jira, and adds verdict
   labels for downstream pipeline idempotency.

2. **security-reviewer** (worker): Runs in `context: fork` isolation on the
   `claude-opus-4-6` model. Each instance performs a two-phase analysis:
   Phase A discovers all potential concerns by checking every catalog pattern
   and performing creative exploration. Phase B applies a relevance gate
   (requiring specific STRAT citations and checking existing controls) and a
   severity decision tree. Architecture context from `.context/` is consulted
   for Standard/Deep tiers to avoid flagging already-mitigated controls.

The Light tier includes a short-circuit: if the threat surface inventory is
entirely empty, the orchestrator skips reviewer spawning and issues a direct
PASS verdict. Intermediate files (threat surface, individual reviewer outputs)
are preserved for auditability and calibration.
