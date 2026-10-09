# pr 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

准备合入 PR 前，自动生成符合规范的正文。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我写 PR 描述` |
| agent | 加载 `skills/pr/SKILL.md`，从 diff 提取要点，生成三段式正文：

```markdown
## Summary

重构结算逻辑...

## Evidence

- **Before:** ...
  **After:** ...

## Merge Danger

**Door:** 双向门
**Blast Radius:** Cart 类接口未变
``` |

## 产出

Markdown 文本（可直接粘贴到 GitHub PR 界面）

## 验证

三段齐全（Summary / Evidence / Merge Danger），Evidence 有 before/after 对比

## 资产位置

- 定义：`skills/pr/SKILL.md`
- 元数据：`skills/pr/manifest.yaml`
