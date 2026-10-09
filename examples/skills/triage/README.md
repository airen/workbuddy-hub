# triage 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

有 issue/PR 需要分类和分诊。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我 triage 一下这些 issue` |
| agent | 加载 `skills/triage/SKILL.md`：

1. 读取 issue/PR 列表
2. 分类：bug / feature / docs / ...
3. 核验：是否可复现？是否有足够信息？
4. 必要时拷问澄清
5. 输出 agent 可执行的简报 |

## 产出

分类后的 issue 列表 + agent 执行简报

## 验证

每个 issue 有明确分类和执行建议

## 资产位置

- 定义：`skills/triage/SKILL.md`
- 元数据：`skills/triage/manifest.yaml`
