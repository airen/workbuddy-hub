# 撰写 Agent 简报

agent 简报（agent brief）是当一个 issue 或 PR 移到 `ready-for-agent` 时，贴在它上面的一条结构化评论。它是 AFK agent 将据以工作的权威规格。原始正文和讨论是上下文：agent 简报才是契约。

简报陈述**agent 应该做什么**，这一点在两个面上都成立：对一个 issue，就是从零构建这个改动；对一个 PR，就是_对现有 diff_ 还剩什么要做：把它做完、补上缺口、回应评审意见。两边原则相同；下面的 PR 示例展示了差异。

## 原则

### 耐久优先于精确

这个 issue 可能在 `ready-for-agent` 停留几天甚至几周。这期间代码库会变化。把简报写得即便文件被重命名、移动或重构后依然有用。

- **要**描述接口、类型和行为契约
- **要**点名 agent 应当寻找或修改的具体类型、函数签名或配置形状
- **不要**引用文件路径：它们会过期
- **不要**引用行号
- **不要**假定当前的实现结构会保持不变

### 行为式，而非流程式

描述系统应该**做什么**，而不是**怎么**实现它。agent 会重新探索代码库并做出自己的实现决策。

- **好：**「`SkillConfig` 类型应当接受一个类型为 `CronExpression` 的可选 `schedule` 字段」
- **坏：**「打开 src/types/skill.ts 并在第 42 行加一个 schedule 字段」
- **好：**「当用户不带参数运行 `triage` 技能时，他们应当看到一份需要注意的 issue 摘要」
- **坏：**「在主处理函数里加一个 switch 语句」

### 完整的验收标准

agent 需要知道什么时候算做完。每份 agent 简报都必须有具体、可测试的验收标准。每条标准都应能被独立核验。

- **好：**「运行 `gh issue list --label needs-triage` 返回已经过初步分类的 issue」
- **坏：**「triage 应该能正确工作」

### 明确的范围边界

说明什么超出范围。这能防止 agent 镀金，或对相邻功能做假设。

## 模板

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** 需要发生什么的一行描述

**Current behavior:**
描述现在会发生什么。对 bug 而言，这就是坏掉的行为。
对 enhancement 而言，这就是该功能所基于的现状。

**Desired behavior:**
描述 agent 的工作完成之后应当发生什么。
把边界情况和错误条件说具体。

**Key interfaces:**
- `TypeName`：需要改什么以及为什么
- `functionName()` 返回类型：它当前返回什么、应该返回什么
- 配置形状：需要的任何新配置项

**Acceptance criteria:**
- [ ] 具体、可测试的标准 1
- [ ] 具体、可测试的标准 2
- [ ] 具体、可测试的标准 3

**Out of scope:**
- 在这个 issue 里不该被改动或处理的东西
- 看起来相关、但其实是另一件事的相邻功能
```

## 示例

### 好的 agent 简报（bug）

```markdown
## Agent Brief

**Category:** bug
**Summary:** 技能描述的截断会从词中间切断，产出损坏的输出

**Current behavior:**
当一个技能描述超过 1024 个字符时，它会被精确截断在 1024 个字符处，
无视词边界。这会产出从词中间结束的描述（例如 "Use when the user wants to confi"）。

**Desired behavior:**
截断应当在 1024 个字符之前的最后一个词边界处断开，
并追加 "..." 来表示发生了截断。

**Key interfaces:**
- `SkillMetadata` 类型的 `description` 字段：类型无需改动，
  但填充它的校验/处理逻辑需要尊重词边界
- 任何读取 SKILL.md frontmatter 并提取 description 的函数

**Acceptance criteria:**
- [ ] 1024 字符以内的描述保持不变
- [ ] 超过 1024 字符的描述在 1024 字符之前的最后一个词边界处截断
- [ ] 被截断的描述以 "..." 结尾
- [ ] 含 "..." 的总长度不超过 1024 字符

