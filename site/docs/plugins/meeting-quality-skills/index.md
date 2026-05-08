---
title: meeting-quality-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# meeting-quality-skills

Pre-meeting skills for improving meeting quality by shifting recurring status
meetings away from general reporting and toward exception-based discussion.
The plugin provides two complementary skills: one checks a shared update
document to identify attendees who have not provided async updates, and the
other analyzes collected updates to generate a risk-focused agenda that
prioritizes blockers and at-risk items.

Both skills work with Google Docs or pasted text, and handle edge cases such
as Jira-exported content (issue keys, dashboards, JQL output) by attempting
to extract owners from fields like Assignee or Owner. When ownership cannot
be determined, items are flagged as uncertain rather than silently dropped.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: Arjay Hinek
    - **License**: Apache-2.0
    - **Category**: [Product Planning](../../categories/planning.md)
    - **Repository**: [ahinek/meeting-quality-skills](https://github.com/ahinek/meeting-quality-skills)
    - **Tags**: <span class="tag-pill">meeting</span> <span class="tag-pill">google-workspace</span> <span class="tag-pill">agenda</span> <span class="tag-pill">async-updates</span> <span class="tag-pill">productivity</span>

## Pipeline

<div class="diagram-container" markdown>
![meeting-quality-skills pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/meeting-async-update-check`](meeting-async-update-check.md) | Check a shared update doc and identify attendees missing async updates before a status meeting | :material-check: |
| [`/meeting-risk-agenda`](meeting-risk-agenda.md) | Analyze pre-meeting updates and generate a risk-focused agenda by identifying blocked and at-risk items | :material-check: |

## Installation

```bash
/plugin install meeting-quality-skills@opendatahub-skills
```

## Architecture

The two skills operate independently but form a natural pre-meeting workflow:
first run meeting-async-update-check to ensure updates are in, then run
meeting-risk-agenda to build a focused agenda from those updates. Both skills
are purely prompt-driven with no external tool dependencies — they rely on
the LLM's ability to parse unstructured document content and apply
classification heuristics (name matching, risk-signal detection).
