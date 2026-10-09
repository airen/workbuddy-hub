# implement 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

有工单或规格，开始 TDD 实现。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `开始实现购物车导出功能` |
| agent | 加载 `skills/implement/SKILL.md`，按工单执行：

```
[Red] 写测试 -> [Green] 实现 -> [Refactor] 重构
提交：feat(cart): export to CSV
```
收尾调 code-review |

## 产出

可运行的代码 + 测试（按工单原子提交）

## 验证

测试全绿；code-review 无 Critical

## 资产位置

- 定义：`skills/implement/SKILL.md`
- 元数据：`skills/implement/manifest.yaml`
