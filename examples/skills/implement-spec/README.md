# implement-spec 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

完整规格说明，需要并发实现多个工单。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `按规格实现购物车导出功能` |
| agent | 加载 `skills/implement-spec/SKILL.md`：

1. 读规格和关联工单
2. 构建阻塞图，识别可并发工单
3. 在集成分支上并发调度子代理
4. 完成后跑 code-review
5. 结掉所有工单 |

## 产出

集成分支上的完整实现，code-review 报告，所有工单已结

## 验证

集成分支测试全绿；code-review 无阻断项

## 资产位置

- 定义：`skills/implement-spec/SKILL.md`
- 元数据：`skills/implement-spec/manifest.yaml`
