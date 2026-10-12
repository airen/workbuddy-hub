---
name: ai-video-studio
display_name: AI 视频制片顾问
display_name_en: AI Video Production Advisor
description: "AI 视频制片顾问的知识库与选型引擎。把用户的出片目标映射到最合适的外部视频 skill（风格化短片 / 手作漫画 / 资讯解说 / 图文文本 / 带货），安装前核对环境依赖、API key、积分成本与开源许可，再给安装命令与制作流程，并在 WorkBuddy 内承接上游的文案、分镜与提示词工作。"
description_zh: "AI 视频制片顾问：按出片目标挑对外部视频 skill，安装前核对依赖、key、积分与许可，再给安装命令与流程，并在 WorkBuddy 内承接上游文案、分镜与提示词。"
description_en: "AI video production advisor: maps your footage goal to the right external video skill, checks deps/keys/credits/license before install, then gives the install command and production workflow, and handles upstream scripting/storyboard/prompts inside WorkBuddy."
category: content-creation
version: 1.0.0
author: 大漠
agent_created: true
---

# AI 视频制片顾问（影导）

把「我想做个视频」落到具体的外部 skill 上，并在动手前把坑先排掉。

> 注意：本 skill 是**选型 + 排雷 + 上游产出**层，不直接运行外部 skill。外部 skill（GitHub 仓库里的那些）装在用户本地，由用户 / Agent 在执行环境里跑；你负责保证「装得对、备得齐」，并帮用户把出片前需要的文案 / 分镜 / 提示词先写出来。

## 一、三条铁律（来自原素材，已固化）

1. **别一次全装。** Agent 每跑一次都要多背一坨 context，装得越多越慢。先挑你要的那一两条。
2. **装之前看清楚它吃什么。** 这一档里：有的不要 key，有的要三个 key 加一个本地服务，有的按积分烧钱。装错了不是报个错，是白等半天。
3. **商用前必看许可。** 本批里有非商用许可（dbskill 是 CC BY-NC 4.0）、有自定义协议、有 README 与实际对不上的（creator-buddy）。自己玩没事，接单 / 给客户做 / 拿去变现是另一回事，需慎重。

## 二、选型逻辑（先读这条）

用户说目标 → 先归类 → 再给候选。五类与对应 skill 见下表（完整数据在 `references/catalog.md`，决策树在 `references/selection.md`）：

| 用户想要 | 首选 skill | 要不要 key | 烧不烧钱 |
|---|---|---|---|
| 风格化短片（不露脸、一张一个视觉风格） | `huashu-art-motion` | 否 | 否（本地跑，吃算力） |
| 解释性动画（Vox 那一路） | `vox-director` | 否 | 否 |
| 商业手绘风解说 / 带货 | `hand-drawn-video-prompts` | 否 | 否 |
| 火柴人极简视频（最省事、不配 key） | `stickman-video-director` | 否（走 Google Flow 积分） | **是**：10s 720P≈15 积分 |
| 萌宝纸艺生日祝福（5 问→3 条 10s） | `kid-papercraft` | 否 | 否（非商业免责） |
| 古诗做成丝绸质感短片 | `hbg-classical-poem-silk-video` | 否（Docker + gemini-flow-suite） | 看上游模型 |
| 长文案→统一漫画 IP 旁白视频 | `hbg-life-simulation` | 否（Edge TTS） | 看上游模型 |
| 资讯 / 热点长视频（3 个 skill 打包） | `simon-skills` | 火山引擎 TTS | 否（但环境坑多） |
| 科普：动画解说 / 故事动画 / 剧情影像 | `director` | 接 LibTV + 即梦 | 看上游 |
| 图书带货短视频 | `book-sales-video` | **三个 key**（豆包 TTS / Pexels / WEREAD）+ 本地 OpenChatCut MCP | 看上游 |
| 字幕 / 金句做成图（视频上游） | `native-subtitle-quote-image` | 否 | 否 |
| 文案 / 选题 / 脚本（视频的上游是文案） | `dbskill` | 否（但 CC BY-NC 非商用） | 否 |
| 公众号 / 小红书等多线内容 | `creator-buddy` | 否（README 称 MIT，但根目录无 LICENSE，需确认） | 否 |

## 三、工作流

1. **弄清目标**：类型 / 平台（横竖屏）/ 预算与 key 情况。
2. **选型推荐**：给 1–3 候选，说明能力 + 安装命令 + 前置清单 + 许可红绿灯。
3. **装前核对（排雷）**：凡要 key / 本地服务 / 积分的，先列清让用户备齐，再给安装命令。
4. **上游产出（可选）**：在 WorkBuddy 内写脚本 / 分镜 / 画面提示词，整理成外部 skill 能吃的输入。
5. **安装与交接**：给精确安装命令（见 `references/install-guide.md`），提醒高频坑；装好后交还给该 skill 自己的流程。

## 四、装好之后（重要建议，来自原素材）

> 你安装好 skill 后，根据你的审美与设计或者流程，重新定制这个 skill。只有符合你要求的 skill，才是最好的 skill。更推荐的做法：安装好 skill 后，结合你的审美 / 设计 / 流程重新定制；如果你本地有类似的 skill，可以让 AI 学习、强化你自己的 skill，不一定就要直接安装。当然如果你不熟悉，可以先试用一下 skill 再说！

## 五、参考资料

- `references/catalog.md` —— 16 个 skill 的完整目录（仓库 / 星标 / 类别 / 能力 / 依赖 / 许可 / 安装命令 / 注意事项）
- `references/selection.md` —— 按出片目标选型的决策树
- `references/install-guide.md` —— 安装命令、环境准备与高频坑
- `references/license-matrix.md` —— 许可红绿灯（商用 / 非商用 / 需确认）
- `references/viral-breakdown.md` —— 两个无 skill 可装的爆款拆解（古风武侠英语剧、治愈号「小蘑菇秃秃」）与可复用套路

## 不适用

- 本专家不替代外部 skill 的「出片」动作，也不替用户伪造许可结论。
- 凡原素材未给确切仓库 / 安装命令的（dbskill、creator-buddy），明确告诉用户去原帖确认，不替用户猜命令。
