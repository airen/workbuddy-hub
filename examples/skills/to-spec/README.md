# to-spec 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

对话已讨论过需求，需要沉淀成规格说明。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `把刚才聊的写成规格` |
| agent | 加载 `skills/to-spec/SKILL.md`，综合对话上下文：

```markdown
## Problem Statement
用户需要从购物车导出数据...

## Solution
在 Cart 类上新增 export_to_csv(path)...

## Seams
- Cart.export_to_csv(path: str) -> None
```
发布到 issue 追踪器，打 ready-for-agent |

## 产出

规格 Markdown 文件（发布到 issue 追踪器）

## 验证

规格包含 Problem/Solution/Seams/Acceptance Criteria 四节

## 资产位置

- 定义：`skills/to-spec/SKILL.md`
- 元数据：`skills/to-spec/manifest.yaml`
