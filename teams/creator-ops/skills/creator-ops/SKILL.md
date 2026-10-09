---
name: creator-ops
description: 自媒体内容生产总入口。当用户要做一个账号的内容、写一篇稿、配一组图、剪一条视频、发到多个平台、或复盘数据时，先用本技能判定「该走哪条链路、该由谁接、出口是什么」，再按需加载具体能力。覆盖选题情报、内容生产、视觉配图、视频制片、多平台发布、数据复盘五大环节。上游技能库没有总入口，本技能补的就是这一层。
---

# 自媒体内容生产总入口

## 这个技能解决什么

上游能力库是一堆**平级的技能**：能写小红书图、能剪口播、能发抖音——但没人回答「我现在该用哪个」。

本技能就是那一层：**先判链路，再派活**。判定完再按路由表加载具体技能，不要一上来就把所有技能塞进上下文。

## §0 先判断：值不值得做

在动手前先问三件事，任何一个答不上来就回去问用户，别硬做：

| 问题 | 答不上来的后果 |
|---|---|
| **给谁看？**（平台 + 账号定位） | 文案语气、图尺寸、标题风格全错 |
| **要什么？**（涨粉 / 转化 / 建立专业度） | 会写成「什么都说了等于什么都没说」 |
| **能提供什么证据？**（数据、案例、一手体验） | 会退化成正确的废话，这是自媒体最致命的问题 |

**证据优先原则**：没有一手材料的稿子，先派 `creator-ops-topic-scout` 去补研究，不要直接让主笔开写。宁可少发一篇，不要发一篇空话。

## §1 五环节总览

| 环节 | 干什么 | 谁负责 | 产出 |
|---|---|---|---|
| **① 选题情报** | 热点、竞品、素材采集 | `creator-ops-topic-scout` | 选题清单 + 证据包 |
| **② 内容生产** | 文案 + 视觉 | `creator-ops-copywriter` / `creator-ops-visual` | 平台原生文案 + 配图组 |
| **③ 视频制片** | 口播剪辑、切片、字幕 | `creator-ops-video` | 成片 + 封面 |
| **④ 多平台发布** | 分发到各平台 | `creator-ops-publisher` | 发布包 / 已发布 |
| **⑤ 数据复盘** | 数据回看、下一轮迭代 | `creator-ops-analyst` | 复盘报告 + 下一轮选题 |

**环节②的文案与视觉可以并行**（同一份大纲，一个写一个画），其余环节串行。

## §2 环节①：选题情报

**触发**：用户说「不知道写什么」「最近有什么热点」「帮我盯一下竞品」「把这篇文章存下来」。

**做什么**：
1. 先明确**平台与账号定位**——同一个热点在公众号和小红书是完全两种写法
2. 采集证据：用 `baoyu-url-to-markdown` / `baoyu-youtube-transcript` / `baoyu-danger-x-to-markdown` 把外部内容转成可引用的文本
3. 需要多平台热榜时，**不要硬编造热榜数据**——热榜聚合是外部服务，见 `creator-toolbox`
4. 输出**选题清单**：每条给「标题角度 + 支撑证据 + 适配平台 + 差异化理由」

**反模式**：列 20 条泛泛的选题（「AI 的十个趋势」）。宁可 3 条有证据的。

## §3 环节②：内容生产

### 文案分支 → `creator-ops-copywriter`

**先定人格再动笔**。这是本包最容易被浪费的一块能力——12 个蒸馏自真实自媒体的人格技能（`baoyu-skill`、`liangziwei-skill`、`jiqizhixin-skill` 等）不是让你模仿口癖，而是给你**不同的切入视角**：

| 想要的效果 | 参考人格 |
|---|---|
| 工程师视角 + 提示词方法论 | `baoyu-skill` |
| 行业快讯、数据驱动、密集更新 | `liangziwei-skill` |
| 论文级深度、学术中立 | `jiqizhixin-skill` |
| Why 追问、创业者伙伴视角 | `jikegongyuan-skill` |
| 硅谷一线、中美双线叙事 | `guixingren-skill` |
| 概念拆解、思维方式输出 | `lijigang-skill` |

**流程**：`self-media-content-brief`（澄清）→ `self-media-content-strategy`（定位）→ 选人格 → `self-media-platform-copywriting`（平台改写）。

**一稿多平台**不是把同一篇复制五遍。小红书要钩子前置 + 短段 + 话题标签；公众号要标题层级 + 逻辑递进；X 要单点锐利。

### 视觉分支 → `creator-ops-visual`

| 要什么 | 用哪个 |
|---|---|
| 文章配图（多张、风格统一） | `baoyu-article-illustrator` |
| 封面图 | `baoyu-cover-image` |
| 小红书图文卡片（带排版） | `baoyu-xhs-images` |
| 信息图 / 数据可视化长图 | `baoyu-infographic` |
| 单张 AI 生成图 | `baoyu-image-gen` |
| 结构图 / 流程图 | `baoyu-diagram` |
| 漫画 / 分镜 | `baoyu-comic` |
| 演示幻灯片 | `baoyu-slide-deck` |
| 发布前压图 | `baoyu-compress-image` |

