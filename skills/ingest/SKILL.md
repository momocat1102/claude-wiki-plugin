---
name: ingest
description: "將來源文件加入研究 Wiki，提取關鍵資訊，整合到現有頁面。觸發詞：ingest this, add to wiki, wiki ingest, 加入 wiki, 讀這篇論文。"
---

# Wiki Ingest

Process a source into the wiki. This is the most important wiki operation — it's how
knowledge accumulates.

## Source Types

- **File path** — PDF, markdown, text, images (use Read tool)
- **URL** — fetch via WebFetch, convert to markdown
- **Web Clipper** — user clipped article via Obsidian Web Clipper → already in `raw/`
- **Pasted text** — user pastes content directly in conversation

## Flow

1. **Read `schema.md`** in the wiki root to understand conventions and tag taxonomy
2. **Read the source document**
   - For PDFs: use Read with page ranges for large documents
   - For URLs: use WebFetch
3. **Share 3-5 key takeaways** with the user, ask what to emphasize
4. **Execute updates** (typically touches 5-15 pages):

| Step | Action |
|------|--------|
| **Source summary** | Create `wiki/sources/<source-slug>.md` with full frontmatter |
| **Entities** | Create or update pages in `wiki/entities/` for each notable entity (people, tools, models, papers, benchmarks) |
| **Concepts** | Create or update pages in `wiki/concepts/` for each key concept/technique |
| **Overview** | Revise `wiki/overview.md` if the source shifts the big picture |
| **Index** | Add entries for all new pages to `wiki/index.md` |
| **Log** | Append entry to `wiki/log.md` |

5. **Report** what was created/updated; **flag any contradictions** with existing knowledge

## Source Summary Frontmatter

See main `SKILL.md` for the full `source` frontmatter template.

## Critical Behaviors

- **Wikilinks**: Always use `[[page-name]]` or `[[page-name|Display Text]]`. When mentioning any entity/concept that has its own page, link it.
- **Contradictions**: When new info contradicts existing wiki content, add a `> [!warning] Contradiction` callout to both pages. Never silently overwrite.
- **Citations**: Every wiki page must have a "Sources" section at the bottom with `[[sources/slug]]` links.
- **Status tracking**: Set `status: stub` for new pages with minimal content, `draft` for pages with some info, `solid` for well-supported pages.

## Image Handling

- Download images to `raw/assets/` with descriptive filenames
- Embed in wiki pages: `![[image-name.png]]`
- LLMs can't read markdown with inline images in one pass — read text first, then view referenced images separately via Read tool
- After ingesting a web-clipped article, remind user to hit `Ctrl+Shift+D` in Obsidian to download remote images locally

## Log Entry Format

```markdown
## [YYYY-MM-DD] ingest | Source Title
- Pages created: entity/foo.md, concept/bar.md
- Pages updated: overview.md, entity/baz.md
- Key additions: [brief summary of what changed]
```

## Determining Which Wiki

If the user has multiple wikis, determine which one from context (current directory, topic mentioned). If ambiguous, ask.
