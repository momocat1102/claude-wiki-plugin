---
name: ppt
description: "從研究 Wiki 內容生成投影片，支援 Marp 和 PPTX。觸發詞：wiki ppt, wiki 簡報。"
---

# Wiki PPT

Generate a presentation from wiki content. Two output formats available.

## Option 1: Marp (default — stays in Obsidian)

Marp turns markdown into slide decks. Obsidian renders with the Marp Slides plugin.

1. Read relevant wiki pages based on the topic
2. Design slide structure:
   - Title + subtitle
   - Context / background (1-2 slides)
   - Key findings (3-7 slides, one main point each)
   - Comparisons / analysis (if relevant)
   - Open questions / next steps
3. Write Marp markdown to `ppt/<topic>.md`:

```markdown
marp: true
theme: default
paginate: true

# Title

Subtitle or context


# Key Finding 1

- Point with [[wikilink]] citation
- Supporting evidence


![bg right:40%](wiki/assets/chart.png)

# Visual Analysis

Insights from the chart


# Open Questions

- What remains to investigate
- Next sources to ingest
```

4. Tell user to open in Obsidian → Marp plugin renders as presentation
5. Export options: `marp ppt/<topic>.md --pptx` or `--pdf` via Marp CLI

## Option 2: PPTX (for external sharing)

1. Read relevant wiki pages
2. Design slide structure (same as above)
3. Generate PPTX via `python-pptx` (`pip install python-pptx` if needed)
4. Include diagrams from `wiki/assets/`
5. Save to `outputs/<topic>-<date>.pptx`

Use PPTX only when user specifically needs it for external sharing. Default to Marp.

## 更新 slide-index.md

產出投影片後，在 `wiki/references/slide-index.md` 的表格追加一行：

```markdown
| MM-DD | `ppt/<topic>/` | 主題描述 | 頁數 | [[concepts/xxx]], [[entities/yyy]] |
```

## Log Entry

```markdown
## [YYYY-MM-DD] ppt | Presentation: <topic>
- Output: ppt/<topic>.md (Marp) or outputs/<topic>.pptx
- Pages referenced: [[page1]], [[page2]], ...
- Slide index updated: wiki/references/slide-index.md
```
