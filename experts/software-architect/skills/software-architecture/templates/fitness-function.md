# 适应度函数定义模板

> 适应度函数 = 对架构特征（质量属性）的**自动化验证**。
> 把"架构应该怎样"从文档里的约定，变成**可执行、会失败的检查**。
> 完整说明见 `references/02-architecture-thinking.md`。

## 1. 定义卡

```markdown
### FF-XXX：<名称>

- **守护的架构特征**：<质量属性，如"模块边界不被穿透">
- **关联决策**：<ADR-XXXX>
- **触发时机**：每次提交 / 每日 / 发布前 / 按需
- **执行方式**：自动化 / 人工检查清单
- **通过标准**：<明确的阈值或断言>
- **失败时动作**：阻断合并 / 告警 / 记录待办
- **所有者**：<谁负责维护>
```

## 2. 常见适应度函数清单

| 架构目标 | 类型 | 检查方式 |
|---------|------|---------|
| 分层不被穿透 | 结构 | ArchUnit / dependency-cruiser 断言依赖方向 |
| 无循环依赖 | 结构 | 依赖图分析（jdeps、madge、import-linter） |
| 模块边界（模块化单体） | 结构 | 断言模块 A 不 import 模块 B 的 internal 包 |
| 服务不直连他人数据库 | 结构 | 静态扫描连接串 / 网络策略 |
| 性能 SLO | 行为 | 压测断言 P99 < 阈值，CI 失败 |
| 错误率 SLO | 行为 | 发布后金丝雀分析，超标自动回滚 |
| 依赖许可合规 | 合规 | SCA 扫描（如 license-checker），禁止 GPL 进闭源 |
| 依赖漏洞 | 安全 | SCA 扫描（npm audit / trivy / snyk） |
| 包体积上限 | 约束 | 构建后断言（主包 < 2MB） |
| API 向后兼容 | 契约 | OpenAPI diff / proto 兼容性检查 |
| 契约测试 | 契约 | 消费者驱动契约（Pact）验证 |
| 可观测性覆盖 | 运维 | 断言所有对外接口都产生 trace |
| 文档同步 | 流程 | 断言新增服务在 C4 图中有节点 |
| 密钥不进版本库 | 安全 | pre-commit 密钥扫描（gitleaks） |
| 测试覆盖率下限 | 质量 | 覆盖率门槛（注意：覆盖率是弱信号） |
| 关键路径有超时 | 弹性 | 静态检查所有 HTTP/RPC 客户端都设置了超时 |
| 配置项有默认值 | 稳健 | 静态检查 |
| 数据库迁移可回滚 | 运维 | 迁移脚本检查 |

## 3. 技术手段速查

| 语言/场景 | 工具 |
|----------|------|
| Java | ArchUnit、jQAssistant、jdeps |
| .NET | NetArchTest |
| JS/TS | dependency-cruiser、madge、eslint-plugin-boundaries、ts-arch |
| Python | import-linter、pytest-archon |
| Go | go-arch-lint、goda |
| 通用 | 自定义脚本扫描 import / 依赖图 |
| 性能 | k6、JMeter、wrk、Gatling |
| 契约 | Pact、Schemathesis、buf（proto） |
| 安全 | Trivy、Snyk、gitleaks、semgrep |
| 云基础设施 | OPA / Conftest（策略即代码） |

## 4. 示例：模块化单体的边界守护

**目标**：`order` 模块不得直接依赖 `payment` 模块的内部实现，只能通过 `payment-api` 包。

### Java（ArchUnit）

```java
@ArchTest
static final ArchRule order_must_not_access_payment_internal =
    noClasses()
        .that().resideInAPackage("..order..")
        .should().dependOnClassesThat()
        .resideInAPackage("..payment.internal..")
        .because("订单模块只能通过 payment-api 访问支付模块（ADR-0012）");

@ArchTest
static final ArchRule no_cycles_between_modules =
    slices().matching("com.example.(*)..")
        .should().beFreeOfCycles();
```

### TypeScript（dependency-cruiser）

```js
// .dependency-cruiser.js
module.exports = {
  forbidden: [
    {
      name: 'order-no-payment-internal',
      comment: '订单模块只能通过 payment-api 访问支付模块（ADR-0012）',
      severity: 'error',
      from: { path: '^src/modules/order' },
      to: { path: '^src/modules/payment/(?!api)' },
    },
    {
      name: 'no-circular',
      severity: 'error',
      from: {},
      to: { circular: true },
    },
  ],
};
```

### 分层规则（Java，六边形）

```java
@ArchTest
static final ArchRule domain_must_not_depend_on_infrastructure =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
        .resideInAnyPackage("..infrastructure..", "..adapter..", "org.springframework..")
        .because("领域层必须独立于框架与基础设施（端口与适配器）");
```

## 5. 示例：性能 SLO 适应度函数

```javascript
// k6 脚本 + CI 断言
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 1000 },  // 爬坡到 1000 并发
    { duration: '5m', target: 1000 },  // 稳态
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    // 适应度函数：P99 < 200ms，错误率 < 0.1%
    http_req_duration: ['p(99)<200'],
    http_req_failed: ['rate<0.001'],
  },
};

export default function () {
  const res = http.get('https://staging.example.com/api/orders');
  check(res, { 'status is 200': (r) => r.status === 200 });
}
```

> CI 中运行 k6，阈值不通过则 exit 1 → **构建失败**。

## 6. 示例：契约兼容性检查

```bash
# 检查 proto 是否有破坏性变更
buf breaking --against '.git#branch=main'

# 检查 OpenAPI 向后兼容性
oasdiff breaking base.yaml new.yaml
```

## 7. 落地建议

| 建议 | 说明 |
|------|------|
| **从 2–3 个开始** | 只给**关键驱动因素**配适应度函数，不要一次上十几个 |
| **优先放 CI** | 能自动失败才有约束力；只在文档里的规则等于没有 |
| **失败要阻断** | 只警告不阻断的检查会被忽略 |
| **允许有期限的豁免** | 老代码可豁免，但要有**递减的豁免清单**和到期日 |
| **关联 ADR** | 每个适应度函数注明它守护哪个决策 |
| **定期回顾** | 需求变了，适应度函数也要变；删除失效的 |
| **避免伪信号** | 覆盖率、代码行数等是弱信号；优先用行为/结构断言 |

## 8. 反模式

| 反模式 | 问题 |
|--------|------|
| 适应度函数只写在文档里 | 无人执行，半年后必然被违反 |
| 一次上 20 个检查 | 噪音大，团队开始忽略 |
| 只告警不阻断 | 变成"已知问题"清单 |
| 无豁免机制 | 老代码导致 CI 长期红，团队索性关掉 |
| 用弱信号（覆盖率）当主要指标 | 可以被轻易"刷"过，不代表质量 |
| 与 ADR 脱节 | 没人知道这个检查为什么存在，需求变了也不敢删 |
| 只检查结构，不检查行为 | 漏掉性能/可用性等真正重要的属性 |
