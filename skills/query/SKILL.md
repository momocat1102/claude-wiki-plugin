---
name: query
description: "查詢研究 Wiki 累積的知識，從多個頁面合成答案。觸發詞：wiki query, 查詢 wiki。"
---

# Wiki Query

Query the wiki and synthesize answers from accumulated knowledge.

## Flow

1. **Read `schema.md`** in the wiki root for conventions
2. **Read `wiki/index.md`** to identify relevant pages
3. If wiki has 100+ pages, use Grep to search content first
4. **Read relevant pages** (typically 3-10)
5. **Synthesize answer** with `[[wikilink]]` citations to specific wiki pages
6. **Choose output format** based on question type:

| Question Type | Format |
|--------------|--------|
| Explanatory | Prose with `[[wikilinks]]` |
| Comparison ("X vs Y") | Markdown table |
| Relationships / flows | Mermaid diagram (renders in Obsidian) |
| Quantitative | Chart via `/home/chunyen/.claude/skills/llm-wiki/scripts/wiki_viz.py` |
| Chronological | Timeline Callout（見 cmd-timeline.md） |
| Presentation | Marp slide deck in `ppt/` |
| Complex relationships | Obsidian `.canvas` JSON |

7. **Ask user**: "Want me to file this as a wiki page?" → if yes, save to `wiki/analyses/` with frontmatter, update `wiki/index.md` and `wiki/log.md`

Filing good answers back into the wiki is important — explorations compound just like ingested sources.

## Page Format for Filed Analyses

```yaml
title: "Analysis Title"
type: analysis
tags: [relevant, tags]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [pages-referenced]
status: solid
```

## Log Entry

```markdown
## [YYYY-MM-DD] query | Question Summary
- Answer filed: analyses/analysis-slug.md (or "not filed")
- Pages referenced: [[page1]], [[page2]], ...
```
