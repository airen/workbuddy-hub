---
name: conversion-optimization
display_name: 转化优化
display_name_en: Conversion Optimization
description: "Diagnose and improve conversion across the funnel — homepage CRO, signup, onboarding, popups, paywalls — using a measurable CRO playbook. Use when conversion rates are low or a page/flow needs lifting. Inspired by coreyhaines31/marketingskills/conversion-optimization."
category: content
version: 1.0.0
author: 大漠
---

# 转化优化（首页 / 注册 / 激活 / 付费墙）

对应原库 `conversion-optimization` 模块：**把访客一步步变成注册用户、付费用户**。涵盖 CRO 审计、signup 流程、onboarding 激活、popups 弹窗、paywalls 付费墙。核心原则——**每条改动都能被衡量**，不靠拍脑袋。

> 前置：`product-marketing` 的"受众 + 价值主张"没定，先回去补。转化漏斗的设计依赖 ICP 的决策链路，基础没定会白做。

## 适用场景

- "首页转化太低，帮我看看怎么优化"
- "注册流程流失严重"
- "新用户注册完就走了，激活率很低"
- "要不要加个弹窗 / 付费墙？怎么设计不惹人烦"

## 输入

- 当前转化链路（落地页 / 首页、注册步骤、激活步骤、付费步骤）
- 现有数据（访问量、注册率、激活率、付费率；没有就说"假设"）
- 你想优化的重点环节（哪一步掉得最狠）

## 执行步骤

### 1. 漏斗体检
读取 `references/cro-playbook.md` 的"漏斗诊断表"，按 5 段（访客→注册→激活→付费墙→续费）逐段问：
- 这一步的转化率大概多少？
- 用户在这一步卡在哪（看不懂、不信任、没动力、步骤太多）？
标出**掉得最狠、且最容易改**的 1–2 段作为主攻点。

### 2. 主页 / 落地页 CRO
按 playbook 的"首页 12 问"过一遍，重点看：
- **价值主张**一眼能懂吗？（对 ICP 说话，不是对同行）
- **主 CTA** 是否单一、是否"下一步动作"清晰？
- **信任证据**（案例、数据、logo、评价）够不够？
- **首屏**是否 5 秒内讲清"这是什么、对我有什么用"？
给出 3–5 条带优先级的修改建议（Critical / Recommended / Nice-to-have）。

### 3. 注册 / 激活
- **注册**：字段能不能砍到最少？能不能社交登录 / 邮箱一步？错误提示是否友好？
- **激活**：新用户第一步该做什么能"啊哈"？有没有空状态引导、示例数据、进度条？
给一份"激活路径"清单（从注册到第一次价值实现的每一步）。

### 4. 弹窗 / 付费墙
- **弹窗**：时机（滚动 50%？退出意图？）、文案、关闭是否容易；明确"不惹人烦"的红线。
- **付费墙**：免费能给多少、付费解锁什么、价格锚点怎么摆；给出 A/B 的两种摆法。
直接给**文案成稿**（弹窗标题 + 按钮、付费墙说明）。

### 5. 衡量方案
每条建议配一个指标 + 当前基线 + 改完预期：
> 例：首页主 CTA 从"免费试用"改成"看 2 分钟 demo" → 注册率预期 +15%（基线假设 3%）

## 输出

- 一份**漏斗诊断**（哪段掉得最狠、为什么）
- 一份带优先级的**CRO 修改清单**（首页 + 注册 + 激活）
- 弹窗 / 付费墙的**成稿文案**
- 一份**衡量方案**（指标 + 基线 + 预期）

## 边界

- 不替用户决定"要不要做付费墙"这种商业模式选择——给方案 + 风险，让用户拍板。
- 数据我没法替你测；给出的基线标"假设"，上线后用分析报告回填。
- A/B 测试设计归本技能；实际跑实验 / 埋点接入靠 analytics 工具或 `ads-measurement`。
