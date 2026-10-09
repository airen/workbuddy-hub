# to-questionnaire 使用示例

**类别**：其他 | **版本**：1.0.0

## 场景

需要向某人收集信息做决策。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我做份问卷，问团队要不要上 Redis` |
| agent | 加载 `skills/to-questionnaire/SKILL.md`：

1. 识别决策点
2. 生成问卷
3. 输出可直接发给团队的问卷 |

## 产出

问卷 Markdown，可直接发给目标人群

## 验证

问题能支撑决策；无诱导性问题

## 资产位置

- 定义：`skills/to-questionnaire/SKILL.md`
- 元数据：`skills/to-questionnaire/manifest.yaml`
