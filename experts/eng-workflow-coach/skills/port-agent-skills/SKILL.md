---
name: port-agent-skills
display_name: "移植外部技能"
display_name_en: "Port Agent Skills"
description: "把一个外部 agent 技能仓库（Claude Code / Codex / Cursor 等格式的 SKILL.md 集合）批量转换并安装成 WorkBuddy 可用的技能。适用于「把这个仓库的 skill 封装成 workbuddy 能用的」「移植 xxx 的 skills」「转换这批 skill」「把 Claude Code 的 skill 搬过来」这类需求。覆盖侦察、转换规范、并行分发、校验、安装、MIT 归属全流程，并附一份校验脚本与一份可直接复用的转换规范。"
description_zh: "把外部 agent 技能仓库批量转换并安装成 WorkBuddy 可用技能"
description_en: "Port an external agent-skill repository into WorkBuddy skills in bulk."
category: development-tools
version: 1.0.0
author: "大漠"
agent_created: true
---

# 移植外部 agent 技能到 WorkBuddy

<!-- validate: allow-legacy-terms -->
<!-- 本技能正文为了说明差异，会正当地写出 `disable-model-invocation`、`argument-hint`
     等需要被移除的字段名，因此关掉校验脚本对这几个字符串的检查。 -->

把一个为别的 agent harness 写的技能集合，整批转成 WorkBuddy 格式并安装。核心不是翻译，而是**先把差异摸清楚、把规范定死、再并行铺开**。

## 为什么要先侦察，不能直接翻

不同 harness 的技能格式看着都是「frontmatter + markdown」，但**语义差异会造成静默失效**。开工前必须逐条确认，否则转完的技能要么触发不了、要么正文引用一堆不存在的东西。

### 已知的语义差异（已实测）

| 外部约定 | WorkBuddy 的实际情况 | 处置 |
| --- | --- | --- |
| `disable-model-invocation: true` | **支持**。官方上架文档明确列出该字段：置 true 则 AI 不会自动触发、只能由用户手动调用（22 个内置技能都在用） | **原样保留**。别当成"平台不认"而删掉 —— 删了会改变技能的调用语义 |
| `user-invocable: false` | **支持**。false 则隐藏菜单，仅供 AI 内部使用 | 按需保留 |
| `argument-hint` | 无此字段 | 语义（这个技能需要用户提供什么输入）融进 `description` 或正文开头的「输入」小节，**不能丢** |
| `allowed-tools` | **支持**（逗号分隔的工具白名单） | 按需保留；不确定是否合法就去掉 |
| `metadata` / `metadata.credits` | 无此字段 | **署名不能丢**，移到正文末尾的 `## 来源与致谢` 小节 |
| `/slash-command` 调用别的技能 | WorkBuddy 里 `/技能名` 也能触发技能，但正文里应写成「`xxx` 技能」更稳 | 全量替换 |
| `sub-agent` / `spawn a sub-agent` | WorkBuddy 有 Agent 工具 | 写成「子代理（用 Agent 工具）」 |
| `agents/openai.yaml`（Codex 用） | 无对应物 | 直接丢弃，不要产出 |
| `.claude-plugin/`、hooks | Claude Code 专属 | 说明是专属并给等价替代，或丢弃 |
| `AGENTS.md` / `CLAUDE.md` | `AGENTS.md` 同样适用 | 统一写成「`AGENTS.md`（或 `CLAUDE.md`）」 |

> ⚠️ **别凭"这个字段看着像别家的"就删。** 本技能的第一版就犯过这个错：
> 看到 `disable-model-invocation` 是 Claude Code 的字段，想当然认定 WorkBuddy 没有等价物，
> 于是把 16 个技能上这个字段全删了。后来查官方上架文档才发现**它是被支持的**。
> **规矩：拿不准的字段，先去 `https://open.workbuddy.cn/docs/skill` 和 `app.asar` 里查证，
> 或者直接看已上架技能的实际 frontmatter，不要凭印象判断。**

### WorkBuddy 的两套 frontmatter

**本地自用**只要三个字段：

```yaml
---
name: <目录名，kebab-case，不翻译>
description: <中文，做什么 + 何时用 + 触发关键词>
agent_created: true
---
```

**要上架到应用市场**，按官方上架文档补全（必填项加粗）：

