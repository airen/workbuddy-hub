---
name: grill-with-docs
display_name: "拷问并留档"
display_name_en: "Grill With Docs"
description: "该技能用于就用户的计划、决策或想法做不留情面的深度访谈，并在访谈过程中顺手产出文档 —— 架构决策记录（ADR）和术语表（glossary）。适用于「拷问我并顺便把文档写了」「边聊边补 ADR 和术语表」「磨方案同时沉淀文档」「grill with docs」这类需求，适合既想磨清设计、又想留下决策记录的场合。"
description_zh: "拷问式访谈，同时在过程中产出 ADR 与术语表"
description_en: "A relentless interview that also produces ADRs and a glossary as it goes."
category: development-tools
version: 1.0.0
author: "大漠"
agent_created: true
---

# 拷问并留下文档（grill-with-docs）

依次调用 Skill 工具加载 `grilling` 和 `domain-modeling` 两个技能。
