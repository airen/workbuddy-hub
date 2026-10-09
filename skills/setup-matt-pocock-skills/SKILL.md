---
name: setup-matt-pocock-skills
display_name: "工程技能初始化"
display_name_en: "Setup Engineering Skills"
description: "该技能用于把当前仓库配置成其他工程技能所假定的样子：设置 issue 追踪器、分诊标签词汇和领域文档布局，每个仓库在首次使用其他工程技能之前跑一次。适用于「初始化」「配置仓库」「跑一遍 setup」「setup 一下」「配置 issue 追踪器」「这些工程技能怎么用起来」这类需求。"
description_zh: "配置仓库的 issue 追踪器、分诊标签与文档布局，每个仓库跑一次"
description_en: "Configure the repo for the engineering skills: issue tracker, triage labels, doc layout."
category: development-tools
version: 1.0.0
author: "大漠"
disable-model-invocation: true
agent_created: true
---

# 配置 Matt Pocock 的技能（Setup Matt Pocock's Skills）

搭好工程技能所假定的、每个仓库一份的配置：

- **Issue 追踪器（issue tracker）**：issue 住在哪里（默认 GitHub；本地 markdown 也开箱支持）
- **分诊标签（triage labels）**：用于五个标准分诊角色的字符串
- **领域文档（domain docs）**：`GLOSSARY.md` 和 ADR 住在哪里，以及读取它们的消费规则

这是一个提示驱动的技能，不是确定性脚本。先探索，把发现摆出来，跟用户确认，然后再写。

## 流程

### 1. 探索

看一下当前仓库，理解它的起始状态。读到什么算什么；不要臆测：

- `git remote -v` 和 `.git/config`：这是不是一个 GitHub 仓库？是哪一个？
- 仓库根目录的 `AGENTS.md` 和 `CLAUDE.md`：两者之一存在吗？里面是否已有 `## Agent skills` 小节？
- 仓库根目录的 `GLOSSARY.md` 和 `GLOSSARY-MAP.md`
- `docs/adr/` 以及任何 `src/*/docs/adr/` 目录
- `docs/agents/`：本技能此前的产出是否已经存在？
- `.scratch/`：这是「本地 markdown issue 追踪器」约定已在使用的迹象
- `triage` 技能是否已安装？（跟本技能并排的一个 `triage` 技能目录，或者你的可用技能里有 `triage`。）这决定 B 节到底跑不跑。
- Monorepo 信号：`pnpm-workspace.yaml`、`package.json` 里的 `workspaces` 字段，或者一个装了东西、自带 `src/` 的 `packages/*`。这些只存在于真正大型的多包仓库；它们缺席就意味着单上下文（single-context），而那几乎是每一个仓库。

### 2. 呈现发现并提问

总结什么在、什么缺。然后按顺序过这几节。一节，一个答复，然后下一节。

每一节都先给出推荐答案，这样用户一个字就能接受它。只有当选择确实会分叉时，才给一句解释；如果探索已经定论，就整节跳过（`triage` 未安装时跳过 B 节，没有 monorepo 时跳过 C 节）。

**A 节：Issue 追踪器。**

> 解释：「issue 追踪器」是这个仓库里 issue 住的地方。`to-tickets`、`triage`、`to-spec` 这类技能都从它读、往它写。它们需要知道该调用 `gh issue create`、在 `.scratch/` 下写一个 markdown 文件，还是走你描述的某种别的流程。挑你实际用来追踪这个仓库工作的地方。

默认姿态：这些技能是为 GitHub 设计的。如果某个 `git remote` 指向 GitHub，就提议它。如果某个 `git remote` 指向 GitLab（`gitlab.com` 或自建主机），就提议 GitLab。否则（或者用户更偏好时），提供：

