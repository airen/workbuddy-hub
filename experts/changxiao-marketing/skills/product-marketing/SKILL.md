---
name: product-marketing
display_name: 产品营销基础
display_name_en: Product Marketing Foundation
description: "Establish the marketing foundation — product, audience, positioning, value proposition, ICP — so all downstream marketing (copy, SEO, ads, growth) is built on a clear 'who/what/why'. Use before any specialized marketing task. Inspired by coreyhaines31/marketingskills/product-marketing."
category: content
version: 1.0.0
author: 大漠
---

# 产品营销基础（所有营销技能的共同基础）

对应原库 `product-marketing` 模块：**所有营销技能的共同基础**。在做任何专项（文案/SEO/转化/投放）之前，先把"产品卖给谁、解决什么问题、与别人有何不同"摸清——基础没定，文案、关键词、转化漏斗都会偏。

## 适用场景

- "我刚做出来一个产品，不知道卖给谁"
- "我们的定位好像有问题，新用户听完介绍还是不清楚"
- "文案一直在改但效果不好，怀疑是定位问题"
- 在做转化优化/SEO/投放前，先回到这一步把基础打牢

## 输入

- 你的产品/服务（是什么、做什么、有什么特性）
- 现有的目标用户描述（哪怕是模糊的）
- 竞品是谁（用户说得出名字的，或者你推断的）
- 你目前用的定位话术（如果有）

## 执行步骤

### 1. 定位画布
读取 `references/positioning-canvas.md`，用 6 个字段把定位写清楚：
- **目标受众**（for）
- **问题/需求**（who）
- **品类**（is a）
- **核心利益**（that）
- **差异化**（unlike）
- **证据/理由**（because）

### 2. ICP 画像
读取 `references/icp-template.md`，填一份理想客户画像：
- 基本信息（行业、规模、角色）
- 痛点与触发事件
- 决策链路与评估标准
- 信息获取渠道

### 3. 价值主张（一句话）
基于定位画布，提炼一句 15–25 字的**价值主张**（不是产品描述）。格式参考：
> 帮 [谁]，在 [场景]，解决 [问题]，得到 [收益]，不像 [替代方案]。

### 4. 对齐检查
自检三个一致：
- 受众画像 ↔ 价值主张：画像里写的人，会被这句话打动吗？
- 价值主张 ↔ 实际功能：产品的核心功能真的能交付这个承诺吗？
- 受众画像 ↔ 信息渠道：你的 ICP 在哪些渠道能听到你？

## 输出

- 一份填好的**定位画布**
- 一份**ICP 画像**（1–2 份主 ICP 即可）
- 一句话**价值主张** + 3 个变体（A/B 测试用）
- **对齐检查**结论：哪条不一致、要补什么信息

## 与下游技能的衔接

定位画布 + ICP 画像定下后，可作为以下技能的基础输入：
- `copywriting-content`：用 ICP 的语言写文案
- `seo-discovery`：用 ICP 的检索意图选关键词
- `conversion-optimization`：用 ICP 的决策链路设计漏斗
- `ads-measurement`：用 ICP 的渠道选投放平台
- `growth-retention`：用 ICP 的痛点设计留存循环
- `monetization-sales`：用 ICP 的付费意愿定价

## 边界

- 不替用户做战略决策（定位、定受众、定价）——给方案 + 理由 + 风险，让用户拍板。
- 用户没说"先做这个"，但任务明显依赖定位（如"帮我写首页文案"），先花 2–3 轮问清基础，再做专项。
- 数据/市场调研超出本技能范围；让用户去做一手调研或接 RAG/搜索技能。
