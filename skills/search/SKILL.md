---
name: search
description: "搜尋研究 Wiki 相關頁面。觸發詞：wiki search, wiki 搜尋, find pages about。"
---

# Wiki Search

Search the wiki for relevant pages. Essential as the wiki grows beyond ~100 pages.

## Tier 1 — Built-in (always available)

1. Read `wiki/index.md` for topic overview
2. Use Grep tool to search markdown content and frontmatter
3. Parse frontmatter tags to filter by category

## Tier 2 — qmd (for large wikis)

[qmd](https://github.com/tobi/qmd) is a local markdown search engine with hybrid BM25/vector search.

```bash
# Install
brew install tobi/tap/qmd   # macOS
# Linux: build from source

# Index the wiki
qmd index <wiki-root>/wiki/

# Search via CLI
qmd search "query string"

# Or run as MCP server
qmd serve --mcp
```

When qmd is available, prefer it for semantic queries. Fall back to Grep when not installed.

## Output

Return a list of relevant pages with:
- Page title and path
- Relevance snippet (matching line or frontmatter excerpt)
- Status and tags
