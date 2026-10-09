# 示例：用 `pr` 技能生成 PR 正文

**引用资产**：`skills/pr`（PR 正文，development 类）

## 触发方式

用户对 agent 说：

- 「写一下 PR 描述」
- 「帮我填 PR 正文」
- 「这个 PR 该怎么写说明」

## 输入 / 输出

- **输入**：当前分支相对目标分支的改动（diff）、改动的动机与前后对比证据
- **输出**：一份按模板组织的 PR 正文，含三个固定区块：
  - `Summary`（摘要 + 配图指引）
  - `Evidence`（证据，前后对比）
  - `Merge Danger`（合并风险：单向门 / 双向门、影响半径）

## 过程

1. 加载 `skills/pr/SKILL.md`，按模板结构填充
2. 从最近 commit 与工作区 diff 提取改动要点
3. 识别改动类型（新功能 / 修复 / 重构），决定 Evidence 用前后对比还是测试记录
4. 判断 Merge Danger：是否改动公共接口、是否单向门（一旦合并难以回退）
5. 输出可直接粘贴到 GitHub PR 界面的 Markdown

## 验证

正文三段齐全、Evidence 能指向具体 diff 或截图、Merge Danger 明确标注了影响半径
（影响哪些调用方 / 页面 / 接口）。

## 资产路径

- 定义：`skills/pr/SKILL.md`
- 参考资料：`skills/pr/references/`
- 元数据：`skills/pr/manifest.yaml`（由 `sync_manifests.py` 生成）