```yaml
---
name: <目录名，kebab-case，不翻译>
display_name: <中文展示名>
display_name_en: <英文展示名>
description: <写清用途和触发词 —— 模型据此决定何时加载>   # 必填
description_zh: <简短中文介绍，一行>                      # 必填
description_en: <简短英文介绍，一行>                      # 必填
category: <分类之一>
version: 1.0.0                                          # 必填
author: <合作方名称>                                     # 必填
---
```

- 官方文档：<https://open.workbuddy.cn/docs/skill>
- `category` 的合法取值（从市场真实技能反查）：`development-tools`、`productivity-tools`、
  `content-creation`、`data-analysis`、`business-operations`、`knowledge-learning`、
  `collaboration`、`investment-finance`。**官方文档示例里的 `writing` 不在这个集合内**，别照抄。
- 目录结构：`references/`（文档）、`scripts/`（脚本）、**`templates/`（模板）** ——
  注意是 `templates/` 不是 `assets/`。
- 提交方式：把技能目录打成 zip 上传开放平台。

`description` 是模型选择技能的**唯一依据**，必须写扎实：第三人称、说清做什么、说清什么时候用、并把用户可能说的**中文原话**列进去（如「拷问我」「帮我挑刺」「debug 一下」）。原文那种一句话的 `description`（"A relentless interview to sharpen a plan or design."）在 WorkBuddy 里**触发不了**，必须重写。`description_zh` / `description_en` 则是给市场卡片看的一行简介，两者都要写。

## 流程

### 第一步：侦察

```bash
git clone --depth 1 <repo> /tmp/port-src
find /tmp/port-src -name SKILL.md | sort
find /tmp/port-src -type f ! -name SKILL.md ! -name "openai.yaml" | sort
```

逐项产出：
- **技能清单**：名字、路径、行数
- **frontmatter 字段表**：把每个技能的 frontmatter 抽出来对比，找出非 WorkBuddy 字段
- **附属文件清单**：哪些 `.md`、哪些脚本、哪些是 harness 专属（如 `agents/openai.yaml`）
- **交叉引用图**：哪些技能引用了哪些技能（斜杠形式），转换时要一并改
- **许可证**：读 `LICENSE`，确认是否 MIT/Apache 等需要保留版权声明

⚠️ 仓库的 README 往往有一个「正式对外」的技能子集，另外还有 `in-progress/`、`misc/`、`deprecated/` 等桶。**先跟用户确认封装范围**，不要默认全都要。

### 第二步：定规范 + 写样板

**不要跳过样板这一步。** 先把 `references/CONVERSION-SPEC.md` 按本次的实际情况改一遍（术语对照表、harness 映射表），然后**亲手写 1–2 个样板技能**，覆盖两种形态：

- 一个**薄技能**（正文只有一两句，靠 `description` 承担触发）
- 一个**带附属文件的技能**（展示 `references/` 怎么放、正文链接怎么改）

样板是后面并行分发的「风格锚点」。没有样板就分发，27 个技能会得到 27 种风格。

### 第三步：并行分发

按技能数量切 4–6 批，每批一个子代理（用 Agent 工具），**一条消息里全部发出**。

每个子代理的 prompt 必须自包含，且包含：

1. 必读清单：规范文件路径 + 样板路径（明确要求「不读就动手会做错」）
2. 本批的技能表：技能名 / 源 SKILL.md / 附属文件及其去向
3. 硬性要求清单（frontmatter 三字段、name 等于目录名、description 要中文含触发词、斜杠引用怎么改、附属文件去哪、署名不能丢、不要增删原文步骤、不要软化语气）
4. 本批的**特别提醒**：哪些技能内容长不能漏（如某技能有 6 个阶段、某技能有 12 条清单）、哪些是薄技能不要扩写、哪些附属文件要保持英文

### 第四步：校验（必做，别信子代理的「已完成」）

子代理会回报「自检通过」，**这不等于合格**。跑校验脚本：

```bash
python3 scripts/validate_skill.py /tmp/port-out
```

它查 7 项：frontmatter 字段齐全（`name` / `description` / `agent_created`，市场格式再查 `display_name` / `display_name_en` / `description_zh` / `description_en` / `category` / `version` / `author`）、`name` 等于目录名、`description` 是中文且够长、无残留的 harness 专属字段与安装命令、无残留的 `/技能名` 斜杠引用、无裸 `sub-agent`、相对链接真实存在。

