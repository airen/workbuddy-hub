---
name: copywriting-content
display_name: 文案与内容
display_name_en: Copywriting & Content
description: "Write and edit marketing copy — homepage copy, emails, cold emails, social posts — using proven frameworks (AIDA/PAS/BAB). Deliver ready-to-use drafts, not theory. Inspired by coreyhaines31/marketingskills/copywriting-content."
category: content
version: 1.0.0
author: 大漠
---

# 文案与内容（首页文案 / 邮件 / 冷邮件 / 社媒）

对应原库 `copywriting-content` 模块：**把 ICP 的语言写成能转化的文案**。涵盖 copywriting（写）、copy-editing（改）、emails（邮件）、social（社媒）、cold-email（冷邮件）。交付的是**成稿**，不是框架讲解。

> 前置：`product-marketing` 定下的 ICP + 价值主张，是文案的"用词字典"。没定就先回去补——否则写出来的文案是对空说话。

## 适用场景

- "帮我写首页文案 / landing page 文案"
- "帮我写 5 封欢迎邮件"
- "帮我写一封冷邮件去拉客户"
- "这篇稿子帮我改得更有说服力"
- "帮我写几条社媒发文的钩子"

## 输入

- 要写的物料类型（首页 / 邮件 / 冷邮件 / 社媒）
- ICP 与价值主张（来自 product-marketing，或让用户补）
- 调性要求（专业 / 活泼 / 极简）、字数限制
- 已有草稿（要改的话）

## 执行步骤

### 1. 选框架
读取 `references/copy-frameworks.md`，按物料选框架：
- 首页 / landing → **AIDA**（抓注意→兴趣→欲望→行动）
- 痛点强 → **PAS**（问题→放大→解决）
- 前后对比 → **BAB**（前→后→桥）
- 邮件主题行 → **4U**（有用/紧急/独特/超具体）

### 2. 写首页 / landing 文案
按 AIDA 给结构稿：
- **首屏标题**：一句话价值主张（对 ICP 说话）
- **副标题**：展开那句话，加信任锚
- **主 CTA**：单一动作
- **下方区块**：利益点 ×3（用 ICP 的语言）、社会证明、FAQ
直接给成稿，标注哪句为什么这么写。

### 3. 写邮件
- **欢迎邮件序列**：读取需求，给 N 封序列，每封含主题行 + 正文 + 目的（见 `references/cold-email-template.md` 的序列模板）。
- **冷邮件**：读 `references/cold-email-template.md`，给"破冰→价值→低门槛 CTA"的成稿（≤150 字）。

### 4. 改稿（copy-editing）
逐句过：砍废话、换抽象词为具体词、补证据、调节奏。给"改前/改后"对照 + 为什么改。

### 5. 社媒钩子
给 3–5 条开头钩子（提问式 / 反直觉 / 故事式），每条配一句正文方向。

## 输出

- 一份**成稿**（首页文案 / 邮件正文 / 冷邮件 / 社媒钩子）
- 框架标注：为什么这么写（哪句对应 AIDA 哪一步）
- 改稿类：改前 / 改后对照

## 边界

- 不写违反平台合规的话术（垃圾邮件诱导、虚假承诺、违规社媒）。
- 数据 / 案例我没法替你编——要用就标"假设，待你替换真实数字"。
- 长文 / 白皮书等深度内容归 content 策略，本技能给单篇成稿与改稿。
