# Issue 追踪器：GitHub

这个仓库的 issue 和规格说明以 GitHub issue 的形式存在。所有操作都用 `gh` CLI。

## 约定

- **创建 issue**：`gh issue create --title "..." --body "..."`。多行正文用 heredoc。
- **读取 issue**：`gh issue view <number> --comments`，用 `jq` 过滤评论，同时取回标签。
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，配上合适的 `--label` 和 `--state` 过滤。
- **评论 issue**：`gh issue comment <number> --body "..."`
- **加 / 移除标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **关闭**：`gh issue close <number> --comment "..."`

从 `git remote -v` 推断仓库；在 clone 里运行时 `gh` 会自动这么做。

## 把 PR 当作分诊面

**把 PR 当作请求面：否。** _（如果这个仓库把外部 PR 当作功能请求，就设成 `yes`；`triage` 技能会读这个开关。）_

设成 `yes` 时，PR 走跟 issue 相同的标签和状态，用对应的 `gh pr`：

- **读取 PR**：`gh pr view <number> --comments`，以及用 `gh pr diff <number>` 拿 diff。
- **列出待分诊的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，然后只保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的（丢掉 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **评论 / 打标签 / 关闭**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 的 issue 和 PR 共用一个编号空间，所以一个裸的 `#42` 可能是两者之一：先用 `gh pr view 42` 解析，再回退到 `gh issue view 42`。

## 当某个技能说「publish to the issue tracker」

创建一个 GitHub issue。

## 当某个技能说「fetch the relevant ticket」

运行 `gh issue view <number> --comments`。

## 寻路操作（Wayfinding operations）

供 `wayfinder` 技能使用。**地图（map）**是一个单独的 issue，**子（child）**issue 是工单。

- **地图**：一个带 `wayfinder:map` 标签的 issue，承载 Notes / Decisions-so-far / Fog 正文。`gh issue create --label wayfinder:map`。
- **子工单**：一个作为 GitHub sub-issue 链接到地图的 issue（对 sub-issues 端点用 `gh api`）。在 sub-issues 未启用的地方，把子项加进地图正文的任务列表，并在子项正文顶部放 `Part of #<map>`。标签：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。一旦被认领，工单就指派给驱动它的开发者。
- **阻塞**：GitHub 的**原生 issue 依赖（native issue dependencies）**，这是规范且 UI 可见的表示。用 `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 添加一条边，其中 `<blocker-db-id>` 是阻塞者的数字**数据库 id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，*不是* `#number` 或 `node_id`）。GitHub 会报告 `issue_dependencies_summary.blocked_by`（只含未关闭的阻塞者，即活的闸门）。在依赖不可用的地方，回退到子项正文顶部的一行 `Blocked by: #<n>, #<n>`。当每个阻塞者都关闭时，工单即解除阻塞。
- **前沿查询（frontier query）**：列出地图下未关闭的子项（`gh issue list --state open`，范围限定在地图的 sub-issues / 任务列表），丢掉任何有未关闭阻塞者（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行里有一个未关闭 issue）或有指派人的；地图顺序里第一个获胜。
- **认领**：`gh issue edit <n> --add-assignee @me`，这是会话的第一次写入。
- **解决**：`gh issue comment <n> --body "<answer>"`，然后 `gh issue close <n>`，再往地图的 Decisions-so-far 追加一个上下文指针（gist + 链接）。
