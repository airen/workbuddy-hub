# GLOSSARY.md 格式

## 结构

```md
# {上下文名称}

{一到两句话，描述这个上下文是什么、为什么存在。}

## Language

**Order**:
{对这个术语一到两句话的描述}
_Avoid_: Purchase, transaction

**Invoice**:
交付之后发给客户的一份付款请求。
_Avoid_: Bill, payment request

**Customer**:
下单的个人或组织。
_Avoid_: Client, buyer, account
```

## 规则

- **要有主见。** 当同一个概念有多个词时，挑最好的那个，把其余的列在 `_Avoid_` 下。
- **定义要紧凑。** 最多一到两句话。定义它*是*什么，而不是它*做*什么。
- **只收录本项目上下文特有的术语。** 通用编程概念（超时、错误类型、工具模式）不属于这里，即便项目大量使用它们。加一个术语之前先问：这是本上下文独有的概念，还是通用编程概念？只有前者才该收。
- 当自然形成聚集时，**把术语归到子标题下**。如果所有术语都属于同一个内聚的领域，用一份平铺列表即可。

## 单上下文 vs 多上下文仓库

**单上下文（大多数仓库）：** 仓库根目录一个 `GLOSSARY.md`。

**多上下文：** 仓库根目录一个 `GLOSSARY-MAP.md` 列出各个上下文、它们住在哪里，以及彼此如何关联：

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): 接收并跟踪客户订单
- [Billing](./src/billing/GLOSSARY.md): 生成发票并处理付款
- [Fulfillment](./src/fulfillment/GLOSSARY.md): 管理仓库拣货与发货

## Relationships

- **Ordering → Fulfillment**: Ordering 发出 `OrderPlaced` 事件；Fulfillment 消费它们以开始拣货
- **Fulfillment → Billing**: Fulfillment 发出 `ShipmentDispatched` 事件；Billing 消费它们以生成发票
- **Ordering ↔ Billing**: 共享 `CustomerId` 和 `Money` 类型
```

本技能会推断适用哪种结构：

- 如果存在 `GLOSSARY-MAP.md`，读它来找出各个上下文
- 如果只存在一个根目录的 `GLOSSARY.md`，就是单上下文
- 如果两者都不存在，就在第一个术语被敲定时惰性创建根目录的 `GLOSSARY.md`

当存在多个上下文时，推断当前话题跟哪一个相关。如果不清楚，就问。
