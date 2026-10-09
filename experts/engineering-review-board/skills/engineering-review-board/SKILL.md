---
name: engineering-review-board
description: 全仓库代码审查入口。当用户要求"审查/review 整个仓库""给这个项目做一次体检""评估架构 / 技术债 / 安全 / 测试 / 性能""这个代码库能不能放心接手或上线"，或要把一次大范围审查拆成可执行、有证据、说明范围的结论时使用。流程是：先建立仓库地图，再按需调用专项审查技能（架构、技术债、安全、性能、依赖供应链、测试、可访问性等），全程默认只读，结论必须挂证据，抽样必须说明范围。不用于单文件或单次 diff 的聚焦评审（那用 code-review），也不用于实现新功能或修复 bug。
---

# Engineering Review Board · 全仓库代码审查入口

这是**全仓库代码审查的统一入口**。它不自己产出专业结论，而是负责把一次"审查一个仓库"的请求**拆成一条有顺序、有证据、有边界的链**：先建图，再分域审查，按需调用专项技能，最后用证据把结论固定下来。

**核心立场**：审查的价值不在"找出多少问题"，而在**每条结论都能被复现、被质疑、被追溯**。宁可少说一条，不要多说一条站不住的。

## 什么时候用 / 不用

**用**：用户要对一个仓库或一个较大模块做**大范围审查**——接手前摸底、上线前体检、技术债盘点、架构评估、安全与测试质量评估、重构前诊断。

**不用**：
- 单次 diff / 单个 PR 的聚焦评审 → 直接用 [`code-review`](../code-review/SKILL.md)
- 用户要**实现**新功能或**修复** bug → 这是开发任务，不是审查
- 已有一个明确的活跃故障要定位 → 用 [`systematic-debugging`](../systematic-debugging/SKILL.md)
- 只做设计期的威胁建模、不涉及已有代码 → 用 [`threat-modeling`](../threat-modeling/SKILL.md)

## 三条不可越界的硬规矩

1. **默认只读。** 审查全程**不修改任何文件**。只有用户**明确要求修复**时才动代码，且修复与审查分成两件事：先出审查结论，用户确认后再改。
2. **不许声称"全覆盖"。** 任何抽样、局部或启发式审查，**必须在报告里写明审查范围**（看了哪些目录/文件/模块、跳过了什么、为什么）。把"我抽查了 12 个文件"说成"我审完了整个仓库"是欺骗。
3. **结论必须挂证据。** 每条结论都要能被指向：`file:line`、命令输出、搜索结果、或"已搜索 X 未发现 Y"。找不到证据的，标为「未验证」或降级成「待确认」，**不许当作结论输出**。

---

## 六步流程

### Step 0 — 先定审查契约（别猜）

开工前用最少的话确认四件事；用户已经说清楚的就不重复问：

| 要确认 | 为什么 |
|---|---|
| **范围** | 全仓库 / 指定模块 / 指定技术栈。范围决定后面抽样怎么声明。 |
| **目标** | 架构、技术债、安全、性能、测试质量、发布就绪——用户最关心哪个？ |
| **深度与预算** | 快速体检（走一遍六个维度、只报高危）vs 深审（按域展开、逐条证据）。 |
| **是否允许跑命令** | 构建 / 测试 / lint / 静态分析会产出最强证据，但会改工作区状态。**默认不跑**，需用户点头。 |

> 用户说"你自己看着办"时，选**快速体检 + 只读 + 不跑命令**，并在报告里声明这个默认。

### Step 1 — 建立仓库地图

**目的**：在判断任何"好坏"之前，先知道这个仓库**长什么样**。没有地图的审查，结论都是悬空的。

