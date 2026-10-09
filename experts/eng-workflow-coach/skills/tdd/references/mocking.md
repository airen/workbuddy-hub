# 什么时候该 mock

只在**系统边界**上 mock：

- 外部 API（支付、邮件等）
- 数据库（有时 —— 优先用测试数据库）
- 时间/随机性
- 文件系统（有时）

不要 mock：

- 你自己的类/模块
- 内部协作者
- 任何你能控制的东西

## 为可 mock 而设计

在系统边界上，设计容易 mock 的接口：

**1. 用依赖注入**

把外部依赖传进来，而不是在内部创建：

```typescript
// 容易 mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// 难以 mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 优先用 SDK 风格的接口，而不是通用的 fetcher**

为每个外部操作建一个专门的函数，而不是用一个带条件分支的通用函数：

```typescript
// GOOD: 每个函数都能独立 mock
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: mock 里还得写条件逻辑
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK 风格的好处：

- 每个 mock 只返回一种确定的形状
- 测试的准备工作里没有条件逻辑
- 更容易看出一个测试覆盖了哪些端点
- 每个端点都有类型安全
