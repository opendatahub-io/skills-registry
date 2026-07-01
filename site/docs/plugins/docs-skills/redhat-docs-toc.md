---
title: redhat-docs-toc
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# redhat-docs-toc

Extracts distinct article URLs from a Red Hat documentation table-of-contents
page. Downloads the page, locates the `<nav id="toc">` element, parses all
links, filters out anchors/section-fragments/index pages, converts relative
to absolute URLs, deduplicates, and returns an alphabetically sorted list
(JSON or plain list). Pairs with `article-extractor` to crawl and download a
whole documentation section. PEP 723 script (requests, BeautifulSoup).

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![redhat-docs-toc diagram](redhat-docs-toc.svg)
</div>

## Arguments

```bash
/redhat-docs-toc --url <url> [--output <file>] [--format json|list]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--url` | :material-check: | - | Red Hat docs TOC/index URL to extract from. |
| `--output` |  | - | Write to a file instead of stdout. |
| `--format` |  | `json` | Output format. |

## Usage

```bash
toc_extractor.py --url https://docs.redhat.com/.../guide/index
toc_extractor.py --url https://docs.redhat.com/.../configure/index --format list
```