**采集手法**（用只读手段，优先精确搜索而不是通读）：
- **模块与目录**：顶层布局、各目录职责、单包还是多包 / monorepo
- **入口点**：程序入口、路由注册、命令注册、事件订阅、定时任务、公开 API 面
- **依赖**：依赖清单与锁文件（`package.json` / `Cargo.toml` / `pyproject.toml` / `composer.json` / `go.mod` 等）、内部模块间的依赖方向
- **关键行为**：核心业务路径、数据模型与持久化、鉴权与信任边界、对外集成
- **工程设施**：构建与 CI 配置、测试布局与覆盖率门槛、Lint / 格式化配置、文档与 `AGENTS.md` / `CONTRIBUTING.md`

**产出**：一段"仓库地图"，用文字或树形结构给出——**模块 → 依赖方向 → 关键行为 → 已识别的信任边界**。同时列出**没看懂 / 没覆盖**的部分，这些会在最后一步变成「未验证事项」。

> 地图不用漂亮，要**准确**。标错一个依赖方向，后面所有架构结论都会跟着错。

### Step 2 — 审查架构与技术债

在地图上叠加"结构"与"时间"两个镜头：

- 加载 [`architecture-review`](../architecture-review/SKILL.md)：模块边界、依赖方向、端口与适配器、分层是否被穿透
- 加载 [`technical-debt-audit`](../technical-debt-audit/SKILL.md)：维护成本、复杂度、重复、依赖健康度、测试缺口、架构侵蚀、文档漂移
- 若地图显示是特定架构风格，**追加**对应镜头：[`clean-architecture`](../clean-architecture/SKILL.md) / [`hexagonal-architecture`](../hexagonal-architecture/SKILL.md) / [`onion-architecture`](../onion-architecture/SKILL.md) / [`domain-driven-design`](../domain-driven-design/SKILL.md) / [`domain-modeling`](../domain-modeling/SKILL.md)
- 接口/契约是审查重点时，追加 [`api-design`](../api-design/SKILL.md)

**关注**：边界是否清晰、依赖方向是否合理、演进是否可持续。**不要用"是否符合某个模式"当判据**——判据是"这个结构是否让下一次变更更容易或更难"。

### Step 3 — 审查代码行为

这一步用**代码行为的四个维度**扫一遍。**必须先加载 [`review-verification-protocol`](../review-verification-protocol/SKILL.md)**（证据闸门，它规定了每条结论在写出来之前必须过哪几关），再按维度加载镜头：

| 维度 | 加载 | 看什么 |
|---|---|---|
| **正确性 / 可维护性** | [`code-review`](../code-review/SKILL.md) | 逻辑是否正确、错误处理是否完整、边界条件、命名与结构 |
| **安全性** | [`security-review`](../security-review/SKILL.md) + [`security-review-evidence`](../security-review-evidence/SKILL.md)；涉及信任边界设计时加 [`threat-modeling`](../threat-modeling/SKILL.md)；依赖面加 [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md) | 鉴权、输入校验、密钥、注入面、信任边界、依赖漏洞 |
| **可靠性 / 性能** | [`performance-review`](../performance-review/SKILL.md) | 热路径、无界输入、并发与资源、超时与重试、可观测性 |
| **测试质量** | [`testing-strategy`](../testing-strategy/SKILL.md) | 信心缺口、边界覆盖、脆弱测试、套件可维护性；语言专项测试质量见路由表 |

语言/技术栈相关的深水区（Rust 所有权、PHP 动态特性、SQL 查询形态等），按 Step 4 的路由表追加对应技能。

### Step 4 — 按需调用专项技能

**只加载当前问题需要的镜头**，不要一次全上——82 个技能全加载会稀释判断力。

完整路由表见下方「技能路由表」。用法：

1. 地图 + 前两步暴露出**具体领域**（比如"这是个 Rust 项目，且用了大量 async + SQLx"）
2. 从路由表挑出对应技能，逐个加载
3. 每个专项技能产出的结论，**同样要过 `review-verification-protocol` 的证据闸门**

### Step 5 — 用证据支持结论

