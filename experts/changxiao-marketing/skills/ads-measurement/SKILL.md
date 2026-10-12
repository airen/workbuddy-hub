---
name: ads-measurement
display_name: 投放与衡量
display_name_en: Ads & Measurement
description: "Plan, create, and measure paid campaigns — ad creative, analytics, A/B testing, attribution. Diagnose spend efficiency and ship better creative. Inspired by coreyhaines31/marketingskills/ads-measurement."
category: content
version: 1.0.0
author: 大漠
---

# 投放与衡量（广告创意 / 数据 / A-B 测试 / 归因）

对应原库 `ads-measurement` 模块：**把预算花在能回本的地方**。涵盖 ads（投放）、ad-creative（创意）、analytics（分析）、ab-testing（A/B）。交付的是**能上线的创意成稿 + 一套衡量方案**，不是名词解释。

> 前置：`product-marketing` 定下的 ICP 决定"投给谁、在哪投"；`conversion-optimization` 决定"落地页接不接得住"。没定先回去补。

## 适用场景

- "我们的投放 ROI 太低，帮我看看"
- "帮我写几组广告创意"
- "这个落地页要不要做 A/B 测试"
- "怎么衡量这次投放到底赚没赚"

## 输入

- 投放平台（Google / Meta / 小红书 / 抖音等）
- 预算与当前数据（CPC / CTR / CAC / ROAS，没有就说"假设"）
- 目标（拉新 / 转化 / 召回）
- 现有创意 / 落地页

## 执行步骤

### 1. 投放诊断
按"渠道 → 受众 → 创意 → 落地 → 衡量"五段问：
- 投的平台是不是 ICP 常驻的？
- 受众定向是不是太宽 / 太窄？
- 创意 CTR 是不是低于行业（假设基准 1%）？
- 落地页接不接得住（回流 conversion-optimization）？
- 有没有一套能算 ROI 的衡量口径？

### 2. 广告创意
读取 `references/ad-creative-templates.md`，给 3–5 组创意成稿：
- 每组含：**主标题 + 副文案 + 视觉方向 + 目标受众钩子**
- 覆盖不同角度（痛点 / 利益 / 社会证明 / 反直觉）
直接给能贴进后台的文案。

### 3. A/B 测试
读取 `references/ab-test-plan.md`，挑 1 个最值得验的变量（标题？受众？落地页？），给一份测试计划：
- 假设、变量、样本量思路、跑多久、怎么判定胜负。

### 4. 衡量口径
给一套最小指标体系：花了多少（Spend）→ 拿到多少（Imp/Click）→ 转化多少（CVR）→ 赚回多少（ROAS/CAC）。
明确"赚没赚"的判定线（如 ROAS ≥ 3 才扩量）。

## 输出

- 一份**投放诊断**（五段，标掉链子的环节）
- **3–5 组广告创意成稿**（标题/副文案/视觉/钩子）
- 一份 **A/B 测试计划**（假设→变量→判定）
- 一套**衡量口径**（Spend→ROAS 链路 + 扩量线）

## 边界

- 不替用户决定"投多少预算"——给判定线，让用户拍板。
- 实时竞价 / 后台数据我查不了；给模板 + 假设基线，用户用报表回填。
- 归因模型（多触点）是深水区，给基础口径（末次/首触），更深指向 analytics 工具。
