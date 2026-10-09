# domain-modeling 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

发现领域术语混乱，需要统一概念。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `理一下购物车领域的模型` |
| agent | 加载 `skills/domain-modeling/SKILL.md`：

1. 扫描代码和文档，找出模糊术语
2. 挑战术语："item" 是指单个商品还是数量？
3. 更新 GLOSSARY.md |

## 产出

更新后的 GLOSSARY.md，可能的 ADR 文件

## 验证

代码注释和文档使用统一术语；无歧义

## 资产位置

- 定义：`skills/domain-modeling/SKILL.md`
- 元数据：`skills/domain-modeling/manifest.yaml`
