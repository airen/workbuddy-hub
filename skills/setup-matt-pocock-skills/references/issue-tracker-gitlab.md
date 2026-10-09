# Issue 追踪器：GitLab

这个仓库的 issue 和规格说明以 GitLab issue 的形式存在。所有操作都用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 约定

- **创建 issue**：`glab issue create --title "..." --description "..."`。多行描述用 heredoc。传 `--description -` 打开编辑器。
- **读取 issue**：`glab issue view <number> --comments`。用 `-F json` 得到机器可读输出。
- **列出 issue**：`glab issue list -F json`，配上合适的 `--label` 过滤。
- **评论 issue**：`glab issue note <number> --message "..."`。GitLab 把评论叫「note」。
- **加 / 移除标签**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多个标签可以用逗号分隔，或重复这个旗标。
- **关闭**：`glab issue close <number>`。`glab issue close` 不接受关闭评论，所以先用 `glab issue note <number> --message "..."` 发出说明，再关闭。
- **合并请求（merge request）**：GitLab 把 PR 叫「merge request」。用 `glab mr create`、`glab mr view`、`glab mr note` 等，形状跟 `gh pr ...` 一样，只是用 `mr` 替换 `pr`、用 `note`/`--message` 替换 `comment`/`--body`。

从 `git remote -v` 推断仓库；在 clone 里运行时 `glab` 会自动这么做。

## 把 MR 当作分诊面

**把 MR 当作请求面：否。** _（如果这个仓库把外部合并请求当作功能请求，就设成 `yes`；`triage` 技能会读这个开关。）_

设成 `yes` 时，MR 走跟 issue 相同的标签和状态，用对应的 `glab mr`：

- **读取 MR**：`glab mr view <number> --comments`，以及用 `glab mr diff <number>` 拿 diff。
- **列出待分诊的外部 MR**：`glab mr list -F json`，然后只保留作者不是项目成员/所有者的 MR（贡献者的 MR，而不是维护者正在进行的活）。
- **评论 / 打标签 / 关闭**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

跟 GitHub 不同，GitLab 给 issue 和 MR 分开编号，所以一旦你知道维护者指的是哪个面，`#42` 就是无歧义的。

## 当某个技能说「publish to the issue tracker」

创建一个 GitLab issue。

## 当某个技能说「fetch the relevant ticket」

运行 `glab issue view <number> --comments`。

## 寻路操作（Wayfinding operations）

供 `wayfinder` 技能使用。**地图（map）**是一个单独的 issue，**子（child）**issue 是工单。

- **地图**：一个带 `wayfinder:map` 标签的 issue，承载 Notes / Decisions-so-far / Fog 正文。`glab issue create --label wayfinder:map`。（在有原生 epic 的 GitLab 套餐上，可以用一个 epic 承载地图；带标签的 issue 在任何地方都管用。）
- **子工单**：一个描述顶部带 `Part of #<map>`、标签为 `wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）的 issue。一旦被认领，工单就指派给驱动它的开发者。
- **阻塞**：GitLab 的**原生阻塞链接（native blocking link）**，这是规范且 UI 可见的表示。用 `/blocked_by #<n>` 快捷操作添加，以一条 note 的形式发出（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生阻塞链接是 Premium/Ultimate 功能；在免费套餐（或不可用的地方）上，回退到描述顶部的一行 `Blocked by: #<n>, #<n>`。当每个阻塞者都关闭时，工单即解除阻塞。
- **前沿查询**：`glab issue list -F json`，范围限定在地图的子项，丢掉任何有未关闭阻塞者的：指向某个未关闭 issue 的原生 `blocked_by` 链接（`glab api projects/:id/issues/:iid/links`），或 `Blocked by` 行里有一个未关闭 issue，或有指派人；地图顺序里第一个获胜。
- **认领**：`glab issue update <n> --assignee @me`，这是会话的第一次写入。
- **解决**：`glab issue note <n> --message "<answer>"`，然后 `glab issue close <n>`，再往地图的 Decisions-so-far 追加一个上下文指针（gist + 链接）。