- **GitHub**：issue 住在仓库的 GitHub Issues 里（使用 `gh` CLI）
- **GitLab**：issue 住在仓库的 GitLab Issues 里（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本地 markdown**：issue 作为文件住在这个仓库的 `.scratch/<feature>/` 下（适合单人项目或没有 remote 的仓库）
- **其他**（Jira、Linear 等）：请用户用一段话描述工作流；技能会把它记成自由文本

把选择记到 `docs/agents/issue-tracker.md`。GitHub 和 GitLab 模板带一个「把 PR 当作请求面」的开关，默认**关**。让它保持关着，也不要去提它：想要把外部 PR 纳入分诊队列的用户，之后可以自己在文件里翻这个开关。

**B 节：分诊标签词汇。** 如果 `triage` 技能未安装（探索已经告诉你），整节跳过，因为未安装的技能不需要任何标签。

如果它已安装，就只问一个问题：

> 你想保留默认的分诊标签吗？（推荐：**是**）

默认值就是五个标准角色，每个标签字符串都等于它的名字：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。**是**就原样写入。只有当用户说不（通常是因为他们的追踪器已经在用别的名字，比如用 `bug:triage` 对应 `needs-triage`）时，才收集这些覆盖，好让 `triage` 去套用已有标签、而不是创建重复的。

**C 节：领域文档。** 默认**单上下文（single-context）**（仓库根一份 `GLOSSARY.md` + `docs/adr/`）。它适合几乎每一个仓库；直接写，不用问。

只有当探索发现 monorepo 信号时，才提供**多上下文（multi-context）**（根部的 `GLOSSARY-MAP.md` 指向每个上下文各自的 `GLOSSARY.md`）。然后确认他们想要哪种布局。

### 3. 确认并编辑

给用户看一份草稿：

- 要加到 `CLAUDE.md` / `AGENTS.md` 中正在被编辑的那个里的 `## Agent skills` 块（选择规则见第 4 步）
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 和 `docs/agents/triage-labels.md` 的内容（最后一个只在 `triage` 已安装时）

让他们在写入前先编辑。

### 4. 写入

**挑选要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则如果 `AGENTS.md` 存在，编辑它。
- 如果两者都不存在，问用户要创建哪一个；不要替他们选。

当 `CLAUDE.md` 已存在时，绝不创建 `AGENTS.md`（反之亦然）；永远编辑已经在那里的那个。

如果选中的文件里已经有 `## Agent skills` 块，就地更新它的内容，而不是再追加一份重复的。不要覆盖用户对周围小节的编辑。

那个块：

```markdown
## Agent skills

### Issue tracker

[issue 追踪在哪里的单行摘要]。见 `docs/agents/issue-tracker.md`。

### Triage labels

[标签词汇的单行摘要]。见 `docs/agents/triage-labels.md`。

### Domain docs

[布局的单行摘要：「single-context」或「multi-context」]。见 `docs/agents/domain.md`。
```

只有当 `triage` 已安装且 B 节跑过时，才包含 `### Triage labels` 子块、并写 `docs/agents/triage-labels.md`。否则两者都省略。

然后用本技能目录里的种子模板作为起点，写这些文档文件：

- [issue-tracker-github.md](references/issue-tracker-github.md)：GitHub issue 追踪器
- [issue-tracker-gitlab.md](references/issue-tracker-gitlab.md)：GitLab issue 追踪器
- [issue-tracker-local.md](references/issue-tracker-local.md)：本地 markdown issue 追踪器
- [triage-labels.md](references/triage-labels.md)：标签映射（只在 `triage` 已安装时）
- [domain.md](references/domain.md)：领域文档的消费规则 + 布局

对于「其他」issue 追踪器，用用户的描述从零写 `docs/agents/issue-tracker.md`。

### 5. 完成

告诉用户配置已完成，以及哪些工程技能此后会从这些文件读取。提一句他们之后可以直接编辑 `docs/agents/*.md`；只有当他们想切换 issue 追踪器或从零重来，才有必要重跑本技能。
