---
title: disconnected-readiness-scorer
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# disconnected-readiness-scorer

Score a repository's readiness for deployment in disconnected / air-gapped
OpenShift environments. Scans for five categories of disconnected-deployment
risks: image manifest completeness (CSV relatedImages or RELATED_IMAGE_* env
vars), digest enforcement (@sha256 vs mutable tags), runtime egress detection
(outbound HTTP calls in Go/Python/TS/shell), Python dependency validation
(unbundled pip packages), and operator manifest cross-referencing against the
opendatahub-operator source.

Automatically detects whether the target repo uses RELATED_IMAGE_* env vars
(opendatahub-operator pattern, threshold: 5+ occurrences in Go source) or
static CSV relatedImages lists. When the env var pattern is detected, the
orchestrator clones the opendatahub-operator repo and builds the authoritative
manifest (100+ env vars across 18 components), then cross-references target
repo image references against it. All rules exclude test files, CI config,
and lint rules from blocker-level findings.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: asanzgom
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Repository**: [opendatahub-io/disconnected-readiness-scorer](https://github.com/opendatahub-io/disconnected-readiness-scorer)
    - **Tags**: <span class="tag-pill">disconnected</span> <span class="tag-pill">air-gap</span> <span class="tag-pill">openshift</span> <span class="tag-pill">image-mirroring</span> <span class="tag-pill">readiness</span> <span class="tag-pill">scoring</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/disconnected-score`](disconnected-score.md) | Score a repository's readiness for disconnected / air-gapped OpenShift deployments | :material-check: |

## Installation

```bash
/plugin install disconnected-readiness-scorer@opendatahub-skills
```

## Architecture

The orchestrator (main.py) is the CLI entry point. It imports rule modules,
runs them, computes the aggregate score (READY / WARNING / NOT READY), and
renders output via a Jinja2 template (templates/report.md) with a built-in
micro-renderer fallback.

Each rule module under rules/ exports a run(repo_root) -> RuleResult function.
RuleResult is a dataclass with rule (name), passed (bool), and findings (list
of Finding). Each Finding has severity (blocker/warning/info), file, line,
image, and message fields.

Five rules:
- csv_relatedimages.py: auto-detects image management pattern (env var vs
  static CSV), checks completeness. Accepts optional manifest_env_vars from
  the orchestrator for cross-referencing against the operator manifest.
- operator_manifest.py: parses opendatahub-operator source to build the
  authoritative image manifest via build_manifest(). Returns a dict, not
  RuleResult; the orchestrator adapts it via adapt_manifest_result().
- no_image_tags.py: enforces @sha256 digest refs, rejects mutable tags.
- no_runtime_egress.py: detects outbound HTTP calls in Go/Python/TS/shell,
  distinguishes hardcoded URLs (blocker) from configurable ones (info).
- python_imports.py: validates Python deps against known-bundled list.

Config files in config/: known_mirrors.yaml (approved registries and PyPI
mirrors) and exceptions.yaml (per-repo rule exceptions for false positives).

Manifest cross-referencing flow: orchestrator detects env_var pattern →
clones opendatahub-operator to temp dir → builds manifest via
operator_manifest.build_manifest() → passes env var set to
csv_relatedimages.run() → three cross-reference checks: (A) image ref uses
var not in manifest → blocker, (B) repo defines var not in manifest →
warning (stale), (C) manifest vars not referenced → info.
