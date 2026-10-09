---
name: handoff
display_name: "会话交接"
display_name_en: "Handoff"
description: "该技能用于把当前会话压缩成一份交接（handoff）文档，供另一个 agent 接手继续工作。适用于「交接一下」「写个交接文档」「把这个会话总结给下一个人」「换会话前留个 handoff」这类需求，也适用于上下文快满、需要开新会话前保存进度时。可传入一段说明，描述下一个会话将用来做什么，文档会据此调整重点。"
description_zh: "把当前会话压缩成一份交接文档，供另一个 agent 接着干"
description_en: "Compact the current conversation into a handoff document for another agent."
category: productivity-tools
version: 1.0.0
author: "大漠"
disable-model-invocation: true
agent_created: true
---

# 交接（handoff）

## 输入

- 可选：一段描述，说明下一个会话将用来做什么。用户传入的参数会被当作对下一个会话重点的说明，文档据此裁剪。

写一份交接文档，总结当前会话，让一个全新的 agent 能接着往下做。保存到用户操作系统的临时目录 —— 不要存进当前工作区。

文档里要包含一个「建议加载的技能（suggested skills）」小节，点名下一个 agent 应该调用 Skill 工具加载哪些技能。

不要重复其他产物（specs、plans、ADRs、issues、commits、diffs）里已经记录的内容。改用路径或 URL 引用它们。

抹掉任何敏感信息，例如 API keys、密码，或个人可识别信息（personally identifiable information）。

如果用户传入了参数，把它们当作对下一个会话重点的描述，据此裁剪这份文档。
