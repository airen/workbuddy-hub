# 使用示例

本目录不是空泛的骨架——每个示例都**对应仓库里一个真实存在的资产**，
告诉你它在什么场合被触发、走完整个流程后产出什么。

> 资产本身就在 `skills/`、`experts/`、`teams/` 里，示例只是「用法说明书」。
> 资产的权威定义是其中的 `SKILL.md` / `plugin.json` / `agents/*.md`，
> 元数据由 `scripts/sync_manifests.py` 派生，不需要在示例里重复抄录。

## 示例一览

| 示例 | 类型 | 引用的真实资产 | 场景一句话 |
|---|---|---|---|
| [single-skill/](single-skill/) | 技能 | `skills/pr` | 发 PR 前自动生成带证据与合并风险的正文 |
| [single-expert/](single-expert/) | 专家 | `experts/lao-dao-editor` | 把一段 AI 腔文稿改成像人写的自然文本 |
| [expert-team/](expert-team/) | 专家团 | `teams/engineering-delivery` | 一个功能从需求澄清到四路审查的完整交付 |
| [skill-chain/](skill-chain/) | 技能链 | `skills/to-spec` → `skills/to-tickets` → `skills/implement` | 一段对话沉淀成规格、工单，再按工单实现 |

## 怎么读示例

每个示例目录下的 `README.md` 结构一致：

1. **触发方式** —— 用户说什么话时该用它
2. **输入 / 输出** —— 喂进去什么、出来什么
3. **过程** —— 关键步骤与会调用的子能力
4. **验证** —— 怎么确认它跑对了
5. **资产路径** —— 对应到仓库里的哪个目录，可直接打开看源码

## 每个示例里有什么

每个示例目录含**两份文件**：

- `README.md` —— 用法说明书（怎么触发、输入输出、过程、验证）
- `*-example.md` / `chain-workflow.md` —— **真实示例产物**：
  按该技能/专家/专家团的模板实际产出的一份文档，
  可直接对照模板看「填好之后长什么样」

> 新增资产时，请同步在这里补一个示例；示例与 `registry/*.yaml` 保持一致
>（新增/改名资产后跑 `python scripts/build_registry.py` 会发现对不上的地方）。
