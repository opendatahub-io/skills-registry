<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# meeting-quality-skills

Skills for evaluating meeting quality and optimizing async collaboration.
Analyzes meeting agendas for risk factors and checks whether meetings
could be replaced with async updates.


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
