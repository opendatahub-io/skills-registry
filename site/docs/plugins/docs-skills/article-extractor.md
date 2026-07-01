---
title: article-extractor
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# article-extractor

Downloads HTML from a public URL and extracts the main article content,
stripping navigation, styling, and other bloat. Targets semantic
`<article>` tags (by default `article[aria-live="polite"]`, as used on
Red Hat docs) but accepts any CSS selector. Outputs clean Markdown, HTML,
or plain text — useful for archiving docs, migrating content, or feeding
pages into analysis. Backed by a PEP 723 script using requests +
BeautifulSoup (+ html2text for Markdown).

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![article-extractor diagram](article-extractor.svg)
</div>

## Arguments

```bash
/article-extractor --url <url> [--format html|markdown|text] [--output <file>] [--selector <css>] [--strip-links]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--url` | :material-check: | - | The page URL to fetch and extract. |
| `--format` |  | `markdown` | Output format. |
| `--output` |  | - | Write to a file instead of stdout. |
| `--selector` |  | `article[aria-live="polite"]` | CSS selector for the article element. |
| `--strip-links` |  | `false` | Remove all hyperlinks from the output. |

## Usage

```bash
article_extractor.py --url https://docs.redhat.com/.../install --format markdown --output install.md
article_extractor.py --url https://example.com/docs/guide --selector article.documentation --format text
```
