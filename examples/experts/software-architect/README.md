# software-architect 使用示例

**类别**：开发与工程 | **版本**：1.0.0
**编排技能**：software-architecture

## 场景

需要架构决策支持。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我做架构权衡分析` |
| agent | 选择专家 "方权衡"（`software-architect`）：

1. 识别质量属性（性能/可扩展性/一致性...）
2. 风格选型（微服务/单体/事件驱动...）
3. 领域建模
4. 分布式数据设计
5. 产出 ADR + 图表 |

## 产出

ADR 文档 + 架构图表

## 验证

每个决策有理由和权衡分析

## 资产位置

- 定义：`experts/software-architect/.codebuddy-plugin/plugin.json`
- 人格：`experts/software-architect/agents/software-architect.md`
- 元数据：`experts/software-architect/manifest.yaml`
