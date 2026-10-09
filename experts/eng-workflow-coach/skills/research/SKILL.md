---
name: research
display_name: "一手资料调研"
display_name_en: "Research"
description: "该技能针对高可信度的一手资料（primary sources）调研一个具体问题，并把结论写成仓库里的一份 Markdown 文件，每条论断都标注来源。适用于「研究一下这个」「帮我查官方文档」「把 API 事实查清楚」「把这个主题研究明白」「查一下第一方资料」这类需求，也适用于要把读资料的体力活交给后台子代理去跑、好让自己继续干活时。"
description_zh: "对着高可信一手资料调研一个问题，把结论写成带引用的 Markdown"
description_en: "Investigate a question against high-trust primary sources; capture findings as a cited Markdown file."
category: knowledge-learning
version: 1.0.0
author: "大漠"
agent_created: true
---

# 调研（research）

起一个**后台子代理**去做调研，这样它读资料的时候你能继续干活。

它的任务：

1. 针对**一手资料（primary sources）**（官方文档、源代码、规格说明、第一方 API）调研这个问题，而不是针对别人对它们的二手转述。每一条论断都要回溯到拥有它的那个源头。
2. 把结论写成一份 Markdown 文件，每一条论断都标注来源。
3. 存到仓库平时放这类笔记的地方；沿用既有约定，如果没有约定，就放在一个合理的位置，并说明放在了哪里。
