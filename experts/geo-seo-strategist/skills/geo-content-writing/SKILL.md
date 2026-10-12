---
name: geo-content-writing
display_name: GEO 式写作
display_name_en: GEO-Style Content Writing
description: "Turns a validated GEO topic into an article that both ranks on Google and gets cited by AI search. Covers expanding a keyword into real queries (with follow-ups), writing clear entities, building scenario-based comparisons backed by verifiable evidence, and organizing the answer-first structure (TL;DR → Comparison → Review → Use Cases → FAQ). Use after geo-topic-research has confirmed a topic is worth writing."
category: content
version: 1.0.0
author: 大漠
---

# GEO 式写作

确定主题后，把"关键词覆盖"升级为"决策信息完善 + 答案结构优化"。GEO 写作不是重写一篇文章，而是补齐三种能力。

> 先讲清边界：**加 FAQ、Schema 或 TL;DR 不保证 AI 一定引用你。** GEO 目前没有稳定排名公式。这些是好实践，不是"保证被推荐"的捷径。

## 适用场景

- 已经有 `geo-topic-research` 确认过的主题，要落成文章
- 给一篇已有 SEO 基础的博客做 GEO 优化（不推倒重写，只调三处）

## 输入

- 已确认的 GEO Topic + 核心 Keyword
- 产品 / 竞品信息（功能、价格、限制）
- 能核实的资料：官方文档、价格页、真实截图或测试结果

## 执行步骤

### 步骤 1 — 从 Keyword 扩展到用户真实 Query（含追问）

以核心 Keyword 为起点，扩展用户实际会问的问题，按决策链路分类：

- **产品认知**：这是什么、安不安全（`Is X safe to use?`）
- **功能**：支持什么、怎么用
- **价格**：免费吗、多少钱（`Is there a free alternative to X?`）
- **替代方案 / 对比**：和谁比、谁更好（`X vs Y: which is better?`）
- **场景追问（Follow-up）**：哪些支持自托管？哪些适合三人小团队？哪些能嵌入现有 SaaS？

这些追问会影响最终推荐，也提示一篇文章除了主问题，还要覆盖用户接下来会关心什么。

### 步骤 2 — 写清 Entity，准确描述"谁、有什么能力、和别人差在哪"

Entity 不是机械重复品牌名，而是让读者（和人）明确知道：你在介绍谁、它有什么能力、和其他工具有什么区别。常见 Entity：

- 产品实体（RecentFollow、EasyComment）
- 产品类别（Instagram 关注者查询工具）
- 功能 / 属性（截图反馈、AI 对话、自托管）

### 步骤 3 — 把 Comparison 和 Evidence 放在一起，按场景解释差异

只列功能差异不足以帮用户选型。用户真正想知道的是"我只需要免费查询该选哪个""我要更细的分析该选哪个"。做法：

- 先**核实**产品功能、价格、限制（官方资料 / 真实截图 / 实测）
- 再围绕**真实使用场景**比较，关键判断尽量用可验证证据支撑
- 避免缺乏依据的"Best Tool"式推荐

### 步骤 4 — 组织成"答案优先"的文章结构

把传统 Review 顺序（介绍→功能→教程→人群→安全→价格→替代→对比→结论）改成答案优先：

1. **TL;DR / Quick Verdict**：开头直接回答适合谁、主要优势、限制
2. **Core Features & Pricing**：核心功能与价格
3. **Comparison（如 X vs Y）**：提前展示对比
4. **Detailed Review & Evidence**：用真实资料解释关键判断
5. **Best For & Use Cases**：针对不同场景给选择建议
6. **FAQ**：补充常见问题

让读者更快找到答案，也让不同问题对应的信息更清晰、独立、易提取——这既利于人读，也利于 AI 抽取去回答具体问题。

## 输出：三处优化对照（用于优化既有文章）

| 优化维度 | 原有 SEO 文章 | GEO 优化方向 |
|---|---|---|
| 内容覆盖 | 围绕核心关键词介绍产品 | 围绕用户真实问题组织内容 |
| 产品信息 | 介绍功能、价格、优势 | 核实实体信息，明确能力与限制 |
| 竞品比较 | 罗列功能差异 | 结合使用场景解释推荐依据 |
| 可信度 | 产品描述与配图 | 官方来源、真实测试、可验证证据 |
| 文章结构 | 按产品介绍顺序展开 | 先给答案，再比较和解释依据 |

一句话：**关键词覆盖 → 决策信息完善 → 答案结构优化。**

## 反模式

- **堆 FAQ / Schema 当捷径**：写了 ≠ AI 会引用；没有稳定公式。
- **只覆盖关键词不覆盖问题**：AI 场景下用户问的是具体问题。
- **"Best Tool"式空推荐**：没有场景、没有证据。
- **重要结论埋在文末**：用户和 AI 都难快速取到答案。
- **不加来源就下判断**：证据必须可核实（官方 / 截图 / 实测）。

## 参考

- 真实案例拆解思路（RecentFollow Review：5.44 万曝光 / 841 点击的 SEO 博客如何做 GEO 优化）来自社区实践，具体调整效果仍需发布后持续跟踪，见 `references/sources.md`。
