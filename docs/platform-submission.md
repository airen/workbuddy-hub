# 上架与本地安装（通用流程）

本文提炼所有 WorkBuddy 资产上架的通用流程与卡点，不针对单个资产。
各资产专属的上架记录见其自身目录或 `CHANGELOG.md`。

## 1. 前提

- 入口：**https://open.workbuddy.cn/** → 立即入驻
- 个人主体需要：中国大陆二代身份证 + 已实名手机号 + 能收验证码的邮箱 + 能做人脸识别的手机
- 个人主体可发布：**技能 ✅ 专家 ✅**；Buddy 应用和硬件接入需要企业认证

## 2. 打包

用 hub 自带打包工具（自动注入缺失头像、清理构建残留、第一层即资产目录）：

```bash
# 打包单个资产
python scripts/package.py experts/lao-dao-editor
python scripts/package.py skills/ask-matt
python scripts/package.py teams/deep-research-crew

# 打包全部
python scripts/package.py --all

# 按类型
python scripts/package.py --all --type skill
```

产物在 `build/<id>.zip`，**第一层就是资产目录**，可直接拖进后台。

> 平台大小上限：技能包 3 MB，专家包 20 MB。按 zip 体积判断。

## 3. 上传

后台路径：**发布管理 → 技能 / 专家 → 右上角「创建」**

1. 把 zip 拖进上传区，平台自动解压、识别、生成 ID
2. 确认信息页：包内字段自动读出（页面上改不了；要改就回源文件改后重新打包）
3. 补齐页面上必填的三项：
   - **市场展示分类**：⚠️ **务必勾选含「AI 创作」的分类**（可多选，建议 AI创作 + 内容创作 / 技术工程）
   - **服务类目**：至少 1 个、最多 5 个，建议「工具-办公」
   - **头像**：可沿用包内头像，也可重传
4. 核对右侧预览（名称 / 简介 / 头像）→ 继续 → 确认汇总 → **提交**

## 4. 平台硬性字段规范

| 字段 | 规范 |
|---|---|
| `name` / `plugin` / `agentName` | **三处一致**，且为全平台全局唯一（不是账号内唯一） |
| `displayDescription.zh` | **40–50 字**（平台硬校验） |
| Team 型 `profession.zh` | 必须与 `displayName.zh` 完全一致 |
| `members[].name` / `tags[]` | 新解析器要求有 `zh` 与 `en`；`tags[]` **必须恰好 3 个**（多于或少于都会报「tags 须固定 3 个」） |
| `defaultInitPrompt` | 必须等于 `quickPrompts[0]` |
| 头像 | 512×512，≤500 KB |
| 团队 | 必须有 `settings.json`（`{"agent": "<team-id>-team-lead"}`） |
| 专家包 | 第一层是 `agents/`+`skills/`+`.codebuddy-plugin/`，**没有 SKILL.md**；传到技能页会报「未找到 SKILL.md」 |

## 5. 常见报错与解法

| 报错 | 原因 | 解法 |
|---|---|---|
| 名称「已被占用」 | `name` 全平台全局唯一 | 换更具体的前缀名，并把 `plugin.json` 的 `name`、`plugin`、`agentName`、agent 文件名、目录名**一起改**，重新打包 |
| 驳回：所选类目与应用类目不符，至少应包含高度生成或 AI 创作类目 | 展示分类没落到 AI 类目 | 上传页**市场展示分类**务必勾含 AI 创作的分类；仍被驳回则把 `categoryId` 改为 `04-DataAI`，版本升一位，重新打包 |
| 驳回：企业开发者才支持深度生成 / AI 创作类目 | 个人主体可能受该类目限制 | 二选一：① 走企业认证；② 邮件 openworkbuddy@tencent.com 确认个人主体可用类目组合 |
| 解析失败：缺少 display_name / description_zh 等 | frontmatter 字段不全 | 补齐九个字段再打包 |
| YAML 解析报错 | 冒号后没空格、多余引号 | `key: value`，引号尽量不用 |
| 多套一层目录 | 打包时把外层包装目录打进去 | 第一层必须是资产目录（`package.py` 已保证） |

## 6. 审核与发布

- 提交后等审核：官方口径 **7 个工作日**，开发者实测约 **18 小时**
- 结果在开放平台**通知中心**看；若开放平台与 WorkBuddy 用同一微信号注册，WorkBuddy 消息中心也会推
- 通过后状态变成「待发布」，**必须再点一次「发布」**才真正上架
- 发布方式选 **「公开发布」**（全部用户可见、市场可搜可装）；「专用发布」只给账号下的 Buddy 应用用
- 发布后卡片上有「更新版本 / 设置 / 下架」，后续维护都在这

## 7. 本地安装（客户端可见）

上架的是**副本**，本地不受影响。本地要让客户端「我的专家」里能看到，用专家管理技能注册：

```bash
EM="/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/expert-manager"
EXP="$WORKBUDDY_CONFIG_DIR/plugins/marketplaces/my-experts/plugins/<asset-id>"

python3 "$EM/scripts/validate_expert.py" "$EXP"   # 校验
python3 "$EM/scripts/register_expert.py" "$EXP"   # 注册
```

注册后重启 WorkBuddy。可在**两个配置目录都注册**（`~/.workbuddy-ai` 与 `~/.workbuddy`）做冗余。

## 8. 版本迭代

改本地文件 → `sync_manifests.py --force` → `build_registry.py` → `validate.py` → `package.py` → 上传新 zip。

> 上架版本与本地版本相互独立；改本地不影响已上架版本，两边要一致需手动同步后重新打包上传。

兜底：<https://open.workbuddy.cn/docs/expert> 、openworkbuddy@tencent.com
