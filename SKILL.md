---
name: wiki
description: >
  建立和維護結構化的研究 Wiki（Obsidian vault），將知識從各種來源逐步編譯成互相連結的 Markdown 頁面。
  觸發詞：/wiki:init, /wiki:ingest, /wiki:timeline, /wiki:search, /wiki:query, /wiki:status,
  /wiki:lint, /wiki:viz, /wiki:ppt, "加入 wiki", "wiki 搜尋", "wiki 狀態", "記錄進度", "wiki 簡報",
  "wiki 健檢", "wiki 圖表", 或任何與研究 wiki 相關的操作。
---

# LLM Wiki — Main Router

Build persistent, compounding research knowledge bases with Obsidian as your IDE.

Instead of re-deriving knowledge from raw documents every query (like RAG), the LLM
**incrementally builds a wiki** — reading sources, extracting key information, and
integrating it into existing pages. Knowledge is compiled once and kept current.

> Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

## Language

所有 wiki 內容用**繁體中文**撰寫。技術專有名詞保留英文。
所有 sub-commands 繼承此規則，無需重複宣告。

## 共用慣例

### Wikilinks
永遠用 Obsidian wikilinks：`[[page-name]]` 或 `[[page-name|顯示文字]]`
Obsidian 依檔名解析，不需相對路徑。提到任何有自己頁面的實體/概念時都要連結。

### Frontmatter（所有 wiki 頁面）

```yaml
---
title: "Page Title"
type: entity|concept|source|analysis|overview
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [source-slug-1]
status: stub|draft|solid|comprehensive
---
```

**Status 等級**：`stub`（剛建立）→ `draft`（資料不足）→ `solid`（來源充足）→ `comprehensive`（全面覆蓋）

### 頁面分類
- `entities/` — 人物、組織、工具、模型、資料集
- `concepts/` — 技術、理論、模式、術語
- `sources/` — 每個來源一頁
- `analyses/` — 查詢結果、比較分析
- `references/` — 參考手冊、檔案地圖

### log.md 慣例
每次操作追加一條記錄，格式：
```markdown
## [YYYY-MM-DD] <operation> | <title>
- [details]
```

### 投影片關聯
投影片存在 `ppt/<名稱>/`，索引在 `wiki/references/slide-index.md`。

- **新增投影片時**：更新 slide-index.md 的表格 + 在相關 wiki 頁面加「相關投影片」連結
- **Timeline entry**：如果進度有對應的投影片，在 entry 加 `**投影片**：ppt/<名稱>/`
- **Concept/Entity 頁面**：底部可加 `## 相關投影片` 區段

## Sub-commands

根據使用者意圖，讀取對應的 reference 檔案後再執行：

| 指令 | 觸發詞 | Reference |
|------|--------|-----------|
| init | wiki init, new wiki, 建 wiki, start a wiki | `references/cmd-init.md` |
| ingest | ingest, 加入 wiki, 讀這篇論文, add to wiki, process this source | `references/cmd-ingest.md` |
| timeline | 記錄進度, timeline, 記一下, wiki timeline, 更新時程, 今天做了什麼 | `references/cmd-timeline.md` |
| search | wiki search, 搜尋 wiki, find pages about | `references/cmd-search.md` |
| query | wiki query, 查詢 wiki, what do we know about, compare X and Y | `references/cmd-query.md` |
| status | wiki status, wiki 狀態, how's the wiki | `references/cmd-status.md` |
| lint | wiki lint, 檢查 wiki, wiki 健檢, check wiki health | `references/cmd-lint.md` |
| viz | wiki viz, wiki graph, wiki 圖表, visualize the wiki | `references/cmd-viz.md` |
| ppt | wiki ppt, wiki slides, wiki 簡報, make a presentation | `references/cmd-ppt.md` |

讀取 reference 檔案後，照其中的 Flow 執行。

## Wiki 目錄結構

```
<wiki-root>/
├── schema.md                  # 本 wiki 的慣例（LLM 每次先讀）
├── raw/                       # 不可變的原始來源
│   └── assets/                # 從來源下載的圖片
├── wiki/                      # LLM 維護的頁面
│   ├── index.md               # 分類目錄
│   ├── log.md                 # 操作記錄（時間序）
│   ├── overview.md            # 所有知識的高層次合成
│   ├── timeline.md            # 專案時程（Timeline Callout 格式）
│   ├── entities/
│   ├── concepts/
│   ├── sources/
│   ├── analyses/
│   ├── references/
│   └── assets/                # 生成的圖表（PNG/SVG）
├── ppt/                       # 投影片
└── outputs/                   # PPTX 匯出、報告
```

預設 wiki root：`~/wikis/<topic-name>/`

## Source Summary Frontmatter（ingest 使用）

```yaml
---
title: "Source Title"
type: source
source_type: paper|article|note|report|talk|book|video|podcast
authors: [Author 1, Author 2]
date: YYYY-MM-DD
url: "original URL"
tags: [relevant, tags]
key_claims:
  - "Claim 1"
  - "Claim 2"
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
status: solid
---
```

## Critical Behaviors

- **Wikilinks**: 任何有自己頁面的實體/概念都要用 `[[page-name]]` 連結
- **Contradictions**: 新資訊與現有 wiki 矛盾時，在兩頁都加 `> [!warning] Contradiction` callout，絕不靜默覆蓋
- **Citations**: 每頁底部都要有 Sources 區段，含 `[[sources/slug]]` 連結
- **Status tracking**: 新頁面設 `stub`，有一定內容設 `draft`，來源充足設 `solid`

## Timeline Callout 格式

`timeline.md` 使用 Timeline Callout CSS（非 Mermaid）呈現里程碑。
CSS 位於 wiki 的 `.obsidian/snippets/timeline-callout.css`。
詳細格式、顏色對照、入口格式見 `references/cmd-timeline.md`。

## Version History

wiki 是 git repo。`/wiki:init` 時執行 `git init`。
建議每次重要 ingest 後 commit，用 `git log` 追蹤演進。