每一条结论都用**同一个四段式**表述，缺一段就不算结论：

| 段 | 内容 |
|---|---|
| **问题** | 一句话说清是什么，带 `file:line` 或模块/符号定位 |
| **审查范围** | 这条结论覆盖了什么（哪些文件/模块），**以及没覆盖什么** |
| **已执行检查** | 为了支撑它，实际跑了什么——读了哪些文件、搜了什么、跑了什么命令、看了什么输出 |
| **未验证事项** | 还没证实、但可能相关的部分；明确标「未验证」 |

**严重度分级**（四档，别自造）：

| 级别 | 含义 |
|---|---|
| **Blocker** | 会导致数据丢失、安全漏洞、线上不可用；不修不能上线 |
| **Major** | 明确的缺陷或高风险债务，应在近期修复 |
| **Minor** | 真实但影响有限的问题，可排期 |
| **Nit** | 风格/偏好，非缺陷；**不得当作阻塞项** |

**抽样纪律**：报告里必须有一段「本次审查范围」，写明——审查了哪些路径、用什么方法抽样（全量 / 随机 / 按风险选样）、样本量、以及**没看的部分**。宁可显得保守，不可显得全面。

### Step 6 — 保留项目设计选择

**审查不是"按教科书重写"，而是"在项目自己的上下文里判断"。** 每条发现必须落到下面四类之一，**不许混为一谈**：

| 分类 | 判据 | 报告里怎么处理 |
|---|---|---|
| **缺陷 Defect** | 与既定意图不符，且会造成实际后果 | 按严重度报，给最小修复建议 |
| **技术债 Tech Debt** | 是过去有意的取舍，现在开始拖慢变更 | 报，但写明"它是怎么来的、代价什么时候开始显现" |
| **可接受取舍 Acceptable Tradeoff** | 在当前约束下合理 | **明确写"这是可接受的"**，并说明理由与前提；不要报成问题 |
| **待验证假设 Hypothesis** | 看起来可疑但证据不足 | 标「待验证」，给出验证方法，**不当结论用** |

**尊重上下文**：读注释、`AGENTS.md`、设计文档、迁移脚本、feature 文件，确认某个"怪"是不是有意为之。**模式纯洁性不是判据**——只要结构是自洽的、可测试的、能演进的，"不标准"也可以是对的。

---

## 技能路由表（全 82 个专项技能）

### 审查镜头（Lenses）

| 技能 | 何时加载 |
|---|---|
| [`architecture-review`](../architecture-review/SKILL.md) | 审边界、依赖方向、端口与适配器 |
| [`code-review`](../code-review/SKILL.md) | 审变更的正确性与可维护性；Step 3 的基础镜头 |
| [`security-review`](../security-review/SKILL.md) | 变更触及鉴权、加密、密钥、信任边界、输入校验、命令执行 |
| [`security-review-evidence`](../security-review-evidence/SKILL.md) | 与 `security-review` 配套的证据清单（**不单独用**） |
| [`review-verification-protocol`](../review-verification-protocol/SKILL.md) | **强制**：报告任何结论之前 |
| [`adversarial-review`](../adversarial-review/SKILL.md) | 需要独立质疑既有结论、合并就绪度、隐藏回归时 |
| [`performance-review`](../performance-review/SKILL.md) | 审性能与可扩展性：热路径、查询形态、并发、渲染 |
| [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md) | 依赖审计、SBOM/SCA、CVE 通告、供应链风险 |
| [`release-readiness`](../release-readiness/SKILL.md) | 评估合并/发布就绪度：测试、文档、迁移、灰度、回滚 |
| [`ux-accessibility-review`](../ux-accessibility-review/SKILL.md) | 审 UI/UX 质量、响应式、交互态、WCAG 可访问性 |
| [`prompt-engineering-review`](../prompt-engineering-review/SKILL.md) | 审提示词与 agent 指令接口 |
| [`rust-code-review`](../rust-code-review/SKILL.md) | Rust 专项：所有权、生命周期、unsafe |

