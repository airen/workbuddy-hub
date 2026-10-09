---
name: software-architecture
description: Deep reference library and decision method for software architecture. Use when designing, reviewing, or documenting a system architecture — quality attributes and -ilities, tradeoff analysis, ADRs, fitness functions, technical debt, Conway's Law; SOLID, coupling/cohesion, boundaries, ports and adapters, YAGNI/KISS, deep modules, complexity budget; layered/modular monolith/microservices/hexagonal/onion/clean/event-driven/CQRS/event sourcing; DDD strategic design, bounded contexts, context mapping, aggregates, ubiquitous language, anti-corruption layer; data ownership, SQL vs NoSQL, replication, partitioning, transactions, Saga, Outbox, polyglot persistence; CAP/PACELC, consistency models, quorum, failure modes, idempotency, Raft, fallacies of distributed computing; REST vs gRPC vs async, queues, pub/sub, event streaming, API contracts and versioning, choreography vs orchestration, gateways and service mesh; evolutionary architecture, strangler fig, observability, SLIs/SLOs/error budgets, resilience patterns, security and secrets; C4 model, architecture kata, design reviews, and classic case studies.
---

# Software Architecture

本技能是「软件架构师」专家的知识库与方法论。它不是一份可以照着念的百科，而是一套**做决策的工具**：先把问题放进正确的框架，再调用对应的深度参考，最后产出可评审的决策产物。

## Overview

架构的本质是**在约束下做取舍**。因此本技能的组织方式不是"知识点罗列"，而是：

```
驱动因素 → 质量属性 → 备选方案 → 权衡 → 决策 → 落档 → 演化
```

每份参考都遵循同一节奏：**它解决什么问题 → 核心概念 → 怎么用 → 代价与陷阱**。读到任何一处，都要能回答"用它的代价是什么"。

## When to Use

- 设计一个新系统 / 新模块的架构
- 评审一份已有的架构设计或技术方案
- 在多个技术方案之间做选型决策
- 划分子系统边界、服务边界、团队边界
- 定义质量属性、SLO、非功能需求
- 规划从单体到分布式（或反向）的迁移路径
- 写 ADR、画 C4 图、组织架构评审
- 面试准备 / 架构能力体系化学习

## 使用方法（三步）

1. **定位**：从下方路由表找到问题落在哪个能力域（可多选）。
2. **加载**：读对应的 `references/*.md`。任何决策类问题，**先读 `decision-frameworks.md`**。
3. **产出**：用 `templates/` 里的模板把结论固化下来（ADR / 评审清单 / C4 图 / 适应度函数 / 质量属性场景）。

## 路由表

### 十大能力域

| # | 模块 | 参考文件 | 关键词 |
|---|------|---------|--------|
| 01 | 基础与角色 | `references/01-foundations-and-role.md` | 架构定义、架构师 vs 高工 vs 技术主管、质量属性与 -ility、功能性 vs 非功能性需求、利益相关者、约束与驱动因素 |
| 02 | 架构思维 | `references/02-architecture-thinking.md` | 权衡分析、ADR、适应度函数、技术债与演化压力、康威定律与团队拓扑 |
| 03 | 设计原则 | `references/03-design-principles.md` | SOLID、内聚与耦合、边界与关注点分离、依赖倒置/端口与适配器、YAGNI/KISS/深模块、复杂度预算 |
| 04 | 架构风格与模式 | `references/04-architecture-styles.md` | 分层/N 层、模块化单体、微服务 vs 单体、六边形/洋葱/整洁、事件驱动/CQRS/事件溯源 |
| 05 | 领域建模 | `references/05-domain-modeling.md` | DDD 战略、限界上下文与上下文映射、聚合/实体/值对象、通用语言、防腐层 |
| 06 | 数据与持久化 | `references/06-data-and-persistence.md` | 数据归属与建模、SQL vs NoSQL 驱动因素、复制与分区、事务/Saga/Outbox、多语言持久化 |
| 07 | 分布式系统 | `references/07-distributed-systems.md` | CAP/PACELC、一致性模型与 Quorum、故障模式/重试/幂等、共识（Raft 直觉）、分布式计算的误区 |
| 08 | 集成与 API | `references/08-integration-and-api.md` | 同步（REST/gRPC）vs 异步、队列/发布订阅/事件流、API 设计/契约/版本控制、编排 vs 协调、网关/服务网格/发现 |
| 09 | 演化与生产环境 | `references/09-evolution-and-production.md` | 演化式架构与绞杀者模式、可观测性、SLI/SLO/错误预算、弹性（熔断/隔板/超时）、安全/最小权限/密钥管理 |
| 10 | 实践与沟通 | `references/10-practice-and-communication.md` | C4 模型与图表、文档化视图与决策、架构 Kata 与设计评审、经典案例（电商/Feed 流/支付）、开发者→架构师进阶 |

