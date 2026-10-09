# Issue 追踪器：本地 Markdown

这个仓库的 issue 和规格说明以 `.scratch/` 里的 markdown 文件形式存在。

## 约定

- 一个功能一个目录：`.scratch/<feature-slug>/`
- 规格说明是 `.scratch/<feature-slug>/spec.md`
- 实施 issue 是每张工单一个文件，位于 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，从 `01` 开始编号，绝不合并成单个工单文件
- 分诊状态记录为每个 issue 文件靠顶部的一行 `Status:`（角色字符串见 `triage-labels.md`）
- 评论和对话历史追加到文件底部、`## Comments` 标题之下

## 当某个技能说「publish to the issue tracker」

在 `.scratch/<feature-slug>/` 下创建一个新文件（需要时创建目录）。

## 当某个技能说「fetch the relevant ticket」

读取被引用路径下的文件。用户通常会直接传路径或 issue 编号。

## 寻路操作（Wayfinding operations）

供 `wayfinder` 技能使用。**地图（map）**是一个文件，每张工单一个**子（child）**文件。

- **地图**：`.scratch/<effort>/map.md`（承载 Notes / Decisions-so-far / Fog 正文）。
- **子工单**：`.scratch/<effort>/issues/NN-<slug>.md`，从 `01` 开始编号，正文里是那个问题。一行 `Type:` 记录工单类型（`research`/`prototype`/`grilling`/`task`）；一行 `Status:` 记录 `claimed`/`resolved`。
- **阻塞**：靠顶部的一行 `Blocked by: NN, NN`。当它列出的每个文件都是 `resolved` 时，工单即解除阻塞。
- **前沿（frontier）**：扫描 `.scratch/<effort>/issues/`，找出未关闭、未阻塞、未被认领的文件；编号最小的获胜。
- **认领**：在任何工作之前设为 `Status: claimed` 并保存。
- **解决**：在一个 `## Answer` 标题下追加答案，设为 `Status: resolved`，再往 `map.md` 里地图的 Decisions-so-far 追加一个上下文指针（gist + 链接）。
