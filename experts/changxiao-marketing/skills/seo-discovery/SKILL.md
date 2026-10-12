---
name: seo-discovery
display_name: SEO 与搜索发现
display_name_en: SEO & Discovery
description: "Audit and improve search visibility — technical SEO, keyword research, AI SEO, programmatic SEO, schema markup. Deliver a prioritized SEO audit, not a theory lecture. Inspired by coreyhaines31/marketingskills/seo-discovery."
category: content
version: 1.0.0
author: 大漠
---

# SEO 与搜索发现（审计 / 关键词 / AI SEO / 程序化 SEO / schema）

对应原库 `seo-discovery` 模块：**让目标用户用搜索找到你**。涵盖 seo-audit（审计）、ai-seo（AI 搜索优化）、programmatic-seo（程序化）、schema（结构化数据）。交付一份**带优先级的 SEO 体检清单**。

> 前置：`product-marketing` 定下的 ICP，决定"用户会搜什么词"。没定就先回去补——选错关键词白做。

## 适用场景

- "给我的网站做个 SEO 审计"
- "我们的关键词该怎么选"
- "怎么让 AI 搜索（ChatGPT/Perplexity）也能提到我们"
- "我们有一堆相似页面，能不能程序化做 SEO"
- "要不要加 schema 结构化数据"

## 输入

- 网站地址 / 主要页面
- 业务与 ICP（来自 product-marketing，或让用户补）
- 现有流量数据（GA / Search Console，没有就说"假设"）
- 主要竞品

## 执行步骤

### 1. 技术审计
读取 `references/seo-audit-checklist.md`，按"技术 / 内容 / 外链 / AI SEO"四块逐条过：
- **技术**：能不能被收录（robots / sitemap / 加载速度 / 移动端 / HTTPS / 重复内容）
- **内容**：标题 / 描述 / H1 / 关键词覆盖 / 内容深度
- **外链**：有没有被权威站引用（没有就列获取方向）
- **AI SEO**：内容有没有被 AI 摘要抓取的潜力（结构清晰、有问答、有数据）

### 2. 关键词映射
按 ICP 的检索意图，给每个核心页面配 1 个主词 + 2–3 个长尾词，列出"搜索意图 → 该写什么内容"。

### 3. AI SEO 建议
- 把核心问题写成"问答块"（FAQ 风格），方便 AI 摘要引用。
- 关键事实配数据 / 来源，提升被引用概率。
- 用 schema 标记组织信息（见下）。

### 4. Schema 与程序化（按需）
- **Schema**：给关键页面加哪种结构化数据（Org / Article / FAQ / Product），给代码片段模板。
- **Programmatic SEO**：如果用户有大量相似页面（城市 / 品类 / 模板），给"模板 + 数据源"的玩法，不替用户生成海量内容。

### 5. 优先级清单
按"影响 × 难度"排：Critical（不改就搜不到）/ Recommended / Nice-to-have。

## 输出

- 一份**SEO 审计清单**（四块，带优先级）
- 一份**关键词映射**（页面 → 主词 + 长尾）
- **AI SEO** 改造建议（问答块 / 数据化）
- **Schema** 代码片段（按需）
- **程序化 SEO** 玩法（按需）

## 边界

- 不黑帽（关键词堆砌、隐形文字、买垃圾外链）——违反平台合规且会被惩罚。
- 实际抓取 / 排名数据我没法实时查；给检查清单 + 假设基线，让用户用工具回填。
- 海量程序化内容生成靠用户的内容管线，本技能给"怎么设计"不替你量产。