### 架构与领域

| 技能 | 何时加载 |
|---|---|
| [`clean-architecture`](../clean-architecture/SKILL.md) | 依赖规则、实体、用例/交互器、接口适配 |
| [`hexagonal-architecture`](../hexagonal-architecture/SKILL.md) | 端口与适配器、外部驱动的边界 |
| [`onion-architecture`](../onion-architecture/SKILL.md) | 同心环：领域 / 应用 / 基础设施 |
| [`domain-driven-design`](../domain-driven-design/SKILL.md) | 限界上下文、模块边界、复杂业务逻辑 |
| [`domain-modeling`](../domain-modeling/SKILL.md) | 审战术 DDD：聚合、实体、值对象、不变量、通用语言 |
| [`api-design`](../api-design/SKILL.md) | 定义、变更、评审服务或公开接口契约 |

### 技术债与诊断

| 技能 | 何时加载 |
|---|---|
| [`technical-debt-audit`](../technical-debt-audit/SKILL.md) | 全仓或聚焦的技术债盘点与修复优先级 |
| [`systematic-debugging`](../systematic-debugging/SKILL.md) | 有活跃 bug / 失败测试 / 不稳定行为要定位 |
| [`root-cause-analysis`](../root-cause-analysis/SKILL.md) | 复发性故障、事故、回归、系统性流程缺口 |
| [`brainstorming`](../brainstorming/SKILL.md) | 需求模糊、需要先发散出多个方案再收敛 |

### 测试与质量

| 技能 | 何时加载 |
|---|---|
| [`testing-strategy`](../testing-strategy/SKILL.md) | 审测试策略、信心缺口、TDD/BDD 适配、脆弱测试 |
| [`test-driven-development`](../test-driven-development/SKILL.md) | 新增/变更行为、修 bug 时的 TDD 流程 |
| [`behavior-driven-development`](../behavior-driven-development/SKILL.md) | 澄清用户可见行为与验收标准 |
| [`gherkin`](../gherkin/SKILL.md) | `.feature` 文件、Scenario、步骤定义 |
| [`playwright-e2e`](../playwright-e2e/SKILL.md) | 浏览器 E2E 测试的新增、调试与评审 |
| [`php-testing-quality`](../php-testing-quality/SKILL.md) | PHP 测试与质量闸（PHPUnit / Pest / Behat） |
| [`rust-testing-quality`](../rust-testing-quality/SKILL.md) | Rust 测试与质量闸 |
| [`object-pascal-testing-quality`](../object-pascal-testing-quality/SKILL.md) | Object Pascal / Delphi 测试与质量闸 |

### 安全设计

| 技能 | 何时加载 |
|---|---|
| [`threat-modeling`](../threat-modeling/SKILL.md) | 设计期威胁建模、滥用场景、攻击者建模 |

### 语言 / 技术栈工程

| 技能 | 何时加载 |
|---|---|
| [`python-engineering`](../python-engineering/SKILL.md) | Python 源码、uv、打包、lint |
| [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md) | JS / TS 源码、lint、格式化、构建 |
| [`rust-engineering`](../rust-engineering/SKILL.md) | Rust crate、模块、公开 API、领域逻辑 |
| [`php-engineering`](../php-engineering/SKILL.md) | PHP 源码、Composer 清单与锁文件 |
| [`ruby-engineering`](../ruby-engineering/SKILL.md) | Ruby 源码与脚本 |
| [`csharp-dotnet-engineering`](../csharp-dotnet-engineering/SKILL.md) | C# / .NET 工程 |
| [`powershell-engineering`](../powershell-engineering/SKILL.md) | 跨平台 PowerShell `.ps1` / `.psm1` |
| [`object-pascal-engineering`](../object-pascal-engineering/SKILL.md) | Object Pascal / Delphi 工程 |
| [`svelte-sveltekit-engineering`](../svelte-sveltekit-engineering/SKILL.md) | Svelte / SvelteKit 组件与路由 |
| [`webassembly-engineering`](../webassembly-engineering/SKILL.md) | Wasm / WAT / WASI / WIT 与组件模型 |

