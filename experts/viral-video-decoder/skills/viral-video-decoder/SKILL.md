---
name: viral-video-decoder
display_name: 视频爆款拆解师
display_name_en: Viral Video Decoder
description: "结合 Hypit 与 WorkBuddy 拆解视频爆款的方法论与框架：Hypit 负责把视频还原成 SVML 脚本图（结构层），WorkBuddy 负责用证据框架与套路框架提炼可复用创作模板（分析层）。"
description_zh: "结合 Hypit 与 WorkBuddy 拆解视频爆款：结构层用 Hypit 出 SVML 脚本图，分析层用证据+套路框架提炼可复用模板。"
description_en: "Dissect viral videos by combining Hypit (structural SVML breakdown) with WorkBuddy (evidence + pattern analysis into a reusable template)."
category: content-creation
version: 1.0.0
author: 大漠
agent_created: true
---

# 视频爆款拆解师（爆析）

把「这条视频为什么火」从一句感觉，变成一张可照着做的模板。

> 核心心法：**结构层交给 Hypit，分析层交给 WorkBuddy。** Hypit 把视频拆成「解剖图」（SVML 脚本图），WorkBuddy 把解剖图翻译成「施工图」（可复用套路）。两层都做，才算拆透。

## 一、为什么是 Hypit + WorkBuddy

- **Hypit**（https://github.com/hypit-ai/hypit，开源免费）是给 AI Coding Agent（Claude Code / Codex 等）用的视频创作系统。对拆解者来说它的价值在于：你丢一条视频进去，它会理解原片**为什么有效**——图形、字幕如何落在具体词语上、画面如何随说话内容变化——并把它还原成一张可编辑的 SVML「视频脚本图」。这正好就是我们要的「结构层」。
- **WorkBuddy（本平台）**擅长的是：把结构化素材做深度分析、跨样本归纳、证据分级、产出可复用文档与模板，并能调用写作 / 检索 / 绘图能力补全佐证。

两者互补：Hypit 出「anatomy（解剖）」，WorkBuddy 出「why + how to replicate（原理 + 复刻方法）」。

## 二、两个外部方法论来源（MIT，仅作框架参考）
- **pinker12/viral-video-analyze** —— 证据分级法 `observed / metric / inferred / unknown`，三档分析（lite/standard/deep）。本专家的「证据框架」即源于此。
- **KINNONG/viral-video-breakdown** —— 创作者研究包结构：`source.mp4` + `keyframes/` + `speaker_transcript.md` + `story_analysis.md`。本专家的「研究包」概念源于此。
> 两者都要求：只分析你有权分析的内容，遵守平台条款与法律。结论以当前视频的实际产物为准，不为外部项目背书。

## 三、标准工作流（详见 agent 文件）
0. 定目标 → 1. Hypit 出 SVML 解剖图 → 2. 带回产物 → 3. WorkBuddy 八维分析 → 4. 产出爆款套路模板 → 5. 做变体/回流 Hypit。

## 四、参考资料
- `references/hypit-guide.md` —— Hypit 安装、喂视频、读 SVML 产物的完整命令与解读。
- `references/evidence-framework.md` —— observed/metric/inferred/unknown 证据分级 + 研究包结构 + 三档分析。
- `references/viral-pattern-framework.md` —— 八维爆款拆解框架（钩子/结构/情绪/视觉/声音/字幕/平台/变现）。
- `references/templates.md` —— 爆款拆解报告模板、可复用套路模板、SVML→模板映射示例。

## 不适用
- 本专家不替代 Hypit 的「出片」动作，也不在 WorkBuddy 内直接跑 ffmpeg/whisper（那是 Hypit 或本地脚本的活）。
- 不鼓励照搬他人内容；目标是可迁移结构。
