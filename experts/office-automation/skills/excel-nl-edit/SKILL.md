---
name: excel-nl-edit
display_name: 自然语言改 Excel
display_name_en: Edit Excel by Natural Language
description: "Edit Excel spreadsheets by natural-language requests — compute columns, clean data, filter, sort, aggregate — using the platform's sheet tools. Use when the user wants to change cells in a table by describing what they want in plain language. Inspired by menahishayan/MS-Office-AI."
category: content
version: 1.0.0
author: 大漠
---

# 自然语言改 Excel

对应开源项目 **menahishayan/MS-Office-AI** 的核心能力：在 Excel 里接入 Gemini，用自然语言请求更新单元格。这里把它内化成一个**本地可跑**的工作流——用户用大白话提表格需求，「办妥」用 WorkBuddy 的表格处理技能把表真正改好，并说清"这次改了哪些单元格"。

## 适用场景

- "帮我把金额列都四舍五入保留两位小数"
- "加一列总额，等于数量乘单价"
- "找出金额大于 1 万的行，标出来"
- "把状态为空的填成待处理，再按销售额排个序"
- 用户甩来一张表 + 一句"帮我这么这么弄"

## 输入

- 用户的 .xlsx / .csv 文件（或让助手起一张新表）
- 一句或多句自然语言修改意图

## 执行步骤

### 1. 先看清表
读取表头、行数、关键列取值，确认字段与单位（参考 cookbook 的"读与看"）。不确定就问一句，别猜。

### 2. 意图翻译
把用户的自然语言映射到 `references/excel-edit-cookbook.md` 里的意图类别（算与填 / 改与清 / 查与排 / 出与联），逐条列出"要改什么"。

### 3. 先确认后改
把"我会改 X 列 / 删 N 行 / 加 Y 列"说给用户听，再动手。涉及删除、覆盖、改格式尤其要先确认。

### 4. 用表格工具执行
调用表格处理技能完成：插入列、公式/计算、条件格式、筛选排序、去重、拆分、导出 CSV 等。输出**新文件** `xxx-v2.xlsx`，保留原表。

### 5. 交付
- 改好的文件 + 一句话"这次改了哪些地方"（旧→新要点）
- 复杂改动可建议配合 `doc-revise-diff` 的思路做单元格级差异说明

## 毕业到原项目（MS-Office-AI）的提示

MS-Office-AI 是"在 Excel 内接 Gemini、用自然语言更新单元格"的插件形态，前置条件较硬：
- 需配置 **Node.js** 运行环境
- 需**插件侧载（add-in sideload）**到 Excel
- 需配置 **Gemini API Key**
- 数据会发往 Gemini 做理解，涉及**敏感/机密表格要谨慎**，确认合规与数据出境风险
- 「办妥」默认用本地表格工具完成同样的"自然语言改表"，不依赖 Gemini；只有当你已具备上述环境、且接受其数据流向时，才考虑引入 MS-Office-AI。

## 边界

- 不丢原表、不原地覆盖；新文件单独命名。
- 用户没给全数据时，用示例行并标注"示例，请替换"，不把编造数据当真。
- 财务/人事等敏感表，改动点标清楚让用户自己复核，不下"已对账/已合规"结论。
