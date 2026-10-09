# 工程评审委员会 · Engineering Review Board

**陆鉴（Lu Jian）· 工程评审总监** — 一个"全仓库代码审查委员会"主理人。先建立仓库地图，再按需调用专项审查镜头（架构、技术债、安全、性能、依赖供应链、测试、可访问性……），全程**默认只读**，每条结论**挂证据**，每次抽样**说明范围**。

## 类型

Agent 型（单个 AI 专家）+ 随包携带 82 个专项技能。

## 功能

### 六步审查流程

1. **建立仓库地图** — 模块、入口点、依赖方向、关键行为、信任边界。地图先于观点。
2. **审查架构与技术债** — 边界是否清晰、依赖方向是否合理、哪些债务开始拖慢变更。
3. **审查代码行为** — 正确性、安全性、可靠性与性能、测试质量四个维度。
4. **按需调用专项技能** — 从 82 个技能里挑当前问题需要的镜头，不一次全上。
5. **用证据支持结论** — 每条结论四段式：问题 → 审查范围 → 已执行检查 → 未验证事项。
6. **保留项目设计选择** — 区分缺陷 / 技术债 / 可接受取舍 / 待验证假设，不用模式纯洁性当判据。

### 三条硬规矩

- **默认只读**：审查阶段不修改任何文件；只有用户明确要求修复才动代码。
- **不许声称"全覆盖"**：抽样必须写明审查范围、样本量、未覆盖部分。
- **结论必须挂证据**：`file:line`、命令输出、搜索结果，或"已搜索 X 未发现 Y"。

### 技能库（82 个）

| 分组 | 技能 |
|---|---|
| 审查镜头 | `architecture-review` `code-review` `security-review` `security-review-evidence` `review-verification-protocol` `adversarial-review` `performance-review` `dependency-supply-chain-review` `release-readiness` `ux-accessibility-review` `prompt-engineering-review` `rust-code-review` |
| 架构与领域 | `clean-architecture` `hexagonal-architecture` `onion-architecture` `domain-driven-design` `domain-modeling` `api-design` |
| 技术债与诊断 | `technical-debt-audit` `systematic-debugging` `root-cause-analysis` `brainstorming` |
| 测试与质量 | `testing-strategy` `test-driven-development` `behavior-driven-development` `gherkin` `playwright-e2e` `php-testing-quality` `rust-testing-quality` `object-pascal-testing-quality` |
| 安全设计 | `threat-modeling` |
| 语言 / 技术栈 | `python-engineering` `javascript-typescript-engineering` `rust-engineering` `php-engineering` `ruby-engineering` `csharp-dotnet-engineering` `powershell-engineering` `object-pascal-engineering` `svelte-sveltekit-engineering` `webassembly-engineering` |
| 模式与反模式 | `python-design-patterns` `python-antipatterns` `php-design-patterns` `php-antipatterns` `rust-design-patterns` `rust-antipatterns` `typescript-javascript-design-patterns` `typescript-javascript-antipatterns` `object-pascal-design-patterns` `object-pascal-antipatterns` |
| 数据与 SQL | `sql-engineering` `postgresql-sql-engineering` `mysql-mariadb-sql-engineering` `sqlite-sql-engineering` `rust-persistence-sql` `data-platform-engineering` `random-data-identifiers` |
| 工程实践 | `documentation-engineering` `git-workflows` `git-commit` `semantic-versioning` `ci-release-engineering` `container-engineering` `observability-engineering` `parallelism-engineering` `script-engineering` `justfiles` `mcp-server-engineering` |
| 前端与样式 | `css-scss-styling` `impeccable` `suggest-lucide-icons` |
| 领域专用 | `internationalization-localization` `zod-engineering` `digital-asset-management` `gossamer-engineering` `piwigo-plugin-engineering` `photo-supreme-scripting` `rust-async-web` `rust-desktop-gui` `hound-web-research` `create-agent-skill` |

> 入口技能 `engineering-review-board` 内含完整路由表（每个技能何时加载）与审查报告模板。

## 使用示例

- 帮我给这个仓库做一次全面审查，看看架构、技术债、安全和测试都有什么问题
- 审查一下这个项目的架构边界和依赖方向，有没有腐化的地方
- 这个代码库能不能放心上线？帮我评估发布就绪度和测试质量

## 适用 / 不适用

**适用**：接手前摸底、上线前体检、技术债盘点、架构评估、安全与测试质量评估、重构前诊断。

**不适用**：单次 diff / 单个 PR 的聚焦评审（用 `code-review`）；实现新功能或修 bug；定位一个明确的活跃故障（用 `systematic-debugging`）。

## 头像

`avatars/engineering-review-board.jpg` — 512×512 px，JPEG。

## 安装

将专家包目录放到专家目录下：

```
/Users/damo/.workbuddy-ai/plugins/marketplaces/my-experts/plugins/engineering-review-board/
```

然后运行注册命令使其可见：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
python3 scripts/package_expert.py <expert-dir> <输出目录>
```

## 来源与许可

本专家包改编自上游仓库 **`nledford/engineering-review-board`**（<https://github.com/nledford/engineering-review-board>），MIT License，Copyright (c) 2026 Nick Ledford。

- `skills/` 下的 82 个技能**原文保留**，未翻译、未简化，仅通过保持 `skills/<name>/` 布局来保留其内部相对链接。
- 本包**新增**的文件：`plugin.json`、`agents/engineering-review-board.md`（主理人人设）、`skills/engineering-review-board/SKILL.md`（全仓库审查入口与路由表）、`README.md`、`avatars/`。
- 上游的仓库维护设施（`AGENTS.md`、`Justfile`、`third-party-skills.json`、技能审计文档、`.gitignore`）未纳入本包。
- 完整许可与归属见 `LICENSE`。
