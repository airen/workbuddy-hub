# 自媒体创作专家团（Creator Ops Team）

> 一个人格化、跨环节的自媒体内容生产专家团。覆盖选题情报 → 内容生产 → 视频制片 → 多平台发布 → 数据复盘五个环节，把「一句话选题」做成「可直接发布的成品」，每个不可逆节点都要拿到你的明确授权。

## 这是什么

把自媒体创作的 5 大环节打包成 7 个角色：
- **主理人 章有序**（内容总监）：编排与终审
- **闻先机**（选题情报官）：热点、竞品、素材
- **毕成章**（主笔）：文案、策略、平台改写
- **颜可观**（视觉设计师）：配图、封面、信息图
- **陶成帧**（视频制片）：口播剪辑、字幕、切片
- **郑多平**（分发运营）：多平台发布、合规自查
- **查有数**（内容分析师）：数据复盘、迭代建议

## 这个专家团适合谁

- 想把一个账号的内容生产**流程化**，而不是每次从头想
- 同时做公众号 / 小红书 / 抖音 / B站 / X 等多平台，需要**一稿多平台改写**
- 视频素材越来越多，**剪片/出字幕/切片段**成了瓶颈
- 团队里有选题、写作、设计、剪辑、发布、复盘分工，但缺一个**总控**

## 包含什么

- **6 套技能**（详见 `skills/creator-ops/SKILL.md` 的路由表）：
  - 内容生产：10 个 `self-media-*`（选题到复盘全流程）+ 21 个 `baoyu-*`（宝玉的写作/视觉/翻译/信息图/小红书图）+ 12 个 `*-skill`（蒸馏自真实 AI 自媒体大 V 的写作人格）
  - 视频制片：4 个 `auto-editor*`（去静音、转写、效果、导出）
  - 多平台发布：1 个 `self-media-wechat-publisher`、3 个 `baoyu-post-to-*`、4 个 `*-upload`
  - 工具箱：1 个 `creator-toolbox`（9 个外部软件的交接指引）
  - 入口：1 个 `creator-ops`（先判链路再派活）

总计 **53 个技能**。

## 怎么用

1. 装上之后，对主理人（章有序）说一句话选题，他会派活
2. 中途会让你**三次确认**：
   - **方向确认**（环节①结束后）
   - **终稿确认**（环节②/③结束后）
   - **发布授权**（环节④开始前）—— **没明确同意不会推送到任何平台**
3. 用 ImageGen 工具出图，用 `present_files` 收交付物

## ⚠️ 运行前置（先看这段）

本包**不是所有能力都能开箱即用**。以下依赖必须先确认：

| 依赖 | 影响的技能 | 怎么补 |
|---|---|---|
| `baoyu-md` / `baoyu-chrome-cdp` / `baoyu-fetch`（npm） | baoyu 的发布/抓取类技能 | 在技能 `scripts/` 目录里 `bun install` |
| `auto-editor`（Nim CLI） | 4 个 `auto-editor*` 技能 | 见 `creator-toolbox` 第 6 条 |
| `sau`（social-auto-upload CLI） | 4 个 `*-upload` 技能 | 见 `creator-toolbox` 第 4 条 |

**先验证再承诺。** 用户说「帮我发到抖音」时，先跑 `sau --help` 确认能通。跑不了就直说，不要假装完成。

## ⚠️ 与既有 self-media-studio 的关系

本机若同时装了 `self-media-studio`，注意二者有 **10 个同名技能**（都来自 `yanhua1010/self-media-content-workflow`）：
- `self-media-content-workflow` / `-brief` / `-strategy` / `-trend-radar` / `-platform-copywriting` / `-short-video` / `-content-analytics` / `-content-delivery` / `-wechat-publisher` / `-video-publisher`

**建议二选一**，同时装会出现重复技能名。本包额外提供了：
- 21 个 baoyu 写作/视觉/发布技能
- 12 个 AI 自媒体大 V 写作人格
- 4 个 omnipost 视频发布技能
- 4 个 auto-editor 剪辑技能
- 工具箱地图（9 个外部软件交接指引）

## 许可与归属

- 本包新增内容（plugin.json、7 个 agent MD、8 个头像、入口技能、工具箱技能、README）以 **MIT** 发布
- 上游 51 个技能原文保留，按上游许可继承（详见 `LICENSE` 的「归属表」）
- 9 个外部软件**未打包**，仅在 `creator-toolbox` 里给出用途与获取方式

完整许可与归属表见 [`LICENSE`](./LICENSE)。

## 安装

**从 open.workbuddy.cn 上架后**，用户可以在 WorkBuddy AI 的专家市场中找到并安装。

**本地安装**（开发者自用）：
```bash
# 1. 把 creator-ops 目录拷到 my-experts/plugins/
cp -R creator-ops ~/.workbuddy-ai/plugins/marketplaces/my-experts/plugins/

# 2. 注册
python3 /Applications/WorkBuddy\ AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/expert-manager/scripts/register_expert.py \
  ~/.workbuddy-ai/plugins/marketplaces/my-experts/plugins/creator-ops

# 3. 重新打开 WorkBuddy AI，在「专家」里能找到「自媒体创作专家团」
```

## 打包

```bash
# 必须先创 settings.json（应用会删，所以要同一条命令里完成）
printf '{\n  "agent": "creator-ops-team-lead"\n}\n' \
  > ~/.workbuddy-ai/plugins/marketplaces/my-experts/plugins/creator-ops/settings.json
python3 /Applications/WorkBuddy\ AI.app/Contents/Resources/app.asur.unpacked/resources/plugins/workbuddy-builtin/skills/expert-manager/scripts/package_expert.py \
  ~/.workbuddy-ai/plugins/marketplaces/my-experts/plugins/creator-ops \
  /Users/damo/workshop/WorkBuddy/dist/

# 上架前自审（解包后跑）
unzip -q dist/creator-ops.zip -d /tmp/audit
python3 ~/.workbuddy-ai/skills/expert-pack-from-skill-repo/scripts/preflight.py /tmp/audit/creator-ops
```

## 致谢

- 5 个上游开源项目（详见 `LICENSE` 第三、四节）
- 本包由 [大漠](mailto:damo@example.com) 整理与封装
