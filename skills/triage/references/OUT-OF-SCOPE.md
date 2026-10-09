# 超出范围知识库（Out-of-Scope Knowledge Base）

仓库里的 `.out-of-scope/` 目录存放被拒绝的功能请求的持久记录。它有两个用途：

1. **机构记忆（Institutional memory）**：为什么某个功能被拒绝，这样在 issue 关闭后理由不会丢失
2. **去重（Deduplication）**：当一个新 issue 进来、且匹配到一次先前的拒绝时，本技能可以把先前的决策挑出来，而不是重新争论一遍

## 目录结构

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

每个**概念（concept）**一个文件，不是每个 issue 一个。请求同一件事的多个 issue 被归到一个文件下。

## 文件格式

文件应当用一种放松、可读的风格来写，更像一份简短的设计文档，而不是一条数据库记录。用段落、代码示例和例子，把理由讲清楚，让第一次遇到它的人也能用得上。

```markdown
# Dark Mode

这个项目不支持暗色模式，也不支持面向用户的主题化。

## Why this is out of scope

渲染管线假定有一套定义在 `ThemeConfig` 里的单一调色板。
支持多套主题将需要：

- 一个包裹整个组件树的主题上下文 provider
- 逐组件的、感知主题的样式解析
- 一个用于用户主题偏好的持久化层

这是一处重大的架构改动，与本项目专注于内容创作的定位不符。
主题化是下游消费者（嵌入或再分发输出的人）的关切。

```ts
// 当前的 ThemeConfig 接口不是为运行时切换设计的：
interface ThemeConfig {
  colors: ColorPalette; // 单一调色板，在构建时解析
  fonts: FontStack;
}
```

## Prior requests

- #42: "Add dark mode support"
- #87: "Night theme for accessibility"
- #134: "Dark theme option"
```

### 给文件命名

用简短、有描述性的 kebab-case 名字来命名这个概念：`dark-mode.md`、`plugin-system.md`、`graphql-api.md`。这个名字应当足够可辨认，让人浏览目录时不打开文件就知道被拒绝的是什么。

### 写理由

理由应当是有实质内容的：不是「我们不想要这个」，而是为什么。好的理由会引用：

- 项目范围或理念（「本项目专注于 X；主题化是下游的关切」）
- 技术约束（「支持这个需要 Y，而 Y 与我们的 Z 架构冲突」）
- 战略决策（「我们选择用 A 而不是 B，因为……」）

理由应当是耐久的。避免引用临时情况（「我们眼下太忙了」）；那不是真正的拒绝，只是延期。

## 什么时候检查 `.out-of-scope/`

在 triage 期间（第 1 步：收集上下文），读取 `.out-of-scope/` 里的所有文件。评估一个新 issue 时：

- 检查这个请求是否匹配某个已有的超出范围概念
- 匹配靠概念相似度，不靠关键词：「night theme」匹配 `dark-mode.md`
- 如果匹配上了，把它挑给维护者看：「这与 `.out-of-scope/dark-mode.md` 相似。我们之前拒绝过它，理由是 [理由]。你现在还是这么看吗？」

维护者可以：

- **确认（Confirm）**：新 issue 被加到已有文件的 "Prior requests" 列表，然后关闭
- **重新考虑（Reconsider）**：超出范围文件被删除或更新，这个 issue 继续走正常的 triage
- **不同意（Disagree）**：这些 issue 相关但不同，继续走正常的 triage

## 什么时候写入 `.out-of-scope/`

只有当某个 **enhancement**（不是 bug）被作为 `wontfix` *拒绝*时。这同样适用于 enhancement PR，与 issue 完全一样：被拒绝的 PR 会被记录在这里，免得同一个请求又作为新代码回来。

**不要**在某样东西因为**已经实现**而被作为 `wontfix` 关闭时写在这里。那是已建成的功能，不是被拒绝的；记录它会用假拒绝污染去重检查。相反，关闭评论应指出该功能已经在哪里。

流程：

1. 维护者判定某个功能请求超出范围
2. 检查是否已存在匹配的 `.out-of-scope/` 文件
3. 如果有：把新 issue 追加到 "Prior requests" 列表
4. 如果没有：用概念名、决策、理由和第一条先前请求创建一个新文件
5. 在 issue 上发一条评论，解释这个决策并提到那个 `.out-of-scope/` 文件
6. 带 `wontfix` 标签关闭这个 issue

## 更新或移除超出范围文件

如果维护者对一个先前被拒绝的概念改变了主意：

- 删除那个 `.out-of-scope/` 文件
- 本技能不需要重新打开旧 issue；它们是历史记录
- 触发这次重新考虑的新 issue 继续走正常的 triage
