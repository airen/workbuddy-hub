# 04 · plan（技术方案）

**命令**：`plan`　**频率**：每个功能一次　**产物**：`plan.md`、`research.md`、`data-model.md`、`quickstart.md`、`contracts/`

## 它解决什么问题

规格回答 **WHAT/WHY**；方案回答 **HOW**。这是整个流程里**唯一**允许出现技术栈、框架、架构、接口设计的地方。

**硬前置**：`spec.md` 必须存在。原版只要求 `specify` 先于 `plan`（`clarify` 是可选关卡）—— 但如果规格里有 `[NEEDS CLARIFICATION]`，先回去澄清，别带着模糊设计。

## 执行步骤

### 1. 读规格

读 `spec.md` 的需求、用户故事、验收标准。**逐条**问自己：这个需求，技术上意味着什么？

### 2. 章程合规（GATE，必须过）

对照 `.specify/memory/constitution.md`：

- **Phase 0 研究之前**检查一次
- **Phase 1 设计之后**再检查一次

违反条款 → 写进 `## Complexity Tracking` 表（Violation / Why Needed / Simpler Alternative Rejected Because）。**没进表 = 阻断。**

### 3. Phase 0：技术调研 → `research.md`

- 技术选型的候选与取舍
- 库兼容性、性能影响、安全隐患
- 组织约束（数据库标准、认证要求、部署策略）
- 每个结论记下**理由**

### 4. Phase 1：设计 → `data-model.md` / `contracts/` / `quickstart.md`

| 产物 | 内容 |
|---|---|
| `data-model.md` | 领域概念 → 数据模型；实体、关系、关键约束 |
| `contracts/` | 接口契约（OpenAPI / 类型定义 / 事件 schema）。**先于实现创建** |
| `quickstart.md` | 快速验证指南 —— 别人拿到代码后怎么在最短路径上跑通 |

同时填 `plan.md` 的：

- **Summary**：主需求 + 技术路线
- **Technical Context**：语言/版本、主要依赖、存储、测试、目标平台、项目类型、性能目标、约束、规模
- **Project Structure**：文档树 + 源码树（**删掉没用到的 Option 标签**，只留真实路径）
- **Structure Decision**：为什么选这个结构，引用真实目录

### 5. 定文件创建顺序（测试优先）

原版强制这个顺序，**照着来**：

```
contracts/ → 契约测试 → 集成测试 → e2e 测试 → 单元测试 → 源码（让测试通过）
```

先写契约再写实现，先写测试再写源码。

## 模板纪律

用 `templates/plan-template.md`。关键约束：

- **Technical Context 里没定的项，写 `NEEDS CLARIFICATION`**，不要留空也不要瞎填。
- **计划保持高层可读**。大段代码样例、详细算法 → 下沉到 `implementation-details/` 文件，别塞进 `plan.md`。
- **`tasks.md` 不是这一步的产物** —— 它由 `tasks` 命令生成。plan 里只写它会存在。

## 收尾

告诉用户：技术栈结论、架构结构、章程关卡是否通过（有无例外）、下一步是 `checklist` 还是直接 `tasks`。
