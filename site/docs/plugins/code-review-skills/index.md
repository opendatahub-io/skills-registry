---
title: code-review-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# code-review-skills

AI-powered code review for GitLab merge requests. Reviews all commits since the
base branch, produces structured JSON feedback with severity-tagged inline
comments, and posts results to the GitLab MR (in CI) or displays them locally
for preview. Designed to run as a job in a GitLab CI code-review pipeline, but
also works locally for previewing review output before pushing.

The skill reviews only the committed diff between branches (never uncommitted
working-tree changes), writes a strict-schema JSON review to
/tmp/ai-review-output.json, then hands off to a deterministic Python script
(review.py) that validates the JSON, applies chill-mode filtering, deduplicates
against previous reviews, deletes prior AI review discussions, and posts inline
comments plus a summary note to the MR. When no CI platform is detected, it
falls back to a formatted terminal display.


!!! info "Plugin Details"

    - **Version**: 0.2.1
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Code Quality](../../categories/code-quality.md)
    - **Repository**: [opendatahub-io/code-review-skills](https://github.com/opendatahub-io/code-review-skills)
    - **Tags**: <span class="tag-pill">code-review</span> <span class="tag-pill">gitlab</span> <span class="tag-pill">ci</span> <span class="tag-pill">merge-request</span> <span class="tag-pill">security</span> <span class="tag-pill">subagents</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/gitlab-code-review`](gitlab-code-review.md) | Perform AI code review on a GitLab merge request with structured JSON feedback and inline comments | :material-check: |
| [`/code-review-panel`](code-review-panel.md) | Risk-tiered review panel for the committed changes on a branch, PR or MR. A triage script picks the tier (quick, standard or deep) and the lenses, one read-only finder subagent runs per lens, skeptic subagents verify each finding, and the ranked report blocks on security. Can write gitlab-code-review JSON for posting. | :material-check: |
| [`/security-diff-review`](security-diff-review.md) | Security-only review of the committed changes on a branch, PR or MR. One finder subagent looks for exploitable vulnerabilities the change introduces, one false-positive filter subagent per finding scores it, and only findings scoring 8 or more out of 10 are kept. Repos tune exclusions and precedents in REVIEW.md at the base ref. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install code-review-skills@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `code-review-skills` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```

## Architecture

Single-skill plugin with a clean split between LLM judgment and deterministic
posting. SKILL.md is the orchestrator: it instructs the agent to inspect the
git diff (git log / git diff against the base branch, using
$CI_MERGE_REQUEST_DIFF_BASE_SHA in CI), produce structured JSON output matching
a fixed schema (summary, positive_aspects, inline_comments with
file/line/severity/comment, optional fix_prompt), and invoke the posting script.

scripts/review.py handles all deterministic work: JSON parsing and validation,
chill-mode filtering (CHILL_MODE env var, default true, drops suggestion-level
comments), platform auto-detection (GitLab CI, GitHub, or local), deduplication
against previous reviews (skips comments on unchanged code), deletion of prior
AI review discussions on the MR, and posting inline comments + summary to the
GitLab MR. It is invoked directly (./scripts/review.py) rather than via python
so the uv shebang manages dependencies. Requires python3, uv, and git; CI
posting requires GITLAB_API_TOKEN.

Inline comments must reference new-side line numbers and only target lines in
the diff. Severity levels: critical (security/build-breaking), major (logic
errors, pattern violations), minor (style), suggestion (optional). In CI, the
GitLab CI_* environment variables are set automatically.
