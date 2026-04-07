---
name: timeline
description: "記錄專案時程到 Wiki 的 timeline.md。追加今天的重大進度、決策、實驗結果或里程碑。觸發詞：記錄進度, timeline, 記一下, 更新時程。"
---

# Wiki Timeline

在研究 wiki 的 `timeline.md` 追加今日進度記錄。這是專案演進的時間軸，讓未來回顧時能快速掌握每一天的重大變化。

## Flow

1. **找到 wiki**：搜尋 `**/wiki/timeline.md`，確認路徑
2. **讀取 timeline.md**：了解現有格式和最後一筆日期
3. **收集今日進度**：
   - 如果使用者有明確說明要記什麼 → 用那個
   - 如果沒有 → 回顧本次對話中完成的工作，提煉重大進度
4. **追加 entry**：在 `timeline.md` 的 `## Callout 圖例` 上方、既有日期 entry 之前插入（reverse chronological）
5. **更新 log.md**：追加 `## [YYYY-MM-DD] timeline | 進度記錄` entry
6. **回報**：告訴使用者記了什麼

## Entry 格式

每天的 entry 用日期作為 H2 標題，每條進度用 Obsidian Callout 色塊。一天可以有多條。

### Callout 類型對照

| 類型 | Callout | 顏色 |
|------|---------|------|
| 實驗 | `[!example]` | 🟣 紫色 |
| 程式 | `[!info]` | 🔵 藍色 |
| 論文 | `[!abstract]` | 🔷 青色 |
| 基建 | `[!success]` | 🟢 綠色 |
| 決策 | `[!warning]` | 🟠 橘色 |
| 文件 | `[!quote]` | 🩶 灰色 |

### 格式範本

```markdown
## YYYY-MM-DD

> [!example] 一句話標題（動詞開頭）
> **影響**：為什麼重要，1-2 句。有數據就附數據
> **相關**：[[concepts/xxx]]、[[analyses/yyy]]
> **投影片**：`ppt/<名稱>/`（如有對應的投影片）
> **下一步**：接下來要做什麼（可選）
```

### 欄位說明

- **Callout 類型**：根據進度性質選對應的 callout（見上表），Obsidian 會自動著色
- **標題**：動詞開頭，簡潔描述（如「完成 IO Skill Med 實驗」「決定放棄 RAG Debug」）
- **影響**：這條進度對專案的意義
- **相關**：wikilinks 連到相關的 wiki 頁面。如果頁面不存在，仍然寫 wikilink（Obsidian 顯示為灰色節點，之後可補建）
- **下一步**：可選。自然帶出的後續行動

### 合併同日 entry

如果今天已經有 entry（H2 日期相同），在該日期下追加新的 callout，不要重複建 H2。

### 插入位置

新 entry 插在最後一條 `---` 分隔線之後、既有日期 entry 之前（reverse chronological）。

## 里程碑更新

如果今日進度是重要里程碑（完成一個 Phase、重大實驗結果、架構決策），也更新 `## 里程碑總覽` 區段，追加一個 `[!timeline|color]` callout。

里程碑用 **Timeline Callout** 呈現（需要 `timeline-callout.css` snippet，安裝在 wiki 的 `.obsidian/snippets/`）。
CSS 原始檔位於 `/home/chunyen/.claude/skills/llm-wiki/assets/timeline-callout.css`。
不要用 Mermaid——Obsidian 深色主題下渲染很差。

### 里程碑 callout 格式

```markdown
> [!timeline|color] MM-DD
> ## 里程碑標題
> 關鍵成果描述（1-2 句，有數據就附數據）
> - 細節 1
> - 細節 2
> - [[concepts/相關頁面]]
```

### 顏色對照

| 顏色 | 用途 |
|------|------|
| `blue` | 已完成的里程碑 |
| `green` | 進行中 / 當前 Phase |
| `orange` | 截稿日 / 警告 |
| `red` | 逾期 / 緊急 |
| `purple` | 重大決策 |
| `cyan` | 新 Phase 開始 |

新增里程碑時，在 `## 里程碑總覽` 下方、`## Callout 圖例` 上方插入新的 `[!timeline|color]` callout。最新的放最下面（chronological）。

## 範例

使用者說：「今天跑完了 CodeBook Skill 的 pilot 測試，Hard 題 +4pp，比預期好」

追加到 timeline.md：

```markdown
## 2026-04-15

> [!example] 完成 CodeBook Skill Pilot 測試
> **影響**：Hard 題 +4pp（超出預估的 +3~5pp 範圍中段），確認結構化 pattern 注入比 RAG tag hint 更有效
> **相關**：[[concepts/codebook-skill]]、[[analyses/experiment-results]]
> **下一步**：生成完整 90 patterns，跑全 dataset 驗證
```

如果是重要里程碑，也在 `## 里程碑總覽` 追加：

```markdown
> [!timeline|green] 04-15
> ## CodeBook Skill Pilot 測試完成
> Hard 題 +4pp，確認結構化 pattern 注入有效
> - [[concepts/codebook-skill]]
```

## 注意事項

- 不要記瑣碎的事（修了一個 typo、調了一行 config）。timeline 記的是「回頭看會覺得重要」的進度
- 如果一天沒有重大進度，不用強迫記錄
- 保持 entry 精簡，細節放在對應的 wiki 頁面裡，timeline 只放摘要 + wikilink
