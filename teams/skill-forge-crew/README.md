# 技能工程流水线专家团（skill-forge-crew）

把 Skill 用成流水线：需求问透、规格落地、测试驱动、质量把关、仓库设防。

> 素材来源：一份按用途整理的 Claude Skills 清单（Anthropic 官方仓库 / Matt Pocock 的 Skills / SkillsMP 社区市场等公开来源），本包按其方法论重写为可在 WorkBuddy 直接执行的形式。

## 它解决什么

很多人用 AI 还是「提一个问题、拿一个答案」。这份包把开发过程串成一条可以反复使用的流水线：

- 需求没问透不动手
- 测试没变红不写实现
- 仓库没设防不交代码
- **同一套动作做到第三次，就固化成 Skill**

## 团队成员

| 成员 | 名字 | 职责 | 持有技能 |
|---|---|---|---|
| 主理人 | 费鸣 | 编排调度、技能固化、提交与发布说明 | skill-authoring、skill-discovery、commit-and-changelog |
| 需求澄清与规划师 | 闻澈 | 追问需求、写 PRD、排计划、拆任务、接口比选 | requirement-interview、write-a-prd、prd-to-plan、prd-to-issues、design-an-interface、brainstorming |
| 实现工程师 | 柯建 | 测试驱动实现、前端规范、代码定位、上下文压缩 | tdd、react-best-practices、code-search、context-optimization |
| 质量守卫 | 秦检 | 功能质检、代码审查、根因排错、Issue 分诊 | qa、code-review、systematic-debugging、issue-triage |
| 仓库守卫 | 卫库 | 提交前钩子、危险命令拦截、依赖体检、重构规划 | repo-guardrails、refactor-planning |

## 内置技能（19 个）

**技能自造**
- `skill-authoring` — 把重复流程写成可复用 Skill（起草 → 试跑 → 迭代 → 结构整理）
- `skill-discovery` — 先找现成方案，找不到再自己写

**需求与规划**
- `requirement-interview` — 一次一个问题把需求问透
- `write-a-prd` — PRD 六要素，含显式非目标
- `prd-to-plan` — 分阶段实施顺序，每阶段一个端到端切片
- `prd-to-issues` — 拆成带依赖、可分别领取的任务
- `design-an-interface` — 3～5 个接口方案比选
- `brainstorming` — 想法展开成方案（数据 / 接口 / 失败恢复）

**实现**
- `tdd` — 红-绿-重构，一次一个可验证的小步
- `react-best-practices` — React / Next.js 工程实践
- `code-search` — ripgrep / ast-grep 快速定位
- `context-optimization` — 压缩上下文、降低 Token 消耗

**质量**
- `qa` — 完整功能质检，重点查边界与回归
- `code-review` — 安全 / 性能 / 错误处理 / 架构四轴审查
- `systematic-debugging` — 复现 → 定位 → 修根因 → 验证
- `issue-triage` — Issue 分诊，明确调查范围与「不查什么」

**仓库与收尾**
- `repo-guardrails` — 提交前钩子、危险命令拦截、依赖体检、工作树隔离
- `refactor-planning` — 坏味道诊断 + 小步重构规划
- `commit-and-changelog` — Conventional Commits + 更新日志

## 典型用法

```
我要做一个新功能，从需求问清楚到测试驱动实现，走一遍完整流水线
把需求问透再写 PRD：一次问一个关键选择，直到没有含糊的地方
我这套重复操作想固化成 Skill，帮我起草、试跑并迭代
给这个仓库装上防线：提交前钩子、危险 Git 命令拦截、依赖体检
```

## 门禁

| 门禁 | 位置 | 规则 |
|---|---|---|
| G1 | 需求 → 规格 | 关键选择还有「不知道」时，不进下一阶段 |
| G2 | 规格 → 实现 | 没有书面规格与验收标准，不写代码 |
| G3 | 实现每步 | 没有通过的测试证据，不进下一步 |
| G4 | 质量 → 合并 | 成员结论未全部回传不进入修复；存在未解决的阻断级发现不放行 |

## 上架信息

- 类型：专家团（`expertType: team`）
- 平台类目：`02-Engineering`
- 打包：`python scripts/package.py teams/skill-forge-crew` → `build/skill-forge-crew.zip`
- 上传页「市场展示分类」务必勾含 AI 创作的类目

## 许可

MIT