⚠️ 脚本会把「来源与致谢」小节排除在字段检查外 —— 那段文字会正当地提及被移除的字段名（如「删掉了 `argument-hint`」），不排除就会误报。

⚠️ 如果某个技能**本身就在讲怎么转换**、或**在教 harness 的字段机制**，它会通篇正当地提到这些字段名。在这类文件的正文里放一个开关即可关掉该检查：

```markdown
<!-- validate: allow-legacy-terms -->
```

⚠️ 如果根目录里混有第三方 / 市场安装的技能，它们的 frontmatter 形态各不相同，可能被判为硬性问题。**先把待校验的技能收拢到独立目录再跑**。

脚本查不到的东西，**人工抽查**：
- 关键清单的条数对不对（`grep -c` 数一下）
- 脚本类附属文件是否与上游**逐字节一致**（`diff` 一下；翻译脚本会把它弄坏）
- 长技能的分节是否齐全（`grep -nE "^## "` 看标题）
- **frontmatter 能被 YAML 解析器解析**（脚本只做正则检查；装了 pyyaml 就 `yaml.safe_load` 跑一遍）

### 第五步：安装与归属

```bash
cp -R /tmp/port-out/. ~/.workbuddy-ai/skills/
```

装完**必须逐字节比对**，确认拷贝没被截断：

```bash
for d in /tmp/port-out/*/; do diff -r "$d" "$HOME/.workbuddy-ai/skills/$(basename $d)"; done
```

**MIT / Apache 归属**：派生 + 翻译属于「substantial portions」。

⚠️ **每个衍生技能的包里都要各带一份许可全文，不能只在索引技能里放一份。**
MIT 原文是「The above copyright notice and this permission notice shall be included in
**all copies or substantial portions** of the Software」—— 而上架时**每个技能是独立打包上传的**，
只在路由器那个包里放一份，其余 26 个包就成了无许可分发。（这个坑本技能第一版就写错了，
实操到打包那一步才发现：27 个衍生技能里只有 1 个带了许可文件。）

做法：把上游 `LICENSE` 全文复制到**每一个衍生技能**的 `references/UPSTREAM-LICENSE.md`，
前面加一段说明（上游仓库 URL、许可证类型、本次转换改动了什么）。自研技能（不含上游代码）不需要。

另外在索引/路由器技能的正文末尾加 `## 来源与致谢`：原作者、上游 URL、许可证、转换改动清单，
方便日后对照上游更新。如果某个技能自带第三方署名（`metadata.credits`），一并保留。

### 第六步：打包上架（要发布到应用市场时）

**本地装好 ≠ 能上架。** 上架要**每个技能单独打一个 zip**，结构有硬要求。
用官方打包器（自带校验）：

```bash
python3 "/Applications/WorkBuddy AI.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/package_skill.py" \
  ~/.workbuddy-ai/skills/<技能名> <输出目录>
```

**唯一的结构要求：zip 解压后第一层必须就是技能目录本身**（`<技能名>/SKILL.md`），不能多套一层。
自己写打包脚本时对应 `arcname = f.relative_to(skill_dir.parent)`。

⚠️ **打完必须复核，别只信打包器**——多套一层是最高频的上架失败原因：

```python
with zipfile.ZipFile(z) as zf:
    tops = {n.split("/")[0] for n in zf.namelist()}
assert tops == {skill_name}, f"第一层是 {tops}，应为 {{{skill_name}}}"
```

其他注意：

- **上架包的 `author` 要和账号下已上架的其它包统一。** 默认拿本机 `git config user.name` 填是常见错——
  用户的历史包可能用的是另一个署名（艺名/品牌名）。**先问，别猜。**
- 单个技能包平台上限 **3 MB**，超了先查 `references/` 里有没有大图。
- 上架时**头像要单独传一张 512×512 正方形图，包里不带**。批量移植就按技能各出一张，
  用同一套底色渐变 + 图形色（按 `category` 分组），看起来像个同系列图标集，比 28 张风格各异的强。
- 顺手产出 `_manifest.json`（技能名 / 展示名 / 分类 / 包大小 / 是否手动调用）和一份
  **「上架指引.md」**（账号准备 → 产物路径 → 逐项流程 → 建议上架顺序 → 卡点清单 → 许可说明），
  用户照着传就行，不用回来问。
