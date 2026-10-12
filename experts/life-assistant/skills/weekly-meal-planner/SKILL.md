---
name: weekly-meal-planner
display_name: 一周食谱规划器
display_name_en: Weekly Meal Planner
description: "Generates a downloadable, offline index.html that plans a week of meals by days, people, budget and existing inventory, then aggregates a shopping list. Use when the user wants a weekly menu, asks to plan meals, or mentions budget/inventory-based planning."
category: other
version: 1.0.0
author: 大漠
---

# 一周食谱规划器

对应开源项目 zhangge11/meal-plan-generator 的核心能力：不想每天重新想菜单？按时间、预算和库存排一周食谱，**下载后打开 index.html 就能用**。这里把这份规划器做成一个离线单文件网页，双击即用。

## 输入

- 规划天数（默认 7）
- 用餐人数（默认 1）
- 每日预算（可选）
- 现有库存（逗号分隔的食材，用于"优先消耗 + 自动出采购单"）

## 执行步骤

### 1. 收集参数
用户没给就取默认值，先给默认再让用户改（别为了问而问）。把参数记下来。

### 2. 生成工具
1. 读取 `references/meal-planner.html`（已内置约 40 道家常菜与成本/库存逻辑，纯前端、零依赖）
2. 按用户给的参数，把模板里的默认值替换成用户值（天数/人数/预算/库存直接填进对应 `input` 的 `value` 或 `textarea` 文本），**让用户打开即看到自己的参数**
3. 将文件写入用户工作区，命名为语义化名字，如 `周食谱.html`
4. `present_files` 交付，并说明双击打开即可、数据存本地

> 若用户只想"先给我看个样例"：可直接在对话里说"已生成，双击打开填一下就有"，不必强行替他决定菜单。

### 3. 收尾提示
- 数据全在浏览器 `localStorage`，换设备/清缓存前点"导出计划"存一份 `.txt`
- 菜谱池是内置的常见家常菜；想加菜改 `POOL` 数组即可（照结构加 `{n,c,i,m}`）
- 成本为粗略估算，仅用于"别超预算"的排序，非真实物价

## 内容边界

- 不声称营养配比/热量，除非用户明确要且标注"估算"
- 不做饮食诊断（过敏/病史请遵医嘱），但可尊重用户给的忌口做过滤
- 离线网页不联网、不收集数据、不要 API key