**WorkBuddy 环境要点**：
- 生成图片用 **ImageGen 工具**，不要试图调用外部图片 API
- 落盘的图用 `present_files` 交付；要在对话里直接展示的简单示意图走 `show_widget`，注意其 `viewBox` 必须以 `0 0 680 ` 开头
- **中文字体是硬约束**：图片/信息图里的中文必须指定含 CJK 的字体栈（如 `Noto Sans CJK SC`），否则会渲染成方框或糊字

## §4 环节③：视频制片 → `creator-ops-video`

**触发**：用户给了口播视频/录音，要「去掉废话」「剪成切片」「加字幕」。

**流程**：
1. `auto-editor` — 去静音、去静止、定节奏（最常用，先跑这个）
2. `auto-editor-transcribe` — 转写字幕，之后可以**按文字剪**而不是按时间轴剪
3. `auto-editor-effects` — 变速、缩放、Ken Burns、画中画
4. `auto-editor-export` — 导出到剪辑软件 / 分片 / 时间轴文件
5. 短视频脚本与分镜用 `self-media-short-video`

**关键提醒**：`auto-editor` 是**外部 CLI**，不是随包附带的。用户没装就先去 `creator-toolbox` 看安装方式，别假装能剪。

**何时交接给外部软件**（见 `creator-toolbox`）：需要按文稿精细剪口播 → ScriptCut；需要 GUI 无损粗剪 → LosslessCut；需要用代码批量生成视频 → Remotion。

## §5 环节④：多平台发布 → `creator-ops-publisher`

**这是全流程唯一有不可逆后果的环节**。

### 铁律：发布前必须拿到用户的明确授权

不允许「我觉得可以发了」就发。必须做到：
1. 把**最终文案全文 + 图片/视频清单 + 目标平台列表**摆给用户
2. 明确问：「确认发布到这些平台吗？」
3. 拿到明确肯定答复才执行

**禁止**：替用户决定发布时间、替用户勾选平台、在用户没看到终稿的情况下发布。

### 技能分工

| 平台 | 技能 |
|---|---|
| 公众号 | `baoyu-post-to-wechat`（排版+发布）/ `self-media-wechat-publisher` |
| 微博 | `baoyu-post-to-weibo` |
| X | `baoyu-post-to-x` |
| B 站 / 抖音 / 快手 / 小红书（视频） | `bilibili-upload` / `douyin-upload` / `kuaishou-upload` / `xiaohongshu-upload` |
| 多平台视频发布编排 | `self-media-video-publisher` |

⚠️ 四个 `*-upload` 技能依赖外部 `sau` CLI（来自 social-auto-upload）。**先确认环境里能跑 `sau --help`**，跑不了就先别承诺发布。

### 合规自查（发布前必做）
- **敏感词**：平台限流词、医疗/金融/绝对化用语
- **版权**：配图、BGM、引用段落是否可用
- **平台规则**：导流外链、二维码、诱导关注——各平台尺度不同
- 更完整的热榜/竞品/敏感词能力需要外部服务，见 `creator-toolbox`

## §6 环节⑤：数据复盘 → `creator-ops-analyst`

**触发**：「这周数据怎么样」「为什么这条爆了那条没爆」。

**流程**：`self-media-content-analytics` → 出复盘 → `self-media-content-delivery` 归档 → 下一轮选题回填给 `creator-ops-topic-scout`。

**核心判据**：复盘要回答**下一轮改什么**，不是罗列数字。没有行动项的复盘报告是废纸。

## §7 全技能路由表

调度时按下表加载，**不要一次性全加载**。

### 选题情报（7）
| 技能 | 何时加载 |
|---|---|
| `self-media-trend-radar` | 需要热点/竞品扫描框架时 |
| `baoyu-youtube-transcript` | 要把 YouTube 视频转成文字素材 |
| `baoyu-url-to-markdown` | 要把任意网页存成干净 markdown |
| `baoyu-danger-x-to-markdown` | 要抓 X/Twitter 帖子内容 |
| `baoyu-wechat-summary` | 要提炼公众号文章 |
| `baoyu-translate` | 外文素材需要翻译 |
| `baoyu-danger-gemini-web` | 需要用 Gemini 网页版做辅助 |

