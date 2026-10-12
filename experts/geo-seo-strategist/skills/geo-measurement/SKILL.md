---
name: geo-measurement
display_name: GEO 效果度量
display_name_en: GEO Effectiveness Measurement
description: "Defines how to tell whether GEO and SEO work actually move the needle, split into three layers: SEO baseline (Google Search Console impressions/clicks/queries), AI search visibility (testing fixed questions on ChatGPT/Perplexity/Bing/Doubao and recording citations), and real business value (signups or key actions). Emphasizes honest attribution — AI mentions, site visits, and conversions must be observed separately. Use after content is published or assets are deployed."
category: business
version: 1.0.0
author: 大漠
---

# GEO 效果度量

文章写完、资产部署完之后，怎么判断 GEO 到底有没有效果？把验证分成三个层次，**而且要把两层概念先分清楚**：AI 有没有提到我 ≠ 网站有没有访问 ≠ 业务有没有转化。

## 适用场景

- 内容发布后想看"被 AI 提到没、带来用户没"
- 给老板 / 团队汇报 GEO 投入的回报
- 决定下一步该优化选题、写作还是资产

## 输入

- GSC 访问权限（看 SEO 基础）
- 一组已整理的核心问题（来自选题与写作阶段）
- 业务后台（看注册 / 关键行为）

## 执行步骤

### 第一层 — SEO 基础表现

通过 GSC 观察：

- 页面的**曝光、点击、平均排名**
- **实际获得曝光的 Query**（不只看品牌词）
- 是否从 `RecentFollow` 这类品牌词，扩展到 `Review` / `Pricing` / `Alternative` 类查询

这能判断内容是否覆盖了更广泛的相关搜索需求。但**必须提醒**：排名和点击变化也受竞争、算法、搜索需求变化影响，不能简单归因于一次内容修改。

### 第二层 — AI 搜索可见性

选取前面整理的核心问题（如 `Is X safe?` / `X vs Y?` / `What is the best free alternative to X?`），在不同 AI 搜索产品里**定期测试**：

- ChatGPT（含 Search）、Perplexity、Bing AI / Copilot、豆包（ByteDance / Bytespider）
- 记录：品牌是否被提及、文章是否被引用、引用了哪些来源、回答里有没有明显的产品信息错误

**关键方法**：固定问题、固定平台、固定记录方式，长期跟踪；**不要只挑一次出现品牌的结果截图**就当结论。

### 第三层 — 真实业务价值

对增长来说最终看文章有没有带来有价值的用户：

- 用户有没有从文章点击进入产品 / 竞品
- 有没有进一步注册或产生其他关键行为
- 如果 AI 平台带来引荐访问，单独分析这批访问的质量

**AI 引用、网站访问、业务转化要分别观察**——并非所有 AI 品牌曝光都会转化为可追踪的点击。

## 输出：三层度量看板（给用户）

| 层 | 看什么 | 指标 | 归因注意 |
|---|---|---|---|
| SEO 基础 | GSC | 曝光 / 点击 / 平均排名 / 实际 Query | 受算法、竞争、需求波动影响 |
| AI 可见性 | 固定问题跨平台测试 | 品牌提及 / 文章引用 / 错误信息 | 固定问题平台方式，长期跟踪 |
| 业务价值 | 业务后台 | 注册 / 关键行为 / 引荐质量 | 引用、访问、转化分开看 |

## 反模式

- 只截图一次"AI 提到了我"就下结论（要长期、固定方式）。
- 把排名变化全算到内容修改头上（忽略算法 / 竞争）。
- 不分三层，把"AI 提及"直接等同"业务增长"。
- 不记录错误信息（AI 答错比不提更伤信任）。

## 参考

- 三层验证框架与"GEO 最终价值不只是 AI 有没有提到我"的观点来自社区 GEO 实践，见 `references/sources.md`。
- 不同 AI 平台的收录 / 引用机制差异较大，做第二层前建议联网确认当前各平台的最新行为。