- **和用户已有的上架产物分目录存放**（如 `dist/<本批名>/`），不要和旧批的 zip 混在一起。

#### 想让用户「装一次全有」→ 改打包成专家包

**技能包结构上只能装一个技能**——子目录只认 `references/` / `scripts/` / `templates/`，
没有可嵌套技能的目录。所以 27 个技能 = 27 个上架条目、27 次安装、27 次审核。

但**专家包能一次内置任意多个技能**：它的 `plugin.json` 有 `skills` 字段（技能目录路径列表）。
本机 16 个已装专家都这么做（`xiaohongshu-ops` 带 7 个、`meme-pack-studio` 带 6 个）。

结构：

```text
<expert-name>/
├── .codebuddy-plugin/plugin.json
├── avatars/<expert-name>.png        512×512，≤500KB
├── agents/<expert-name>.md          人设；frontmatter 的 skills 列全部技能名
├── skills/<每个技能>/
└── README.md
```

⚠️ **内置技能必须剥掉 `disable-model-invocation`**，否则 agent 无法自动路由到它们。
实证：本机已上架的多技能专家（`xiaohongshu-ops`、`meme-pack-studio`）**无一使用该字段**。
独立技能包则原样保留（那是上游原始设计）。

⚠️ **代价必须跟用户讲清楚，让他自己选**：专家内置的技能**不进全局技能列表**。
实测本机专家包内置 92 个 `SKILL.md`，全局技能列表里**一个都没有**；
而插件内置的 21 个全在。也就是说内置技能只在**召唤该专家后**的会话里生效，
不能像独立技能那样在任何对话中被 AI 自动触发。

`plugin.json` 硬约束（官方 `/docs/expert`）：

- `displayDescription.zh` 必须 **40–50 字**（会拒）
- `tags` 恰好 **3 个**；`quickPrompts` 恰好 **3 个**，且 `defaultInitPrompt` 必须等于第一条
- `name` / `plugin` / `agentName` / agent 文件名 **四处一致**，且 `name` 全平台全局唯一
- `expertType: "agent"`，`categoryId` 取官方 15 个枚举之一（工程类填 `02-Engineering`）
- 专家包上限 **20 MB**（技能包是 3 MB）

## 坑

- **`ls -1d <dir>/*/ | wc -l` 在这个沙箱里会给出错的计数**（实测 45 个目录数成 34 个）。数目录一律用 `find <dir> -maxdepth 1 -mindepth 1 -type d | wc -l`。
- **`cp -R` 在这个沙箱里行为不稳定，别信它的返回码**。有时报 `Broker request timed out`
  但**其实已经拷完**；有时报 broker 错误**且真的没拷**（2026-10-01 实测：拷一个专家目录时
  报错、目标目录根本没被创建）。**拷完一律用 `find` 点一下文件数再往下走**；
  要稳就直接用 Python `shutil.copytree`（本次改用后一次成功）。
- **zsh 下 `rm -rf /tmp/x/*` 在目录为空时会 `no matches found` 并中断整条 `&&` 链**，后续命令静默不执行。改用 `rm -rf /tmp/x; mkdir -p /tmp/x`。
- **内容检索用 Grep 工具，不要用 Bash 的 `grep`**（本沙箱的 bash `grep` 对明明存在的字符串也会返回空）。数条数时 `grep -c` 的 `||` 回退链要小心，可能拿到两行输出。
- 原文的 `<spec-template>` 这类模板块要保留；里面**字段名/占位符保持英文**，描述性文字才译中文。
- 原文语气是资产。「Refuse to give up」「Do NOT proceed」要译成同等强度的中文（「不许放弃」「未完成不得进入下一阶段」），不要软化成「建议」。
- 有个别技能（如讲「怎么给 agent 写文档」的）**正文里就在教 harness 的 frontmatter 机制**，这种内容要按 WorkBuddy 的规范**改写**而不是直译，否则会教出错的用法。

## 参考

- 转换规范模板：[references/CONVERSION-SPEC.md](references/CONVERSION-SPEC.md) —— 含术语中英对照表与 harness 映射表，改一改就能用
- 校验脚本：[scripts/validate_skill.py](scripts/validate_skill.py) —— 用法 `python3 validate_skill.py <skills-root>`