### 设计模式与反模式

| 技能 | 何时加载 |
|---|---|
| [`python-design-patterns`](../python-design-patterns/SKILL.md) / [`python-antipatterns`](../python-antipatterns/SKILL.md) | Python 惯用法 / 坏味道 |
| [`php-design-patterns`](../php-design-patterns/SKILL.md) / [`php-antipatterns`](../php-antipatterns/SKILL.md) | PHP 模式 / 坏味道 |
| [`rust-design-patterns`](../rust-design-patterns/SKILL.md) / [`rust-antipatterns`](../rust-antipatterns/SKILL.md) | Rust 惯用法 / 坏味道 |
| [`typescript-javascript-design-patterns`](../typescript-javascript-design-patterns/SKILL.md) / [`typescript-javascript-antipatterns`](../typescript-javascript-antipatterns/SKILL.md) | TS/JS 模式 / 坏味道 |
| [`object-pascal-design-patterns`](../object-pascal-design-patterns/SKILL.md) / [`object-pascal-antipatterns`](../object-pascal-antipatterns/SKILL.md) | Object Pascal 模式 / 坏味道 |

### 数据与 SQL

| 技能 | 何时加载 |
|---|---|
| [`sql-engineering`](../sql-engineering/SKILL.md) | 与数据库无关的 SQL 读写与优化 |
| [`postgresql-sql-engineering`](../postgresql-sql-engineering/SKILL.md) | PostgreSQL 专项 |
| [`mysql-mariadb-sql-engineering`](../mysql-mariadb-sql-engineering/SKILL.md) | MySQL / MariaDB 专项 |
| [`sqlite-sql-engineering`](../sqlite-sql-engineering/SKILL.md) | SQLite 专项 |
| [`rust-persistence-sql`](../rust-persistence-sql/SKILL.md) | Rust SQLx / SeaQuery / SQL 库 |
| [`data-platform-engineering`](../data-platform-engineering/SKILL.md) | 源到落地的数据管道工程 |
| [`random-data-identifiers`](../random-data-identifiers/SKILL.md) | 随机数、生成标识符、测试数据 |

### 工程实践与流程

| 技能 | 何时加载 |
|---|---|
| [`documentation-engineering`](../documentation-engineering/SKILL.md) | Markdown 文档、README、文档重构 |
| [`git-workflows`](../git-workflows/SKILL.md) | 分支、远端、历史、重写、冲突、恢复 |
| [`git-commit`](../git-commit/SKILL.md) | 提交与提交信息质量 |
| [`semantic-versioning`](../semantic-versioning/SKILL.md) | 版本号变更是否合规 |
| [`ci-release-engineering`](../ci-release-engineering/SKILL.md) | CI / 发布流水线配置 |
| [`container-engineering`](../container-engineering/SKILL.md) | Dockerfile / OCI 镜像 / Compose |
| [`observability-engineering`](../observability-engineering/SKILL.md) | 可观测性、遥测、生产诊断 |
| [`parallelism-engineering`](../parallelism-engineering/SKILL.md) | CPU 密集、数据并行、任务并行的分解 |
| [`script-engineering`](../script-engineering/SKILL.md) | POSIX shell / Bash 等脚本 |
| [`justfiles`](../justfiles/SKILL.md) | Justfile 的编写、重构与审计 |
| [`mcp-server-engineering`](../mcp-server-engineering/SKILL.md) | MCP server 的创建、重构与评审 |

### 前端与样式

