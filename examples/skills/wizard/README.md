# wizard 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

需要引导用户完成手动配置步骤。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我配置一下 CI secrets` |
| agent | 加载 `skills/wizard/SKILL.md`：

1. 识别需要人工操作的步骤
2. 生成交互式向导
3. 逐阶段确认 |

## 产出

交互式 bash 向导脚本

## 验证

向导能引导用户完成配置，每步有确认

## 资产位置

- 定义：`skills/wizard/SKILL.md`
- 元数据：`skills/wizard/manifest.yaml`
