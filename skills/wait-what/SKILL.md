---
name: wait-what
display_name: "换个说法重讲"
display_name_en: "Wait What"
description: "该技能用于在用户没看懂上一条消息时，让 agent 停下来，用 ASD-STE100 简化技术英语（Simplified Technical English）把那段话重讲一遍：补一点上下文，并使用 `GLOSSARY.md` 里的通用语言。适用于「我懵了」「等一下，你在说什么」「没听懂」「换个说法重讲」「wait what」这类需求。"
description_zh: "没听懂时，用简化技术英语补上上下文重讲一遍"
description_en: "Re-pitch the last message in plain English with the context the user is missing."
category: productivity-tools
version: 1.0.0
author: "大漠"
disable-model-invocation: true
agent_created: true
---

# 等等，什么？（wait-what）

等一下，我看不懂你这里讲到哪了。把那段重讲一遍：给我一点上下文，用 ASD-STE100 简化技术英语（Simplified Technical English）来说，并使用 `GLOSSARY.md` 里的通用语言（ubiquitous language）（如果仓库里有不止一个术语表，就顺着 `GLOSSARY-MAP.md` 找到对的那个）。
