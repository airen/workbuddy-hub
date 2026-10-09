---
name: to-spec
display_name: "写成规格"
display_name_en: "To Spec"
description: "该技能用于把当前对话的上下文和代码库理解综合成一份规格说明（spec），并发布到项目的 issue 追踪器上；它不做访谈，只综合你已经讨论过的东西。适用于「写成规格」「生成 spec」「把刚才聊的整理成文档」「沉淀成方案」「输出规格说明」「to-spec」这类需求。"
description_zh: "把当前对话综合成一份规格说明，并发布到项目的 issue 追踪器"
description_en: "Synthesize the current conversation into a spec and publish it to the issue tracker."
category: development-tools
version: 1.0.0
author: "大漠"
agent_created: true
---

# 写成规格说明（to-spec）

本技能拿当前对话上下文和代码库理解，产出一份规格说明。**不要**访谈用户；只综合你已经知道的东西。

Issue 追踪器和分诊标签词汇应该已经提供给你了。如果没有，提示用户先运行 `setup-matt-pocock-skills` 技能完成本仓库初始化。

## 流程

1. 探索仓库以理解代码库的当前状态（如果你还没做过）。整份规格说明里都要使用项目领域术语表的词汇，并尊重你正在触碰那块区域里的任何 ADR。

2. 勾勒出你打算在哪些接缝（seam）上测试这个功能。已有的接缝应优先于新接缝。使用尽可能高的接缝。如果需要新接缝，就在你能做到的最高点上提议它们。整个代码库里的接缝越少越好 —— 理想数量是一个。

跟用户确认这些接缝符合他们的预期。

3. 用下面的模板写出规格说明，然后发布到项目的 issue 追踪器。打上 `ready-for-agent` 分诊标签 —— 不需要额外的分诊。

<spec-template>

## Problem Statement

用户正面临的问题，从用户的视角出发。

## Solution

这个问题的解决方案，从用户的视角出发。

## User Stories

一份**长长的**、编号的用户故事清单。每条用户故事都应是这种格式：

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

这份用户故事清单应当极其详尽，覆盖这个功能的方方面面。

## Implementation Decisions

一份已做出的实施决策清单。可以包括：

- 将要构建/修改的模块
- 那些模块中将要修改的接口
- 来自开发者的技术澄清
- 架构决策
- Schema 变更
- API 契约
- 具体的交互

**不要**包含具体的文件路径或代码片段。它们可能很快就会过时。

例外：如果某个原型产出了一段代码片段，它比散文更精确地编码了某个决策（状态机、reducer、schema、类型形状），就把它内联到相关决策里，并简要注明它来自一个原型。裁剪到只剩决策密集的部分，不是一个可运行的 demo，只是重要的那几块。

## Testing Decisions

一份已做出的测试决策清单。包括：

- 描述什么构成一个好测试（只测外部行为，不测实现细节）
- 哪些模块会被测试
- 测试的先例（即代码库中类似类型的测试）

## Out of Scope

描述这份规格说明范围之外的东西。

## Further Notes

关于这个功能的任何进一步备注。

</spec-template>
