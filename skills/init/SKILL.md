---
name: init
description: "初始化新的 LLM Wiki（Obsidian vault）。建立目錄結構、schema、種子頁面、git repo。觸發詞：wiki init, new wiki, 建 wiki。"
---

# Wiki Init

Create a new research wiki (Obsidian vault) for a topic.

## Flow

1. **Confirm with user:**
   - Topic name (becomes directory name, kebab-case)
   - Location (default: project root — wiki files go into `wiki/`, `raw/`, `schema.md` alongside existing project structure)
   - Initial scope — what aspects to focus on
   - Any initial sources to ingest

2. **Create directory structure:**
```
<wiki-root>/
├── schema.md
├── raw/
│   └── assets/
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── overview.md
│   ├── timeline.md              ← 專案時程（Timeline Callout 格式）
│   ├── entities/
│   ├── concepts/
│   ├── sources/
│   ├── analyses/
│   ├── references/
│   │   └── project-file-map.md  ← 專案檔案地圖
│   ├── assets/
│   └── .obsidian/
│       └── snippets/
│           └── timeline-callout.css  ← Timeline 視覺樣式
├── ppt/
└── outputs/
```

3. **Generate `schema.md`** from the template at `/home/chunyen/.claude/skills/llm-wiki/references/schema_template.md`. Customize for the topic:
   - Replace `{{TOPIC}}` with the topic name
   - Replace `{{SCOPE}}` with the agreed scope
   - Customize `{{CATEGORIES_ENTITIES}}` and `{{CATEGORIES_CONCEPTS}}` for the domain
   - Add domain-specific tag taxonomy

4. **Create seed pages:**
   - `wiki/index.md` — empty catalog with Dataview table at bottom（含時程、參考手冊區段）
   - `wiki/log.md` — first entry: init
   - `wiki/overview.md` — seed with known context about the topic
   - `wiki/timeline.md` — 專案時程頁，用 `[!timeline|color]` Callout 格式（見 `cmd-timeline.md`）
   - `wiki/references/project-file-map.md` — 掃描專案目錄結構，記錄每個目錄的用途、產生方式（手寫/AI/腳本）、狀態
   - `wiki/references/slide-index.md` — 投影片索引（初始為空表格：日期/投影片/主題/頁數/關聯頁面）
   - `wiki/.obsidian/snippets/timeline-callout.css` — 複製自 `/home/chunyen/.claude/skills/llm-wiki/assets/timeline-callout.css`

5. **Init git:** `git init` in the wiki root

6. **更新專案 CLAUDE.md**：在專案的 CLAUDE.md 加入 wiki 說明區塊，讓新 session 的模型知道 wiki 的存在和用法。如果 CLAUDE.md 不存在就建立。追加以下內容：

```markdown
## 研究 Wiki（專案知識庫）

本專案有一個結構化的研究 Wiki，用 Obsidian 瀏覽，是專案的知識中心。

- **位置**：`<wiki-root>/wiki/`
- **用途**：集中管理專案知識——設計文件、實驗結果、文獻調研、進度追蹤、檔案地圖
- **查詢**：回答研究相關問題前，先用 Grep 搜尋 wiki 或用 `/wiki-search`
- **更新**：完成實驗或設計決策後，用 `/wiki-ingest` 或 `/wiki-timeline` 更新
- **索引**：`wiki/index.md` 列出所有頁面
- **時程**：`wiki/timeline.md` 記錄每日重大進度
- **投影片**：`wiki/references/slide-index.md` 關聯所有投影片

Wiki 的內容比 CLAUDE.md 更詳細。遇到專案相關的問題，優先查 wiki。
```

根據實際的 wiki 路徑和專案名稱調整。

7. **Guide Obsidian setup:**
   - Tell user: "Open this folder as a vault in Obsidian: `<path>`"
   - Required plugins: **Dataview**, **Marp Slides**
   - Recommended: **Obsidian Web Clipper** (browser extension for clipping articles)
   - Settings to configure:
     - Files and links → Default attachment location: `raw/assets/`
     - Files and links → Use `[[Wikilinks]]`: ON
     - Hotkeys → bind "Download attachments" to `Ctrl+Shift+D`
   - Show them Graph View: `Ctrl+G`

7. If initial sources provided, proceed to ingest (use `cmd-ingest.md`)

## Page Format Convention

All wiki pages use YAML frontmatter + `[[wikilinks]]` — see main `SKILL.md` for the full template.

```markdown
# Page Title

Content with [[wikilinks]] to other pages.

## Sources
- [[sources/source-slug]]
```
