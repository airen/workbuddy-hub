# 自媒体内容工作室（Self Media Studio）

把一个母题从「一句话选题」走到「已发布并复盘」的自媒体内容生产闭环。工具无关、证据优先、人工在环——方向、平台、标题、终稿、发布五道确认，一道都不跳。

## 类型

Agent 型（单个 AI 专家）· 行业分类：内容创作（`06-ContentCreative`）

## 功能

主理人「柳成文」负责请求路由、状态管理和确认点，把 10 个预加载技能串成一条可续跑的链路：

| 技能 | 职责 |
|------|------|
| `self-media-content-workflow` | 总控：请求路由、状态管理、确认点和端到端编排 |
| `self-media-content-brief` | 创作简报：澄清目标、受众、证据、角度和约束 |
| `self-media-content-strategy` | 内容策略：账号定位、内容配比、栏目、选题池和内容日历 |
| `self-media-trend-radar` | 热点与竞品：热点追踪、关键词研究、竞品拆解和原创选题 |
| `self-media-platform-copywriting` | 平台文案：X、小红书、公众号、短视频平台和 YouTube 原生文案，含 8 套配图风格预设 |
| `self-media-short-video` | 短视频：钩子、口播、分镜、字幕、拍摄方案，可选数字人制片与动画解说制片，横竖屏多平台版本 |
| `self-media-content-analytics` | 数据复盘：数据质量、基线比较、归因、决策和实验 |
| `self-media-content-delivery` | 交付归档：里程碑保存、版本、路径核验和完整发布包 |
| `self-media-wechat-publisher` | 公众号发布：排版、图片上传、草稿箱写入和小绿书图片消息 |
| `self-media-video-publisher` | 视频发布：逐平台发布包，逐平台授权后上传为私密、草稿或定时 |

**四条设计原则**：工具无关（不绑定特定模型、浏览器、图片、视频、发布或数据服务，运行时自动发现可用能力）；平台原生（同一母题共享事实与证据，为每个平台分别设计标题、开头、结构和行动）；人工在环（五道强制确认，默认只产出草稿或发布包，从不自动群发）；证据优先（关键数字必须有来源，区分事实、判断、推断与建议）。

## 使用示例

- 我只有一个选题，帮我从创作简报一路做到多平台发布
- 帮我给这个账号理一份内容策略：定位、栏目和选题池
- 视频成片已确认，帮我出抖音、视频号和小红书的发布包
- 找一下这周这个话题的热点窗口，拆三个同类爆款的结构，给我几个能做的原创角度
- 上周公众号和小红书的数据我发你了，帮我做个周复盘，看下该加码还是改包装

## 头像

头像位于 `avatars/self-media-studio.jpg`。如需替换：JPG 或 PNG，512×512 px，单张不超过 500KB。

## 安装

将专家包目录放到专家目录下：

```
$WORKBUDDY_CONFIG_DIR/plugins/marketplaces/my-experts/plugins/self-media-studio/
```

然后运行注册命令使其可见：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
python3 scripts/package_expert.py <expert-dir> <output-dir>
```

## 来源与许可

本专家包是对开源项目 [yanhua1010/self-media-content-workflow](https://github.com/yanhua1010/self-media-content-workflow)（MIT License, Copyright (c) 2026 Yanhua）的封装转化。

- `skills/**` 下的全部 10 个技能**逐字保留**上游内容，未翻译、未简化、未改写。
- 本包新增的只有编排层：主理人 persona、`plugin.json` 元数据、README、LICENSE、头像。
- 完整归属说明见 `LICENSE`。

上游仓库的 `scripts/validate.py`、`.github/workflows/`、`.claude-plugin/` 等属于上游自身的工程设施，与技能内容无关，未纳入本包。

## 免责声明

平台规则以官方为准；账号操作风险自担；凭据由用户自己保管；内容合规由发布者负责；不保证效果。
