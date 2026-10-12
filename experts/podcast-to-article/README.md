# podcast-to-article 陈听

播客改稿主编（Agent 型，分类：06-ContentCreative）。

![播客改稿工作流程](assets/upstream-workflow.jpg)

- **人设**：播客改稿主编，把一段口语对谈改写成读者愿意读完、能理解、愿意转发的中文长文。不复述录音时间线，也不把受访者当金句供应商。
- **默认工作流**：获取可靠文字稿 → 通读选材 → 按读者问题重组 → 生成第一正文章节完整内容配图 → **等确认** → 逐章配图 → 按需存入 Obsidian。
- **三条判据**：**原声得是真的**（直接引用 / 整理引用 / 作者提炼分得清，可回溯原稿）、**重组得有依据**（围绕读者问题而非录音顺序，标题不比正文依据更强）、**图片得被点过头**（首图未确认不生成其余章节）。
- **输入**：YouTube / 小宇宙单集链接、用户逐字稿、本地音视频。只有简介或不完整字幕时会**明确写出覆盖范围**，绝不凭标题和简介编造访谈。
- **输出**：完整文章 + 短编辑备注（重大删改、补充解释、整理引用、待确认事实）；配图默认 3:2、极简视觉隐喻风。
- **归档**：用户说「存入 Obsidian」时，把成稿与已接受配图导出到本机配置的仓库（脚本只用 Python 标准库，配置存本机、不进包）。
- **内置技能**：`skills/keke-podcast-to-article`
  - `SKILL.md` — 核心写作与配图规则
  - `references/editorial-examples.md` — 七种转换的已验证编辑实例与边界
  - `references/source-input-workflow.md` — YouTube / 小宇宙链接输入流程
  - `references/punk-illustration-workflow.md` — 章节配图流程（首图试看、逐章生成、全部生成）
  - `references/obsidian-export.md` — 通用 Obsidian 导出说明
  - `scripts/save_to_obsidian.py` — 本机配置与文章附件导出（零第三方依赖）

## 三个人工确认点

| 编号 | 确认点 | 门禁 |
|---|---|---|
| G1 | 文字稿可靠、覆盖范围明确 | 没有可靠文字稿不硬写长文 |
| G2 | 首图确认 | 未获明确确认不为其余章节配图 |
| G3 | 保存授权 | 未授权不写任何 Obsidian 文件 |

## 依赖与降级

- **文章整理**：由专家自身完成，无需额外库。
- **链接输入**：需要可用的浏览 / 字幕获取 / 转写能力。受限时请用户提供原稿，不承诺任意链接都能转写。
- **配图**：使用当前环境的图像生成能力；若本机安装了上游提到的 `punk-cover` 风格资源可沿用其风格。**缺失时照常交付文章**，只说明配图尚未完成。
- **Obsidian 导出**：需要 Python 3.9+ 与本机可写仓库，只用标准库。

## 来源与许可

上游仓库：<https://github.com/sunkeke-ai/keke-podcast-to-article>（MIT License, Copyright (c) 2026 sunkeke-ai）。

本包保留上游技能正文、参考资料与脚本原文，仅新增 WorkBuddy 编排层（persona、元数据、头像）；唯一的上游文件改动是给 `SKILL.md` 的 frontmatter 追加平台必需的 `display_name` / `display_name_en` / `category` / `version` 四个字段。详见 `LICENSE` 的归属说明。

由大漠基于 sunkeke-ai 的开源技能整理制作。
