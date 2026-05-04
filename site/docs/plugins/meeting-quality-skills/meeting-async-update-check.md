<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# meeting-async-update-check

Check whether a meeting could be replaced with an async update.
Validates that attendees have provided their updates in the shared document.

**Plugin**: [meeting-quality-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![meeting-async-update-check diagram](meeting-async-update-check.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `meeting_title` | :material-check: | — | Title of the meeting |
| `meeting_datetime` | :material-check: | — | Meeting date and time |
| `attendee_list` | :material-check: | — | List of meeting attendees |
| `update_document` | :material-check: | — | Shared meeting update document content or link |

## Usage

```
/meeting-async-update-check
```
