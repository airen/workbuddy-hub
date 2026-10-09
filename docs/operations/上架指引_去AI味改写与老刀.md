# 上架指引：去AI味改写（技能）+ 老刀（专家）

两个包已按 open.workbuddy.cn 开放平台的接收格式打好，**可直接拖进后台上传**。下面按操作顺序来。

> 2026-09-21 更新：专家包原名 `de-ai-editor` 上传时报「专家名称已被占用」，已改用全局唯一名 **`lao-dao-editor`**（目录名、plugin.json 的 name/plugin/agentName、agent 文件名、头像文件名已全部统一）。技能包名 `de-ai-rewrite` 目前未发现冲突，若上传也报占用，同理换名。

---

## 0. 先准备好账号（只能你本人做）

上架入口：**https://open.workbuddy.cn/** → 立即入驻

个人主体需要四样材料：**中国大陆二代身份证** + 已实名的本人手机号 + 能收验证码的邮箱 + 能做人脸识别的手机。
（港澳台及外籍证件暂不支持；一张身份证全平台只能认证一个个人主体。）

个人主体可发布的：**技能 ✅ 专家 ✅**；Buddy 应用和硬件接入需要企业认证。

---

## 1. 要上传的两个包

| 包 | 路径 | 大小 | 平台上限 |
|---|---|---|---|
| 技能包 | `dist/de-ai-rewrite.zip` | 2.4 KB | 3 MB |
| 专家包 | `dist/lao-dao-editor.zip` | 442 KB | 20 MB |

技能卡头像（上传技能时要单独传一张 512×512 的图）：`dist/去AI味改写_头像.png`

两个包都已核对：解压后第一层就是技能目录 / 专家目录，没有多套一层。

---

## 2. 上架「去AI味改写」技能

后台路径：**发布管理 → 技能 → 右上角「创建」**

1. 把 `de-ai-rewrite.zip` 拖进上传区 → 平台自动解压、识别、生成技能 ID
2. 点「继续」进入确认信息页。有一部分字段是从包里读出来的，页面上改不了；要改就回 SKILL.md 改了重新打包
3. 补齐页面上的三项：
   - **市场展示分类**：建议选「内容创作」（可多选，比如再加「知识与学习」）
   - **服务类目**：至少 1 个、最多 5 个，建议「工具-办公」
   - **头像**：上传 `去AI味改写_头像.png`
4. 核对右侧预览（名称 / 简介 / 头像）→ 继续 → 确认汇总信息 → **提交**

包里已写好的字段（页面会读出来，供核对）：

- name：`de-ai-rewrite`
- display_name：去AI味改写 / display_name_en：De-AI Rewrite
- description：含触发词（去 AI 味 / 去 AI 腔 / 人味改写 / 降 AI 检测率 / 润色得自然一点…）
- version：1.0.0 · author：大漠 · category：`content-creation`
- 正文：10 类 AI 腔删除规则 + 注入真实人声 + 3 遍流程（与本地版本完全一致）

---

## 3. 上架「老刀」专家

后台路径：**发布管理 → 专家 → 「创建」**

1. 把 `lao-dao-editor.zip` 拖进上传区（专家包上限 20 MB，我们只有 442 KB）
2. 补齐市场展示信息（其余字段包里已带）：
   - **市场展示分类**：建议「内容创作」
   - **服务类目**：至少 1 个，建议「工具-办公」
   - **头像**：可沿用包内 `avatars/lao-dao-editor.png`，也可重传
3. 提交审核

包里已写好的字段：

- name / plugin / agentName：全部 `lao-dao-editor`（三处一致，agent 文件名也是 `lao-dao-editor.md`）
- expertType：agent · categoryId：`06-ContentCreative`
- displayName：老刀 · profession：资深编辑 · 去AI味改写
- displayDescription.zh：45 字（平台要求 40–50 字）
- tags 3 个（去AI味改写 / 文案润色 / 人味写作）· quickPrompts 3 个（第一条 = defaultInitPrompt）
- 内置技能：`skills/de-ai-rewrite`（召唤老刀即自带完整方法论，不依赖外部服务）

