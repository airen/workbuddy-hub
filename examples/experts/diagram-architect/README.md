# diagram-architect 使用示例

**类别**：开发与工程 | **版本**：1.0.0
**编排技能**：diagram-architect, diagram-design, svg-diagram, dashmotion, documd-visuals, archify

## 场景

需要画技术图表。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `画一个微服务架构图` |
| agent | 选择专家 "江图南"（`diagram-architect`）：

1. 定图型：架构图
2. 定出口：SVG（内联）+ PNG（落盘）
3. 调度绘图能力库（svg-diagram / dashmotion / archify 等）
4. 过质检闸门（svg-lint）
5. 交付

产出：SVG + PNG 图表 |

## 产出

SVG + PNG 图表文件

## 验证

图表无断链；符合设计系统；质检闸门全过

## 资产位置

- 定义：`experts/diagram-architect/.codebuddy-plugin/plugin.json`
- 人格：`experts/diagram-architect/agents/diagram-architect.md`
- 元数据：`experts/diagram-architect/manifest.yaml`