### 横向工具

| 用途 | 文件 |
|------|------|
| 权衡矩阵、ATAM-lite、质量属性场景六要素、复杂度预算、可逆性（单向门/双向门）判断 | `references/decision-frameworks.md` |
| 架构反模式速查（审查设计时逐条对照） | `references/anti-patterns.md` |

### 模板（`templates/`）

| 模板 | 用途 |
|------|------|
| `adr.md` | 架构决策记录（MADR 风格），记录决策、备选、后果 |
| `architecture-review.md` | 设计评审清单（驱动因素、质量属性、边界、数据、集成、运维、风险） |
| `c4-diagram.md` | C4 四层图 + Mermaid 骨架 + 常见画法错误 |
| `fitness-function.md` | 适应度函数定义（把架构约束变成可自动验证的检查） |
| `quality-attribute-scenario.md` | 质量属性场景工作表（六要素 + 度量） |
| `architecture-kata.md` | 架构 Kata 工作表（限时设计演练） |

### 脚本（`scripts/`）

| 脚本 | 用途 |
|------|------|
| `new-adr.sh` | 从模板脚手架一份新 ADR，自动编号与命名 |

## 核心工作法（记住这五条）

1. **先要数字，再谈架构。** 没有量级（QPS、数据量、团队规模、SLA）的方案都是想象。缺数字就先声明假设。
2. **把形容词变成场景。** "高可用/高性能/可扩展"不是需求；六要素场景（刺激源→刺激→制品→环境→响应→度量）才是。
3. **至少三个备选，含"什么都不做"。** 只有一个方案等于没有决策。
4. **代价必写。** 说不出代价的方案说明还没想清楚。这条是本技能的硬规矩。
5. **先判可逆性。** 单向门（难回退）慎重论证；双向门（易回退）快速实验。**别把双向门当单向门论证，那是最大的浪费。**

## 常用速查

### 架构风格选择的第一性问题

| 你真正的约束 | 通常的起点 |
|-------------|-----------|
| 团队小（< 10 人）、边界还没稳定 | 模块化单体（modular monolith） |
| 团队多、边界清晰、独立部署是刚需 | 微服务（按限界上下文切） |
| 领域复杂、业务规则多 | DDD 战略设计 + 六边形架构 |
| 读写负载差异巨大 | CQRS（读模型独立优化） |
| 需要完整审计/回放/时态查询 | 事件溯源（Event Sourcing） |
| 大量异步、多消费者、削峰 | 事件驱动 + 消息队列 |
| 遗留系统要渐进替换 | 绞杀者模式（Strangler Fig） |

> ⚠️ 上表是**起点**，不是结论。任何一格都要走一遍 `decision-frameworks.md` 的权衡流程。

### 复杂度预算（记住这个心智模型）

架构师的工作是**控制复杂度**，不是消灭它。每次引入一个模式（微服务、事件溯源、服务网格），都在**支出复杂度预算**。预算的偿付方式是**团队能持续交付**。当团队开始说"改一处要动五个服务""本地跑不起来"，说明预算透支了——该做减法。

## 硬约束

- **不做无前提的推荐**。任何模式都有适用条件；被问"X 好不好"时先问场景。
- **不臆造事实**。行业规范、平台规格、组件能力不确定时，明说并建议核实官方文档。
- **不做代码级实现**。本技能设计接缝与契约，不写业务逻辑。
- **不推荐许可不清的组件**。推荐第三方时主动核对开源许可与合规要求。
- **优先可演化而非最优**。为不确定的未来做过度设计，是架构师最大的失误。
