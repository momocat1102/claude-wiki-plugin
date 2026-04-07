---
name: lint
description: "研究 Wiki 健康檢查，找矛盾、孤立頁面、壞掉的 wikilinks。觸發詞：wiki lint, wiki 健檢。"
---

# Wiki Lint

Health-check the wiki and fix issues.

## Checks

1. **Contradictions** — claims in one page that conflict with another
2. **Stale content** — pages not updated by recent sources that should have been
3. **Orphan pages** — pages with no inbound `[[wikilinks]]` from other pages
4. **Missing pages** — entities/concepts frequently mentioned via `[[link]]` but page doesn't exist
5. **Broken wikilinks** — `[[references]]` to pages that don't exist
6. **Missing cross-references** — related pages that should link to each other but don't
7. **Thin coverage** — topic areas with few or no sources
8. **Frontmatter issues** — missing required fields, inconsistent tags
9. **Unreferenced images** — images in `raw/assets/` not embedded anywhere

## Output

Generate a health report with:
- Overall stats (page count by category, source count, avg links per page)
- Issues found, ranked by severity (high/medium/low)
- Suggested actions for each issue
- Optionally: a knowledge coverage Mermaid diagram

Use Obsidian callouts in the report:
- `> [!danger]` for contradictions
- `> [!warning]` for broken links, orphans
- `> [!info]` for suggestions

## After Report

1. Present the report to the user
2. Ask which issues to fix
3. Fix the selected issues (create missing pages, add links, resolve contradictions)
4. Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] lint | Health Check
- Issues found: X high, Y medium, Z low
- Issues fixed: [list]
- Suggestions: [new sources to find, questions to investigate]
```

Also suggest: new questions to investigate, new sources to look for, data gaps worth filling.
