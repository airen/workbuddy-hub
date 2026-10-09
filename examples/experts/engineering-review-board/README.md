# engineering-review-board 使用示例

**类别**：开发与工程 | **版本**：1.0.0
**编排技能**：adversarial-review, api-design, architecture-review, behavior-driven-development, brainstorming, ci-release-engineering, clean-architecture, code-review, container-engineering, create-agent-skill, csharp-dotnet-engineering, css-scss-styling, data-platform-engineering, dependency-supply-chain-review, digital-asset-management, documentation-engineering, domain-driven-design, domain-modeling, engineering-review-board, gherkin, git-commit, git-workflows, gossamer-engineering, hexagonal-architecture, hound-web-research, impeccable, internationalization-localization, javascript-typescript-engineering, justfiles, mcp-server-engineering, mysql-mariadb-sql-engineering, object-pascal-antipatterns, object-pascal-design-patterns, object-pascal-engineering, object-pascal-testing-quality, observability-engineering, onion-architecture, parallelism-engineering, performance-review, photo-supreme-scripting, php-antipatterns, php-design-patterns, php-engineering, php-testing-quality, piwigo-plugin-engineering, playwright-e2e, postgresql-sql-engineering, powershell-engineering, prompt-engineering-review, python-antipatterns, python-design-patterns, python-engineering, random-data-identifiers, release-readiness, review-verification-protocol, root-cause-analysis, ruby-engineering, rust-antipatterns, rust-async-web, rust-code-review, rust-design-patterns, rust-desktop-gui, rust-engineering, rust-persistence-sql, rust-testing-quality, script-engineering, security-review, security-review-evidence, semantic-versioning, sql-engineering, sqlite-sql-engineering, suggest-lucide-icons, svelte-sveltekit-engineering, systematic-debugging, technical-debt-audit, test-driven-development, testing-strategy, threat-modeling, typescript-javascript-antipatterns, typescript-javascript-design-patterns, ux-accessibility-review, webassembly-engineering, zod-engineering

## 场景

需要全仓库代码审查。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我审查整个仓库` |
| agent | 选择专家 "陆鉴"（`engineering-review-board`）：

1. 建地图（扫描全仓）
2. 按需调用专项技能：
   - 架构审查 -> architecture-review
   - 技术债 -> technical-debt-audit
   - 安全 -> security-review
   - 测试 -> testing-strategy
3. 输出证据驱动的审查报告 |

## 产出

全仓审查报告（按专项分类，附证据）

## 验证

每个发现附代码位置；无主观臆断

## 资产位置

- 定义：`experts/engineering-review-board/.codebuddy-plugin/plugin.json`
- 人格：`experts/engineering-review-board/agents/engineering-review-board.md`
- 元数据：`experts/engineering-review-board/manifest.yaml`
