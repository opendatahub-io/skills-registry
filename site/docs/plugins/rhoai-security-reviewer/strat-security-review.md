---
title: strat-security-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strat-security-review

Multi-reviewer consensus orchestrator for security review of RHOAI strategy
documents. Operates in four phases: (1) fetch the STRAT from Jira and extract
a mechanical threat surface inventory covering endpoints, services, data flows,
credentials, CRDs, trust boundaries, RBAC, external dependencies, and agent/MCP
surfaces; (2) determine review tier (Light/Standard/Deep) based on security
surface hints and effort size, then spawn three independent security-reviewer
instances in isolated forked contexts; (3) synthesize findings using confidence
tagging (HIGH=3/3, MEDIUM=2/3, LOW=1/3 reviewer agreement) with majority-vote
severity resolution; (4) write a full review and a requirements file, attach
requirements to Jira, and add idempotency labels (strat-security-pass,
strat-security-concerns, strat-security-fail).

Includes a Light tier short-circuit that skips reviewer spawning when the
threat surface inventory is entirely empty. Cross-references synthesized
findings against a 47-item NFR checklist derived from 422 prior reviews.
Five or more NFR gaps at Standard/Deep tier upgrade the verdict to CONCERNS.

**Plugin**: [rhoai-security-reviewer](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![strat-security-review diagram](strat-security-review.svg)
</div>

## Arguments

```bash
/strat-security-review <RHAISTRAT_KEY> [--force]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `RHAISTRAT_KEY` | :material-check: | - | RHAISTRAT Jira key identifying the strategy document to review (e.g., RHAISTRAT-400) |
| `--force` |  | `false` | Regenerate the security review even if one already exists for this STRAT |

## Usage

```bash
/strat-security-review RHAISTRAT-400
/strat-security-review RHAISTRAT-400 --force
```