---

## 4. 审核与发布

- 提交后等审核：官方口径 **7 个工作日**，开发者实测约 **18 小时**
- 结果在开放平台的**通知中心**看；若开放平台和 WorkBuddy 是同一个微信号注册的，WorkBuddy 消息中心也会推
- 通过后状态变成「待发布」，**必须再点一次「发布」**才真正上架
- 发布方式选 **「公开发布」**（全部用户可见、市场可搜可装）；「专用发布」只给账号下的 Buddy 应用用
- 发布后卡片上有「更新版本 / 设置 / 下架」，后续维护都在这

---

## 5. 卡点清单（实测踩过的）

| 报错 | 原因 | 解法 |
|---|---|---|
| 专家/技能名称「已被占用」 | name 是**全平台全局唯一**，不是账号内唯一 | 换一个更具体的前缀名，并把 plugin.json 的 `name` **和** `plugin`（专家还要 `agentName` + agent 文件名 + 目录名）一起改，重新打包 |
| 解析失败：缺少 display_name / description_zh 等 | 本地 frontmatter 字段不全 | 补齐九个字段再打包（已补） |
| YAML 解析报错 | 冒号后没空格、多余引号 | `key: value`，引号尽量不用（已用解析器校验） |
| 多套一层目录 | 打包时把 `skills/` 一起打进去 | 第一层必须是技能/专家目录（已核对） |
| 驳回：所选类目与应用类目不符，至少应包含高度生成或AI创作类目 | 包内 categoryId 用了 `06-ContentCreative`，上传页展示分类也选了「内容创作」，审核认为没落到 AI 类目 | 已改：plugin.json `categoryId` → `04-DataAI`（数据智能/AI 应用），版本升 `1.0.1`，重新打包。重新上传时上传页的**市场展示分类务必勾选含「AI创作」的分类**（可多选，建议 AI创作 + 内容创作） |

若仍解决不了：对照 https://open.workbuddy.cn/docs/skill 与 https://open.workbuddy.cn/docs/expert ，或发邮件 **openworkbuddy@tencent.com**。

---

## 6. 上架版本与本地版本的关系

上架的是副本，**本地不受影响**：

- 技能：`~/.workbuddy/skills/de-ai-rewrite/`
- 专家：`~/.workbuddy/plugins/marketplaces/my-experts/plugins/lao-dao-editor/`（已重新注册，重启 WorkBuddy 后专家中心可见「老刀」）

后续在平台「更新版本」时：改本地文件 → 同步专家包里的 `skills/de-ai-rewrite/SKILL.md` 副本 → 重新打包 → 上传。

---

## 7. v1.0.1 重新提交（2026-10-02）

针对 2026-09-24 驳回意见（所选类目与应用类目不符，至少应包含高度生成或AI创作类目）的修复版本：

- `plugin.json`：`version` 1.0.0 → **1.0.1**；`categoryId` `06-ContentCreative` → **`04-DataAI`**（官方 15 类中最贴近「AI 创作/高度生成」的类目：数据分析、机器学习、AI 应用）
- 已重新校验 + 注册 + 打包：`dist/lao-dao-editor.zip`（441.7 KB，第一层即专家目录）
- 操作：卡片上点**「重新提交」**，上传新 zip；上传页「市场展示分类」勾选含 AI 创作的分类（建议 AI创作 + 内容创作多选），服务类目维持「工具-办公」

> ⚠️ 驳回意见里提到「企业开发者支持发布深度生成或AI创作类目相关的资产，请先进行企业认证」。如果重新提交后仍因同一原因被拒，说明该类目对个人主体不开放——届时二选一：① 走企业认证后再发；② 邮件沟通 openworkbuddy@tencent.com 确认个人主体可用的类目组合。
