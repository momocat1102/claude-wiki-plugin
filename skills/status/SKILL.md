---
name: status
description: "研究 Wiki 狀態總覽。觸發詞：wiki status, wiki 狀態。"
---

# Wiki Status

Quick overview of a wiki's current state.

## What to Report

1. **Stats**: Total pages by category (entities, concepts, sources, analyses), total sources ingested
2. **Last activity**: Last 5 entries from `wiki/log.md` (`grep "^## \[" wiki/log.md | tail -5`)
3. **Status breakdown**: Pages by status (stub/draft/solid/comprehensive)
4. **Coverage**: Which topic areas are strong vs thin (based on tag counts and status)
5. **Pending issues**: If a lint was run previously, summarize outstanding issues

## Format

Present as a concise summary with a stats table. Example:

```
Wiki: MACS-Coder Research
Pages: 45 (12 entities, 8 concepts, 20 sources, 5 analyses)
Status: 3 comprehensive, 15 solid, 18 draft, 9 stub
Last ingest: 2026-04-07 — "RPM-MCTS Deep Dive"
Coverage: strong on code-agent, rag | thin on rl, mcts
```
