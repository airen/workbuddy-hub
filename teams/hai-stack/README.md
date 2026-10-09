# 软件迭代专家团（hai-stack）

> 把一次软件迭代做对：先判断值不值得做，再设计边界、按测试驱动落地，用证据确认，最后把文档沉淀干净。

一个基于 [@海拉鲁编程客](https://github.com/hylarucoder) 的 [hai-stack](https://github.com/hylarucoder/hai-stack) 方法论封装的 WorkBuddy **Team 型专家团**。主理人调度六名成员，内置 19 个技能，覆盖从「这事要不要做」到「文档改干净」的完整链路。

## 类型

Team 型（多角色协作团队）— 1 名主理人 + 6 名成员

## 团队构成

| 成员 | 职业 | 负责的技能 | 什么时候找它 |
|------|------|-----------|-------------|
| 纪循章 `hai-stack-team-lead` | 迭代总控 | —（编排调度） | 综合性、跨阶段的问题 |
| 甄可行 `hai-idea-judge` | 需求判断官 | `hai-idea` `hai-prd` | 值不值得做、是不是伪需求、写 PRD、PRD 拆分 |
| 房清源 `hai-architect` | 系统架构师 | `hai-architecture` `entity-model-auditor` `hai-naming` | 系统太绕、模块边界、字段该存还是该算、起名 |
| 施必达 `hai-engineer` | 实施工程师 | `hai-goal` `hai-tdd` `hai-debug` `hai-ast-grep` | 拆阶段、先写测试、排障、批量改写 |
| 郑辨真 `hai-reviewer` | 质量评审官 | `code-review-and-quality` `write-technical-acceptance-report` | review diff、验收报告、发布就绪 |
| 文一章 `hai-doc-officer` | 技术文档官 | `hai-audit-docs` `hai-rewrite-doc` `hai-simplified-technical` `hai-visual-explainer` `readme-beautifier` | 文档过时、按最新结论重写、写得干净点、做成图 |
| 毕开疆 `hai-corrector` | 方案纠偏官 | `geju` `goudi` `hai-razor` | 打开格局、压实第一步、概念剃刀 |

## 六个阶段

```
判断 → 设计 → 动手 → 确认 → 沉淀 → 纠偏
```

任何跳步都会返工。团队按阶段串行/并行调度，跨成员信息一律经主理人中转。

## 预设 Workflow

| # | 触发 | 编排 |
|---|------|------|
| W1 | 这事值不值得做 | 甄可行 → 五选一裁决 + 最强反对意见 + 最小验证 |
| W2 | 系统太绕，改不动 | 房清源 → 追调用链、定位复杂度中心、给方案与第一个证明点 |
| W3 | 从需求到落地（全链路） | 判断 → 设计（架构 ∥ 纠偏）→ 计划 → 实施 → 评审验收 → 文档沉淀 |
| W4 | 线上故障 | 施必达 诊断 → （要求修复时）最小修复 → 郑辨真 评审 |
| W5 | 评审 + 验收 | 郑辨真 → 缺陷评审 → 需求追溯矩阵 + GO / CONDITIONAL GO / NO-GO |
| W6 | 文档全流程 | 文一章 → 先审计定事实 → 按结论分流到重写/简化/排版/可视化 |
| W7 | 方案太飘 / 被兼容绑架 | 毕开疆 → 格局判断 → 压实第一步 |

单一维度的问题不走 Workflow，主理人直接路由到对应成员。

## 招牌能力：四十六规则

`hai-simplified-technical` 是本专家团最「看得见」的能力——按 ASD-STE100（简化技术英语）第 8 版第一部分改编的**简化技术中文**，46 条规则（28 条硬规则 + 18 条软规则），分九章：

1. **词**（1.1–1.5）：一个概念一个词、一个词一个意思、用术语表、不用含糊词、用实义动词
2. **名词短语**（2.1–2.3）：最多两个「的」、不堆名词、的/地/得分用
3. **动词**（3.1–3.4）：不用包装动词、主动句写出谁做、不写「正在」、情态词只用六个
4. **句子**（4.1–4.5）：一句一件事、写明主语、代词只指一个东西、写明句间关系、三项以上用列表
5. **操作步骤**（5.1–5.5）：一步一条指令、动词开头、条件在前、一句 ≤ 40 字、说明与指令分开
6. **说明文字**（6.1–6.5）：结论在段首、一段一个主题、一句 ≤ 50 字、数字写明条件、分清已做和计划
7. **警告**（7.1–7.4）：警告在步骤前、先指令后后果、一条一个风险、警告/注意两级
8. **标点和长度**（8.1–8.9）：全角标点、全文一种引号、中英文空格、数量用数字、范围用「–」、日期两种写法、句长数法、列表句号
9. **写作习惯**（9.1–9.6）：术语唯一译名、代码名加反引号、官方产品名、不用成语比喻、称「你」和「我们」、引用能定位

规则全文见 `skills/hai-simplified-technical/references/rules-zh.md`（英文版 `rules-en.md`），并附带机械检查脚本 `scripts/check.py`。

## 使用示例

- 我想加一个 AI 命令推荐器，但不确定是不是伪需求，值得投入两周吗？
- 系统太绕了，从 server 和 worker 入口看看为什么改重试规则这么费劲。
- 线上把 `RETRY_ENABLED=false` 后仍重复请求，本地却正常。先定位原因，不要改代码。
- review 当前 diff，优先找真实 bug 和缺少的验证。
- 对照实现检查并修复 README，批准的未来需求不要改成现有行为。
- 这份 runbook 写得太绕，按简化技术中文改一遍，意思不要变。
- 把格局打开。／用苟帝压实第一步。／用剃刀看看哪些概念该合并。

## 内置技能（19 个）

| 分组 | 技能 |
|------|------|
| 判断 | `hai-idea` `hai-prd` |
| 设计 | `hai-architecture` `entity-model-auditor` `hai-naming` |
| 动手 | `hai-goal` `hai-tdd` `hai-debug` `hai-ast-grep` |
| 确认 | `code-review-and-quality` `write-technical-acceptance-report` |
| 沉淀 | `hai-audit-docs` `hai-rewrite-doc` `hai-simplified-technical` `hai-visual-explainer` `readme-beautifier` |
| 纠偏 | `geju` `goudi` `hai-razor` |

技能来自 [hai-stack](https://github.com/hylarucoder/hai-stack)，保留原始 `SKILL.md`、中文版 `SKILL.zh_CN.md`、`references/`、`scripts/`、`assets/`。

## 设计取舍

- **团队而不是单专家**：19 个技能覆盖 6 个互不相同的分析域，每个域都有用户会直接问它的问题，符合「能独立成 agent」的标准。
- **一个概念一个角色**：判断、设计、动手、确认、沉淀、纠偏——每个成员覆盖一个完整分析域，域内多能力归并，不跨域。
- **技能原样内置**：不重写技能内容，保留上游的完整 references 与脚本，避免转述丢失细节。
- **主理人不代写**：专业产出必须由对应成员输出后再采信，主理人只做编排与汇编。

## 头像

头像已生成在 `avatars/` 目录下。如需替换为自定义头像，要求：
- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 许可证与署名

见 `ATTRIBUTION.md`。方法论与技能版权归原作者所有，采用 **CC BY-NC 4.0**（署名—非商业性使用）。个人使用、学习、研究与非商业项目可直接使用；**商业用途需要单独授权**。