**Out of scope:**
- 改动 1024 字符这个上限本身
- 多行描述支持
```

### 好的 agent 简报（enhancement）

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** 增加 `.out-of-scope/` 目录支持，用来追踪被拒绝的功能请求

**Current behavior:**
当一个功能请求被拒绝时，这个 issue 会带 `wontfix` 标签和一条评论关闭。
对这个决策或理由没有任何持久记录。未来类似的请求需要维护者
回忆或搜索先前的讨论。

**Desired behavior:**
被拒绝的功能请求应当被记录在 `.out-of-scope/<concept>.md` 文件里，
捕获决策、理由，以及所有请求过该功能的 issue 的链接。
在 triage 新 issue 时，应当检查这些文件是否有匹配。

**Key interfaces:**
- `.out-of-scope/` 里的 markdown 文件格式：每个文件应有一个
  `# Concept Name` 标题、一行 `**Decision:**`、一行 `**Reason:**`，
  以及一个带 issue 链接的 `**Prior requests:**` 列表
- triage 工作流应当尽早读取所有 `.out-of-scope/*.md` 文件，
  并按概念相似度把进来的 issue 与它们匹配

**Acceptance criteria:**
- [ ] 把某个功能作为 wontfix 关闭时，在 `.out-of-scope/` 里创建/更新一个文件
- [ ] 该文件包含决策、理由，以及指向被关闭 issue 的链接
- [ ] 如果已存在匹配的 `.out-of-scope/` 文件，新 issue 会被追加到它的
      "Prior requests" 列表，而不是创建一份重复
- [ ] triage 期间会检查现有的 `.out-of-scope/` 文件，并在新 issue
      匹配到一次先前拒绝时把它挑出来

**Out of scope:**
- 自动匹配（由人类确认匹配）
- 重新打开先前被拒绝的功能
- bug 报告（只有被拒绝的 enhancement 才进 `.out-of-scope/`）
```

### 好的 agent 简报（PR）

对一个 PR，「Current behavior」描述的是 diff 的状态，简报要求 agent 把它做完或修好，而不是从零构建。

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** 完成贡献者为 `triage list` 加的 `--json` 输出标志

**Current behavior:**
这个 PR 加了一个 `--json` 标志，把 issue 列表序列化成 JSON。happy path
能工作，diff 也符合项目的命令结构。还差两处：错误仍然以人类可读文本
打印（不是 JSON），而且新标志没有测试覆盖。

**Desired behavior:**
带 `--json` 时，所有输出（包括错误）都是 stdout 上格式良好的 JSON，
且命令的退出码保持不变。标志缺席时，现有的人类可读输出不受影响。

**Key interfaces:**
- 命令的错误路径在 `--json` 下应发出 `{ "error": string }`，
  而不是纯文本错误
- 复用这个 PR 已经加的那个序列化器；不要引入第二个

**Acceptance criteria:**
- [ ] `triage list --json` 对成功和错误两种情况都发出合法 JSON
- [ ] 退出码与非 JSON 命令一致
- [ ] 有一个测试覆盖 `--json` 的成功输出和一个错误情况
- [ ] 默认（非 JSON）输出逐字节不变

**Out of scope:**
- 给任何其他命令加 `--json`
- 改动这个 PR 已经定义的、成功载荷的 JSON 形状
```

### 坏的 agent 简报

```markdown
## Agent Brief

**Summary:** 修一下 triage 的 bug

**What to do:**
triage 那东西坏了。看看主文件然后修一下。
大概第 150 行那个函数有问题。

**Files to change:**
- src/triage/handler.ts (line 150)
- src/types.ts (line 42)
```

这是坏的，因为：

- 没有 category
- 描述含糊（「triage 那东西坏了」）
- 引用了会过期的文件路径和行号
- 没有验收标准
- 没有范围边界
- 没有描述当前行为与期望行为
