# 软件架构师 · 方权衡

一个务实的软件架构师专家：把模糊的系统目标，变成**经得起变化、团队协作和规模化考验的决策**。

## 类型

Agent 型（单个 AI 专家）

## 功能

覆盖软件架构的完整知识体系（10 大能力域），但**组织方式是决策导向而非知识罗列**：

| # | 能力域 | 内容 |
|---|--------|------|
| 01 | 基础与角色 | 架构定义、架构师 vs 高工 vs 技术主管、质量属性与 -ility、功能性 vs 非功能性需求、利益相关者与约束 |
| 02 | 架构思维 | 权衡分析、ADR、适应度函数、技术债与演化压力、康威定律与团队拓扑 |
| 03 | 设计原则 | SOLID、内聚与耦合、边界与关注点分离、依赖倒置/端口与适配器、YAGNI/KISS/深模块、复杂度预算 |
| 04 | 架构风格与模式 | 分层/N 层、模块化单体、微服务 vs 单体、六边形/洋葱/整洁、事件驱动/CQRS/事件溯源 |
| 05 | 领域建模 | DDD 战略、限界上下文与上下文映射、聚合/实体/值对象、通用语言、防腐层 |
| 06 | 数据与持久化 | 数据归属、SQL vs NoSQL 驱动因素、复制与分区、事务/Saga/Outbox、多语言持久化 |
| 07 | 分布式系统 | CAP/PACELC、一致性模型与 Quorum、故障/重试/幂等、Raft 直觉、分布式计算误区 |
| 08 | 集成与 API | 同步 vs 异步、队列/发布订阅/事件流、API 契约与版本、编排 vs 协调、网关/服务网格 |
| 09 | 演化与生产环境 | 演化式架构与绞杀者、可观测性、SLI/SLO/错误预算、弹性模式、安全与密钥管理 |
| 10 | 实践与沟通 | C4 模型、文档化视图、架构 Kata 与设计评审、经典案例（电商/Feed/支付）、进阶之路 |

### 核心方法论

工作流是**决策导向**的七步：澄清驱动因素 → 质量属性场景化 → 列备选（≥3，含"什么都不做"）→ 权衡分析 → 给建议（推荐/理由/代价/前提/重估触发点）→ 落档（ADR + C4 + 适应度函数）→ 演化路径。

### 五条信条

1. **没有免费的午餐** —— 任何决策都有代价，说不出代价就是没想清楚
2. **没有量级不谈架构** —— 先要数字（QPS、数据量、团队规模、SLA）
3. **架构是决策，不是图** —— 图是产物，不是决策本身
4. **可逆性决定谨慎程度** —— 单向门慎重，双向门快试
5. **最好的架构是能演化的架构**

## 包含的技能

### `software-architecture`

| 目录 | 内容 |
|------|------|
| `references/` | 10 个能力域各一份深度参考 + `decision-frameworks.md`（权衡矩阵/ATAM-lite/质量属性场景/复杂度预算/容量估算）+ `anti-patterns.md`（30+ 条反模式速查） |
| `templates/` | `adr.md`、`architecture-review.md`、`c4-diagram.md`（含 Mermaid 骨架）、`fitness-function.md`、`quality-attribute-scenario.md`、`architecture-kata.md` |
| `scripts/` | `new-adr.sh` —— 从模板脚手架 ADR，自动编号 |

## 使用示例

- 「帮我评审这个系统设计，指出真正的风险和取舍」
- 「我们在考虑把单体拆成微服务，先做一次权衡分析再决定拆不拆」
- 「把这个架构决策写成一份 ADR，包含备选方案和后果」
- 「订单和库存的边界该怎么划？帮我用 DDD 战略设计理一下」
- 「这个接口延迟 P99 是 800ms，帮我做一次延迟预算分解」
- 「帮我把这三个质量属性写成可度量的场景」
- 「我的服务老是被下游拖垮，帮我设计一套弹性方案」
- 「帮我给这个模块设计适应度函数，放进 CI 里守护边界」

## 目录结构

```
software-architect/
├── .codebuddy-plugin/plugin.json
├── agents/
│   └── software-architect.md          # Agent 主提示词（路由表 + 七步工作流）
├── skills/
│   └── software-architecture/
│       ├── SKILL.md                   # 技能入口（路由 + 核心工作法）
│       ├── references/                # 10 个能力域 + 决策框架 + 反模式
│       ├── templates/                 # 6 份可复用模板
│       └── scripts/new-adr.sh
├── avatars/
│   └── software-architect.png
└── README.md
```

## 头像

头像已自动生成在 `avatars/` 目录下。如需替换为自定义头像，要求：

- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 安装

将专家包目录放到专家目录下：

```
~/.workbuddy-ai/plugins/marketplaces/my-experts/plugins/software-architect/
```

然后运行注册命令使其可见：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
python3 scripts/package_expert.py <expert-dir> <output-dir>
```
