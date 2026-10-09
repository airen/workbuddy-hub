---
name: creator-toolbox
description: 自媒体外部工具箱地图。收录 9 个不能打包进专家包的创作者工具（热榜聚合、竞品监控、多平台发布、口播剪辑、无损剪切、代码生成视频），说明各自解决什么问题、什么时候该把活交接出去、以及从哪里获取。当用户提到 TrendRadar、beacon 烽火台、RSSHub、AutoX、ScriptCut、auto-editor、Remotion、LosslessCut，或问「有没有工具能做 X」时加载本技能。
---

# 自媒体外部工具箱地图

## §0 为什么单独有这个技能

自媒体创作里有一半的活**不是「写」出来的，是「跑」出来的**：抓热榜、盯竞品、批量发平台、剪口播。

这些东西是**独立软件**，不是提示词能替代的能力。它们没法打包进专家包（体积、许可、运行环境都不允许），但用户又确实需要知道**什么时候该用哪个**。

本技能就是那份「交接说明书」：**专家团负责判断和产出，外部工具负责执行重活**。

## §1 工具箱总表

| # | 工具 | 解决什么 | 形态 | 许可 | 获取 |
|---|---|---|---|---|---|
| 1 | **TrendRadar** | 多平台热榜聚合 + RSS + 关键词筛选 + AI 简报 | 自部署服务 | GPL-3.0 | [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) |
| 2 | **beacon 烽火台** | 热榜 + 竞对监控 + AI 选题 + 一稿多平台改写 + 敏感词合规 | SaaS / 自部署 | AGPL-3.0 + 商业授权 | [AiyaFun/beacon](https://github.com/AiyaFun/beacon) |
| 3 | **RSSHub** | 把 5000+ 站点转成 RSS，用来盯竞品和资讯 | 自部署 / 公开实例 | AGPL-3.0 | [DIYgod/RSSHub](https://github.com/DIYgod/RSSHub) |
| 4 | **AutoX** | 多平台一键发布、视频搬家、YouTube/抖音监控、自动翻译 | 桌面应用 | ⚠️ 未声明许可 | [spider-ios/autox-release](https://github.com/spider-ios/autox-release) |
| 5 | **ScriptCut** | 按文稿剪口播，导出社媒切片 | 桌面应用 | AGPL-3.0 | [FernandoAbishai/ScriptCut](https://github.com/FernandoAbishai/ScriptCut) |
| 6 | **auto-editor** | 自动去静音/去静止，命令行改节奏 | CLI | Unlicense（公有领域） | [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) |
| 7 | **Remotion** | 用 React 代码批量生成视频 | 开发框架 | ⚠️ 非开源（商用需授权） | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) |
| 8 | **LosslessCut** | 无损粗剪（不重编码，秒级完成） | 桌面应用 | GPL-2.0 | [mifi/lossless-cut](https://github.com/mifi/lossless-cut) |
| 9 | **Awesome 清单 ×2** | 创作者工具 / AI 视频工具索引 | 文档 | CC0-1.0 | [lucky-verma](https://github.com/lucky-verma/awesome-creator-tools) · [JuneYaooo](https://github.com/JuneYaooo/awesome-ai-media) |

## §2 逐个说明与交接时机

### 1. TrendRadar —— 热榜情报底座

**是什么**：聚合多平台热点 + RSS 订阅，支持关键词精准筛选、AI 智能筛选/翻译/简报，可接入 MCP 架构让 AI 直接对话分析。推送渠道覆盖企业微信/飞书/钉钉/Telegram/邮件/ntfy/bark/Slack。

**什么时候交接**：用户说「帮我盯热点」「每天早上给我一份热点简报」「最近什么话题在涨」——**这是 TrendRadar 的活，不是让模型凭空编热榜**。

**怎么拿**：仓库提供 Docker 部署、本地部署（Python）、GitHub Actions 定时跑三种路径，另有在线演示站。部署方式见仓库 README 的「快速开始 / Docker 部署 / 本地部署」章节。

**许可**：GPL-3.0。**仅作为外部服务使用**，不要把它当库链接进商业产品。

### 2. beacon 烽火台 —— 选题作战室

**是什么**：面向创作者和内容团队的多平台选题 SaaS。七源热榜聚合、竞对监控、AI 选题智囊团（带六维评分与推荐理由）、一稿多平台改写、敏感词合规检测、数据看板。支持 Docker Compose 自部署，也提供在线体验。

**什么时候交接**：用户要的是「**每天早上一份带理由的选题推荐**」，而不只是热榜列表；或者要「一稿多平台改写 + 敏感词检测」这种组合能力。

**怎么拿**：官方在线体验站可直接试用；自部署走仓库的 Docker Compose 路径。Node.js 20+。

**许可**：AGPL-3.0 + 单独的商业授权文件。**商用需另谈授权**，别默认能白用。

### 3. RSSHub —— 竞品监控管道

**是什么**：把几乎所有站点转成 RSS。5000+ 全球实例。

**什么时候交接**：用户说「我想盯着某个账号/某个站点的更新」。RSSHub 负责把内容变成订阅流，之后可以接到任意 RSS 阅读器。

**怎么拿**：Docker 镜像 `diygod/rsshub`；npm 包 `rsshub`；也可用公开实例 `rsshub.app`。部署细节见官方文档 <https://docs.rsshub.app/deploy/>。搭配 [Folo](https://folo.is/)（开源 AI RSS 阅读器）体验更好。

**许可**：AGPL-3.0。

### 4. AutoX（autox-release）—— 多平台发布与搬家

**是什么**：桌面端自媒体运营工具。一键发布视频到快手/YouTube/小红书/美拍/B站等，另含视频搬家、YouTube 监控、抖音监控、自动翻译。

**什么时候交接**：用户要「一条视频同时发到 6 个平台」或「把某平台的历史视频搬到另一个平台」。

**怎么拿**：从仓库 Releases 下载（当前 v2.0.0）。需要邮箱注册登录，**部分功能需要向作者申请授权**。

⚠️ **macOS 首次打开要执行**（官方 README 明确给出）：
```bash
sudo xattr -r -d com.apple.quarantine /Applications/AutoX.app
```

⚠️ **许可风险**：该仓库**未声明任何开源许可**，默认「保留所有权利」。仅作个人工具使用，**不要打包、不要二次分发、不要商用**。

### 5. ScriptCut —— 按文稿剪口播

**是什么**：开源、本地优先的桌面视频生产工具。核心玩法是「像编辑文档一样编辑口播视频」——改文稿就等于改视频，然后导出成片和社媒切片。

**什么时候交接**：用户有**长口播/播客/访谈**要精剪，且需要**按文字删改**（而不是按时间轴拖）。

**怎么拿**：GitHub Releases 下载 DMG（当前 v0.1.0-alpha.6）。⚠️ **仅支持 macOS Apple Silicon（arm64）**，且**未做 Apple 公证**。首次启动若被拦，走「系统设置 → 隐私与安全性 → 仍要打开」。**不要关闭 Gatekeeper，也不要跑终端隔离命令。**

**许可**：AGPL-3.0。

### 6. auto-editor —— 命令行去静音

**是什么**：命令行视频/音频自动剪辑。核心是分析音频响度（或画面运动）判断「活跃/静默」，默认把静默段剪掉。这是剪口播的**第一道工序**。

**注意**：本专家包**已经内置了 4 个 auto-editor 技能**（`auto-editor` / `auto-editor-transcribe` / `auto-editor-effects` / `auto-editor-export`），它们负责「怎么用」。但**工具本体要用户自己装**。

**怎么拿**：安装说明见 <https://auto-editor.com/installing>。也可以跑 `npx skills add WyattBlue/auto-editor` 装上游技能（本包已含，通常不需要）。

**典型用法**：
```bash
auto-editor path/to/your/video.mp4                  # 去静默
auto-editor example.mp4 --margin 0.2sec             # 留点呼吸感
auto-editor example.mp4 --export premiere           # 导出到 Premiere
```

**许可**：Unlicense（公有领域）。⚠️ 但注意 README 说明：**Releases 里的二进制产物可能适用不同的开源许可**。

### 7. Remotion —— 用代码批量生成视频

**是什么**：用 React 写视频。适合「数据驱动 + 批量渲染」场景——同一套模板喂不同数据，生成成百上千条视频。

**什么时候交接**：用户要「用代码生成视频」「批量出片」「做数据可视化动画」。**不适合**做单条口播剪辑。

**怎么拿**：
```bash
npx create-video@latest
```
官方还提供 Agent Skills 文档：<https://www.remotion.dev/docs/ai/skills>

⚠️ **许可**：Remotion 采用**自有许可（非开源）**，公司规模达到门槛后**商用需付费授权**。个人/小团队免费，商用前务必确认。

### 8. LosslessCut —— 秒级无损粗剪

**是什么**：FFmpeg 的图形界面封装。核心能力是**无损裁剪**——直接复制数据，不重新编码，所以极快且不掉画质。适合从大段素材里粗切出可用片段。

**什么时候交接**：用户要「快速切出这段」「去掉片头片尾」「从 2 小时素材里挑 10 分钟」，且**不需要精细转场**。

**怎么拿**：<https://losslesscut.app/> 下载对应平台版本。

**许可**：GPL-2.0。

### 9. Awesome 清单 —— 继续找工具

- **awesome-creator-tools**（CC0-1.0）：视频创作剪辑、缩略图、音频播客、直播、社媒管理、分析、变现、Newsletter、AI 内容工具等分类索引。
- **awesome-ai-media**（README 标注 CC0-1.0，但仓库内**无 LICENSE 文件**）：150+ AI 视频生成、社媒自动化工具，带对比表。

**用法**：用户问「有没有能 XX 的工具」时，从这两份清单里找，而不是凭记忆编工具名。

## §3 运行前置：包内技能也有 CLI 依赖

⚠️ **这一节最容易被忽略，但直接决定技能能不能跑**。

本专家包里有几组技能**依赖外部命令行工具**。用户没装，技能就跑不动：

| 依赖 | 影响的技能 | 怎么补 |
|---|---|---|
| **`baoyu-md`**（npm） | `baoyu-post-to-wechat`、`baoyu-post-to-weibo` | 在技能的 `scripts/` 目录里 `bun install` 或 `npm install` |
| **`baoyu-chrome-cdp`**（npm） | 同上 + `baoyu-post-to-x` | 同上 |
| **`baoyu-fetch`**（npm） | `baoyu-url-to-markdown` | 同上 |
| **`auto-editor`**（Nim CLI） | 4 个 `auto-editor*` 技能 | 见上文第 6 条 |
| **`sau`**（social-auto-upload CLI） | `bilibili-upload`、`douyin-upload`、`kuaishou-upload`、`xiaohongshu-upload` | 来自 [social-auto-upload](https://github.com/dreammis/social-auto-upload) |

**规矩：先验证，再承诺。**
用户说「帮我发到抖音」时，先跑一句 `sau --help` 确认能通。跑不了就**直说**，并给替代方案（手动导出发布包让用户自己发）。**不要假装完成了。**

## §4 交接决策树

```
用户要盯热点 / 竞品？
├─ 只要热榜列表 ────────────────→ TrendRadar
├─ 要「带理由的选题推荐」+ 合规检查 → beacon
└─ 要盯某个具体账号/站点的更新 ──→ RSSHub

用户要处理视频？
├─ 口播去静音、改节奏 ──────────→ auto-editor（包内技能 + 外部 CLI）
├─ 长口播要按文稿精剪 ──────────→ ScriptCut（仅 macOS arm64）
├─ 从大素材里快速粗切 ──────────→ LosslessCut
└─ 用代码/数据批量生成 ─────────→ Remotion

用户要发多平台？
├─ 包内技能能覆盖的平台 ────────→ 用 baoyu-post-to-* / *-upload（需 CLI）
└─ 需要图形界面一键全平台 + 搬家 ─→ AutoX

用户问「有没有工具能 XX」─────→ 查 awesome 清单两份
```

## §5 三条纪律

1. **不要编造热榜数据**。需要热点就用 TrendRadar / beacon / RSSHub，模型自己「回忆」的热点大概率是错的。
2. **不要替用户承诺发布**。发布类工具的账号授权、平台风控都不可控，先说清前置条件。
3. **注意许可差异**。AutoX 无许可、Remotion 商用收费、beacon 是 AGPL + 商业双授权——**商用前必须确认**，别默认开源就能白用。