| 技能 | 何时加载 |
|---|---|
| [`css-scss-styling`](../css-scss-styling/SKILL.md) | CSS / SCSS / Tailwind |
| [`impeccable`](../impeccable/SKILL.md) | 界面设计、评审、打磨、无障碍观感（UI 工艺） |
| [`suggest-lucide-icons`](../suggest-lucide-icons/SKILL.md) | 为概念/界面位置选真实存在的 Lucide 图标 |

### 领域专用

| 技能 | 何时加载 |
|---|---|
| [`internationalization-localization`](../internationalization-localization/SKILL.md) | i18n / l10n、Fluent `.ftl` |
| [`zod-engineering`](../zod-engineering/SKILL.md) | Zod schema 的选择、迁移、评审与优化 |
| [`digital-asset-management`](../digital-asset-management/SKILL.md) | 照片/视频入库、资产标识、不可变原件 |
| [`gossamer-engineering`](../gossamer-engineering/SKILL.md) | Gossamer `.gos` / `project.toml` |
| [`piwigo-plugin-engineering`](../piwigo-plugin-engineering/SKILL.md) | Piwigo 插件 |
| [`photo-supreme-scripting`](../photo-supreme-scripting/SKILL.md) | Photo Supreme 内嵌 Object Pascal 脚本 |
| [`rust-async-web`](../rust-async-web/SKILL.md) | Tokio、异步任务、取消、超时 |
| [`rust-desktop-gui`](../rust-desktop-gui/SKILL.md) | Rust 原生桌面 GUI |
| [`hound-web-research`](../hound-web-research/SKILL.md) | 用 Hound MCP 做公开网络调研 |
| [`create-agent-skill`](../create-agent-skill/SKILL.md) | 审查对象包含 agent 技能/指令本身时 |

---

## 输出：审查报告结构

报告按下面顺序组织，**不要省略任何一节**：

```markdown
# 仓库审查报告：<仓库名>

## 0. 审查契约
- 范围：<全仓 / 模块 / 技术栈>
- 目标：<架构 / 技术债 / 安全 / 性能 / 测试 / 发布就绪>
- 深度：<快速体检 / 深审>；是否运行了命令：<是/否 + 命令清单>
- 只读声明：本次审查未修改任何文件

## 1. 仓库地图
<模块 → 依赖方向 → 关键行为 → 信任边界>
<明确列出：没看懂 / 未覆盖的部分>

## 2. 架构与技术债
<结论（四段式）>

## 3. 代码行为（正确性 / 安全 / 可靠性与性能 / 测试质量）
<结论（四段式）>

## 4. 按域专项发现
<按加载的专项技能分组>

## 5. 结论汇总表

| # | 级别 | 分类 | 问题 | 位置 | 建议 |
|---|---|---|---|---|---|
| 1 | Blocker | 缺陷 | ... | `path/file.ts:42` | ... |

## 6. 设计选择说明（保留判断）
- **可接受取舍**：<哪些"看起来怪但合理"的选择，为什么接受>
- **待验证假设**：<哪些可疑但证据不足，怎么验证>

## 7. 本次审查范围与未验证事项
- 实际覆盖：<路径 / 抽样方法 / 样本量>
- 未覆盖：<...>，原因：<...>
- 未验证：<...>
- **不得声称全覆盖**：本报告为<抽样 / 局部 / 全量>审查
```

## 报告写作纪律

- **先结论后证据**，每条结论独立可读，不依赖上下文
- **数值与位置要具体**：`src/auth/session.ts:128`，不写"相关文件"
- **区分"没做"和"做了没通过"**：验证状态必须诚实（passed / failed / not run + 原因）
- **脱敏**：报告可能被分享，**不要粘贴密钥、token、个人隐私、内网地址**；发现代码里已有敏感信息，作为一条发现上报（标注位置，不复制值）
- **语言跟随用户**：用户用中文就用中文
- **修复是另一件事**：报告完成后，若用户要求修复，再逐条确认范围后动手；**不要边审边改**
