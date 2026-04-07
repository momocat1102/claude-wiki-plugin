# Wiki Plugin for Claude Code

研究 Wiki 管理工具——9 個子指令管理 Obsidian vault 知識庫。

## 安裝

```bash
# 1. 加入 marketplace
claude plugin marketplace add https://github.com/momocat1102/claude-wiki-plugin

# 2. 安裝 plugin
claude plugin install wiki

# 3. 重新載入
# 在 Claude Code 裡執行 /reload-plugins
```

## 解除安裝

```bash
claude plugin uninstall wiki
claude plugin marketplace remove wiki
```

## 可用指令

| 指令 | 說明 |
|------|------|
| `/wiki:init` | 初始化新的 Wiki（Obsidian vault） |
| `/wiki:ingest` | 將文件加入 Wiki |
| `/wiki:timeline` | 記錄今日進度到里程碑 |
| `/wiki:search` | 搜尋 Wiki |
| `/wiki:query` | 跨頁面合成答案 |
| `/wiki:status` | Wiki 狀態總覽 |
| `/wiki:lint` | Wiki 健康檢查 |
| `/wiki:viz` | 生成視覺化圖表 |
| `/wiki:ppt` | 從 Wiki 生成投影片 |

## 共用設定

所有子指令共用的設定（Language、frontmatter、log.md 慣例）在 `references/shared-config.md`。

## 授權

MIT
