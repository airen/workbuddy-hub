# AI 项目推进官（ai-project-pilot）

用「**立项 → 计划 → 执行与监控 → 验收与上线**」四阶段方法，推进 AI 产品与 AI 项目落地。方法底座：**PMP 项目管理 × AI 软件工程**。

一个 AI 项目最危险的不是技术不行，而是价值没说清、责任没到人、任务没拆细、上线没人管。这个技能把四张方法论图解变成 agent 可执行的工作流和 10 份可直接填写的交付物模板。

## 目录结构

```text
ai-project-pilot/
├── SKILL.md                          # 技能定义（WorkBuddy / Claude Code 通用）
├── AGENTS.md                         # Codex / Cursor 等 AGENTS.md 系工具入口
├── README.md                         # 本文件
├── references/                       # 四阶段完整方法 + 工程护栏
│   ├── 01-initiation.md
│   ├── 02-planning.md
│   ├── 03-execution-monitoring.md
│   ├── 04-acceptance-launch.md
│   └── 05-engineering-guardrails.md  # 可选：把工程原则接进项目管理
└── templates/                        # 10 份交付物模板
    ├── 项目章程.md
    ├── 相关方登记册.md
    ├── 风险登记册.md
    ├── WBS与里程碑.md
    ├── 状态报告.md
    ├── 变更申请.md
    ├── 验收记录.md
    ├── 运营交接包.md
    ├── 复盘报告.md
    └── 工程规范.md                    # CLAUDE.md / AGENTS.md 骨架
```

## 三端安装

| 平台 | 做法 |
|---|---|
| **WorkBuddy** | 把 `ai-project-pilot/` 整个目录拷到 `~/.workbuddy-ai/skills/`，重启后在对话里说「推进一个 AI 项目」即自动触发。或从应用市场直接安装。 |
| **Claude Code** | 把 `ai-project-pilot/` 拷到 `~/.claude/skills/`（个人级）或项目内 `.claude/skills/`（项目级）。`SKILL.md` 的 frontmatter 是标准 Agent Skills 格式，Claude 按 `description` 自动触发。 |
| **Codex / Cursor** | 把 `AGENTS.md` 拷到你的项目根目录（或 `~/.codex/AGENTS.md` 作为全局），agent 即按四阶段流程工作。若同时保留 `references/`、`templates/`，AGENTS.md 会引用到它们。 |

> 三个平台读的是同一个方法内核，只是入口文件不同：WorkBuddy 与 Claude 读 `SKILL.md`，Codex 系读 `AGENTS.md`。

## 用法示例

- 「我要做一个客服 AI 助手，帮我做立项」→ 产出项目章程（含业务目标、范围边界、相关方、成功标准）
- 「这个 AI 项目怎么拆任务、怎么排期」→ 产出 WBS 与里程碑、进度成本基准
- 「项目在跑，帮我出一份周报」→ 产出状态报告（进度/质量/成本/业务四维度）
- 「AI 项目怎么验收、怎么上线」→ 产出验收记录、运营交接包、复盘报告
- 「给这个项目定一份工程规范」→ 产出 `CLAUDE.md` / `AGENTS.md` 骨架（含变更速查表）

## 工程护栏（可选章节）

项目管理管「做什么、值不值、过不过关口」，工程规范管「代码怎么写」。`references/05-engineering-guardrails.md` 把两者接在三个接口上：**计划阶段的设计关口、执行阶段的变更准入、收尾阶段的决策归档**。

处理原则是**分清方法层与实现层**：

- **方法层**（换个项目仍成立）→ 写进本技能。如「架构与领域优先」「变更可验证可观测可回滚」「删除优于兼容」。
- **实现层**（项目专属）→ 写进项目自己的工程规范。如具体命令（`bun run precheck`）、单文件行数上限、分层模型名、依赖清单位置。

所以原 `CLAUDE.md` 里的规则**不是原样搬进来**，而是：可移植的部分成为技能的默认原则，项目专属的部分变成 `templates/工程规范.md` 里的空格。

## 方法来源

整理自公开实践总结「AI 项目推进管理」四阶段图解（PMP 方法 × AI 软件工程），本技能为其可执行化封装。内容为原创整理与转写，无第三方代码依赖。

## 许可

本技能为原创方法论封装，可自由分发。作者：大漠。
