# wayfinder 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

项目太大，需要规划路线。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `这个项目太大了，帮我规划一下` |
| agent | 加载 `skills/wayfinder/SKILL.md`：

1. 识别关键决策点
2. 生成决策票据地图（issue tracker）
3. 逐张推进，直到路线清晰 |

## 产出

决策票据地图（系列 issue）

## 验证

地图覆盖所有关键决策；路线清晰可执行

## 资产位置

- 定义：`skills/wayfinder/SKILL.md`
- 元数据：`skills/wayfinder/manifest.yaml`
