# 12 · 集成与命令调用语法

**用途**：当用户问"这套东西支持我的编辑器/代理吗""命令怎么敲"时查这张表。

## 与 WorkBuddy 的关系

**在 WorkBuddy 里你不需要关心这些。** WorkBuddy 本身就是执行器 —— 用户说人话，你编排。这一节存在是为了：

1. 用户从 Spec Kit 那边迁移过来，习惯用 `/speckit-*` 语汇 → 你能听懂并翻译
2. 用户想把产物同步给团队里的其他编码代理（比如同事用 Cursor、Claude Code）→ 你能告诉他各家怎么调用
3. 用户问"支持多少个代理"→ 你能给出准确数字

## 命令调用语法的四个体系

原版 Spec Kit 的斜杠命令在不同代理里语法不同：

| 语法 | 适用代理 |
|---|---|
| `/speckit-<command>`（斜杠 + 连字符） | GitHub Copilot（默认 skills 模式）、Alquimia、Antigravity、Devin、Factory Droid、Grok Build、MiniMax Code、Muse Code、Zed、DeepSeek Harness |
| `$speckit-<command>`（美元符号） | Codex CLI、Command Code、ZCode |
| `/skill:speckit-<command>` | Kimi Code |
| `/speckit.<command>`（点号） | 文档参考记法，非某个代理的实机语法 |

对照示例：

| 代理 / 模式 | SDD 示例 | 扩展示例 |
|---|---|---|
| GitHub Copilot（默认 skills） | `/speckit-specify` | `/speckit-bug-assess` |
| 文档点号记法 | `/speckit.specify` | `/speckit.bug.assess` |
| Codex / Command Code / ZCode | `$speckit-specify` | `$speckit-bug-assess` |
| Kimi Code | `/skill:speckit-specify` | `/skill:speckit-bug-assess` |

> ⚠️ **这些是 agent skills，不是终端命令。** 要在代理的对话里调用，不是在 shell 里敲。

## 支持规模

**共 44 个集成**（43 个具体编码代理 + 1 个 `generic` 通用兜底）。其中明确标注为 **skills 模式**的约 18 个；声明为**多装安全**（multi-install safe，即多个代理可共用同一个项目而不冲突）的 **26 个**。

用户常提到的那几个：

| 代理 | 集成键 | 安装目录 | 调用语法 |
|---|---|---|---|
| Claude Code | `claude` | `.claude/skills` | `/speckit-<cmd>` |
| GitHub Copilot | `copilot` | `.github/skills`（默认） | `/speckit-<cmd>` |
| Codex CLI | `codex` | `.agents/skills` | `$speckit-<cmd>` |
| Gemini CLI | `gemini` | `.gemini/commands` | 命令式（未标注 skills） |
| Cursor | `cursor-agent` | `.cursor/skills` | 未明确标注 |
| CodeBuddy CLI | `codebuddy` | `.codebuddy/commands` | 未明确标注 |
| Kimi Code | `kimi` | `.kimi-code/skills` | `/skill:speckit-<cmd>` |
| Zed | `zed` | `.agents/skills` | `/speckit-<cmd>` |
| opencode | `opencode` | `.opencode/commands` | 未明确标注 |
| Qwen Code | `qwen` | `.qwen/commands` | 未明确标注 |

其余键名（按字母序）：`agy`、`alquimia`、`amp`、`auggie`、`bob`、`cline`、`command-code`、`devin`、`docker-agent`、`droid`、`dsh`、`firebender`、`forge`、`goose`、`grok`、`hermes`、`junie`、`kilocode`、`kiro-cli`、`lingma`、`mcode`、`muse`、`omp`、`pi`、`qodercli`、`rovodev`、`shai`、`tabnine`、`trae`、`vibe`、`zcode`、`generic`。

## 通用兜底

自带代理（自研 agent）时用 `generic`：

```bash
specify init my-project --integration generic --integration-options="--commands-dir <path>"
```

## 安装（原版 CLI，供参考）

```bash
uv tool install specify-cli
specify init my-project --integration copilot
cd my-project
```

需要 Python 3.11+ 与 `uv`，支持 Linux / macOS / Windows。

- 已有代码库：参考 existing-projects 指南
- 升级已有安装：参考 Upgrade 文档
- 扩展安装：`specify extension add bug` / `specify extension add assess` / `specify extension add github`

## 定制机制

| 机制 | 作用 |
|---|---|
| **Extensions** | 增加能力（如 `bug`、`assess`、`github`） |
| **Presets** | 调整既有行为 |
| **Workflows** | 把多个步骤自动化 |
| **Bundles** | 打包一套基于角色的配置 |
| **项目内覆盖** | 一次性改模板 |

> 上游项目：https://github.com/github/spec-kit （MIT License）