### 文案与人格（17）
| 技能 | 何时加载 |
|---|---|
| `self-media-content-brief` | 需求模糊，先澄清目标/受众/角度 |
| `self-media-content-strategy` | 要给账号定定位、栏目、选题池 |
| `self-media-platform-copywriting` | 一稿改写为多平台原生文案 |
| `baoyu-format-markdown` | 要规范 markdown 结构 |
| `baoyu-markdown-to-html` | 要转成带样式的 HTML |
| `baoyu-skill` | 想用「工程师思维 + 提示词方法论」视角 |
| `guixingren-skill` | 想用「硅谷一线 + 中美双线」视角 |
| `jikegongyuan-skill` | 想用「Why 追问 + 创业者伙伴」视角 |
| `jiqizhixin-skill` | 想用「论文级深度 + 量化驱动」视角 |
| `liangziwei-skill` | 想用「数据驱动 + 速报深析」视角 |
| `lijigang-skill` | 想用「概念拆解 + 思维方式」视角 |
| `qiuzhi2046-skill` | 想用「求智2046」视角 |
| `saibochanshin-skill` | 想用「赛博禅心」视角 |
| `saiwenqiaoyi-skill` | 想用「赛文乔伊」视角 |
| `shuzishengmingkazike-skill` | 想用「数字生命卡兹克」视角 |
| `tegongyuzhou-skill` | 想用「特工宇宙」视角 |
| `xinzhiyuan-skill` | 想用「新智元」视角 |

### 视觉（9）
| 技能 | 何时加载 |
|---|---|
| `baoyu-article-illustrator` | 文章需要成套配图 |
| `baoyu-cover-image` | 需要封面图 |
| `baoyu-xhs-images` | 需要小红书图文卡片 |
| `baoyu-infographic` | 需要信息图 / 数据长图 |
| `baoyu-image-gen` | 需要单张 AI 生成图 |
| `baoyu-diagram` | 需要结构图 / 流程图 |
| `baoyu-comic` | 需要漫画 / 分镜 |
| `baoyu-slide-deck` | 需要演示文稿 |
| `baoyu-compress-image` | 发布前压图 |

### 视频（5）
| 技能 | 何时加载 |
|---|---|
| `self-media-short-video` | 要写短视频脚本 / 分镜 |
| `auto-editor` | 去静音、去静止、定节奏 |
| `auto-editor-transcribe` | 转写字幕、按文字剪 |
| `auto-editor-effects` | 变速、缩放、画中画等效果 |
| `auto-editor-export` | 导出到剪辑软件 / 分片 / 时间轴 |

### 发布（9）
| 技能 | 何时加载 |
|---|---|
| `self-media-wechat-publisher` | 公众号发布编排 |
| `self-media-video-publisher` | 多平台视频发布编排 |
| `baoyu-post-to-wechat` | 公众号排版并发布 |
| `baoyu-post-to-weibo` | 微博发布 |
| `baoyu-post-to-x` | X 发布 |
| `bilibili-upload` | B 站上传 |
| `douyin-upload` | 抖音上传 |
| `kuaishou-upload` | 快手上传 |
| `xiaohongshu-upload` | 小红书上传 |

### 复盘与归档（3）
| 技能 | 何时加载 |
|---|---|
| `self-media-content-analytics` | 数据复盘、指标口径 |
| `self-media-content-delivery` | 交付归档、内容登记 |
| `self-media-content-workflow` | 需要完整闭环编排框架时 |

### 工具（1）
| 技能 | 何时加载 |
|---|---|
| `baoyu-electron-extract` | 从 Electron 应用里提取源码（开发用途，非创作必需） |

### 外部工具（不随包附带，见 `creator-toolbox`）
`creator-toolbox` —— 8 个外部软件的用途、获取方式、什么时候该交接出去。

## §8 运行前置（别跳过这段）

本包**不是所有能力都能开箱即用**。三类依赖必须提前确认：

| 依赖 | 影响的技能 | 怎么补 |
|---|---|---|
| `baoyu-md` / `baoyu-chrome-cdp` / `baoyu-fetch`（npm 包） | `baoyu-post-to-wechat`、`baoyu-post-to-weibo`、`baoyu-post-to-x`、`baoyu-url-to-markdown` | 在各技能的 `scripts/` 目录里 `bun install` 或 `npm install` |
| `auto-editor`（Nim CLI） | 4 个 `auto-editor*` 技能 | 见 `creator-toolbox` |
| `sau`（social-auto-upload CLI） | 4 个 `*-upload` 技能 | 见 `creator-toolbox` |

**先验证再承诺**。用户说「帮我发到抖音」时，先确认 `sau` 能不能跑；跑不了就直说，并给替代方案（手动导出发布包），不要假装完成了。

## §9 人工确认闸门

三个不可逆节点，每个都必须停下等用户：

1. **方向确认** — 选题与切入角度定了才开写
2. **终稿确认** — 文案/成片定稿才做发布物料
3. **发布授权** — 用户明确同意才推送到平台

除此之外（查资料、写草稿、配图、剪片）都可以自主推进，不用反复问。

## §10 输出规范

- **交付物落盘**：文案 `.md`、发布包按平台分目录，图片/视频与文案放一起
- **用 `present_files` 交付**，让用户能直接打开看
- **平台版本分开命名**：`标题_小红书.md` / `标题_公众号.md`，不要混在一个文件里
- **语言跟随用户**：用户用中文就用中文，不要输出英文报告
- **数据与结论要能追溯**：引用的数据标明来源与时间，不要给无出处的数字

## 与既有专家的关系

如果本机同时装了 `self-media-studio`，注意二者有 10 个同名技能（都来自 `yanhua1010/self-media-content-workflow`）。**建议二选一**，同时装会出现重复技能名。
