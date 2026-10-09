# 命名规范

## 资产 ID（目录名）

- 一律 **kebab-case**：小写字母、数字、连字符。例：`market-research`、`deep-research-crew`、`de-ai-rewrite`。
- **全局唯一**，且与下列位置保持一致：
  - Skill：`SKILL.md` frontmatter 的 `name`。
  - Expert/Team：`.codebuddy-plugin/plugin.json` 的 `name`、`plugin`、`agentName`（团队还要与 `agents/<id>-team-lead.md` 文件名）一致。
- 平台对 `name` 是**全平台全局唯一**的，重名会被拒。起名时加足够具体的前缀。

## 文件与目录

- 专家人格文件：`agents/<id>.md`（单专家）或 `agents/<team-id>-<role>.md`（团队各成员）。
- 专家团主理人：`agents/<team-id>-team-lead.md`，并在 `settings.json` 里 `"agent": "<team-id>-team-lead"`。
- 头像：`avatars/<id>.png`（单专家）或 `avatars/team.jpg`（团队），建议 512×512、≤500KB。
- 技能目录：`references/`（深度资料）、`scripts/`（可执行脚本）、`assets/`（静态资源/头像）、`evals/`（评测用例）。

## 分类（category）

从固定枚举中选一个，写入 `manifest.yaml` 的 `category`，并与 `plugin.json` 的 `categoryId` 对齐：

| hub category | 含义 | 常见 platform categoryId |
|---|---|---|
| `research` | 调研与信息检索 | `04-DataAI` |
| `development` | 开发与工程 | `02-Engineering` |
| `content` | 内容生产 | `06-ContentCreative` |
| `design` | 设计与视觉 | （平台暂无精确对应，先填 `other` 并在 `platform_category` 记原值） |
| `business` | 商业分析与运营 | （同上） |
| `other` | 其他/未分类 | — |

映射逻辑见 `scripts/_hublib.py` 的 `CATEGORY_ID_MAP` / `SKILL_CATEGORY_MAP`。

## 版本

- 语义化版本 `x.y.z`，`SKILL.md` frontmatter 与 `plugin.json` 的 `version` 必须一致。
- 修改资产后升版本并记录到 `CHANGELOG.md`。

## 标签（tags）

- 取自 `plugin.json` 的 `tags[].zh`（中文优先）。
- 同一资产标签数量建议 ≤ 5。
