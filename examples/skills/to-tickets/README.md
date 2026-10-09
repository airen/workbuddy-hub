# to-tickets 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

规格已定，需要拆成可执行的工单。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `把规格拆成工单` |
| agent | 加载 `skills/to-tickets/SKILL.md`，拆出工单：

```
ticket-1: 定义接口（无阻塞）
ticket-2: 实现空购物车处理（阻塞于 ticket-1）
ticket-3: 实现多商品 CSV 生成（阻塞于 ticket-2）
```
本地每张工单一个文件 |

## 产出

一组工单文件（含阻塞关系声明）

## 验证

工单图无环；最小工单集可独立运行

## 资产位置

- 定义：`skills/to-tickets/SKILL.md`
- 元数据：`skills/to-tickets/manifest.yaml`
