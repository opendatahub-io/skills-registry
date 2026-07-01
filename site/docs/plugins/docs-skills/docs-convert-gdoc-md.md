---
title: docs-convert-gdoc-md
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-convert-gdoc-md

Reads a Google Docs document, Google Slides presentation, or Google Sheets
spreadsheet and converts it to Markdown (Docs/Slides) or CSV (Sheets),
auto-detecting the type from the URL. Slides are exported via PPTX with slide
titles, bullets, tables, and speaker notes. Authenticates via the `gcloud`
CLI (`gcloud auth login --enable-gdrive-access`) or Google Application
Default Credentials. Optionally pulls Google Docs comment threads and inserts
them as Markdown footnotes anchored to the quoted text.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-convert-gdoc-md diagram](docs-convert-gdoc-md.svg)
</div>

## Arguments

```bash
/docs-convert-gdoc-md [--comments] [--include-resolved] <url> [<output_file>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `url` | :material-check: | - | Google Docs, Slides, or Sheets URL (type auto-detected from the path). |
| `output_file` |  | - | Output path. Defaults to <id>.md or <id>.csv. |
| `--comments` |  | `false` | Pull Google Docs comment threads and insert them as footnotes (Docs only). |
| `--include-resolved` |  | `false` | Include resolved comment threads (with --comments). |

## Usage

```bash
gdoc2md.py "https://docs.google.com/document/d/.../edit"
gdoc2md.py --comments "https://docs.google.com/document/d/.../edit"
gdoc2md.py "https://docs.google.com/spreadsheets/d/.../edit" data.csv
```
