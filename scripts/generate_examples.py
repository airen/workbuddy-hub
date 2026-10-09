#!/usr/bin/env python3
"""为 hub 全部资产生成使用示例文档。

每个示例包含：场景、对话片段、产出、验证、资产位置。
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "examples"


def _category_label(cat: str) -> str:
    return {
        "development": "开发与工程",
        "content": "内容生产",
        "research": "调研与信息检索",
        "other": "其他",
        "design": "设计与视觉",
        "business": "商业分析与运营",
    }.get(cat, cat)


def _extract_triggers(desc: str) -> str:
    """从 description 提取触发词。"""
    if not desc:
        return "按需调用"
    # 尝试匹配各种引号格式
    for pattern in [
        r'适用于[「『\'](.*?)[」』\']',
        r'当用户(.+?)时',
        r'适用于(.+?)时使用',
    ]:
        m = re.search(pattern, desc, re.S)
        if m:
            text = m.group(1).strip()
            # 取第一段或前 60 字
            parts = re.split(r'[，,、]', text)
            return parts[0][:60] if parts else text[:60]
    return desc[:60]


def _make_dialog(user_prompt: str, agent_response: str) -> str:
    """生成对话表格。"""
    return f"""| 说话者 | 内容 |
|---|---|
| 用户 | `{user_prompt}` |
| agent | {agent_response} |"""


def write_skill_example(id_: str, meta: dict):
    """为技能生成示例。"""
    desc = (meta.get("description") or "").strip()
    category = meta.get("category", "other")
    version = meta.get("version", "1.0.0")
    triggers = _extract_triggers(desc)

    # 根据技能 ID 提供不同的示例内容
    example_contents = {
        "tdd": {
            "scene": "开发新功能或修复 bug 时，希望先写测试。",
            "dialog": _make_dialog(
                "写一个 TDD 循环：为 add_item 方法写测试",
                '加载 `skills/tdd/SKILL.md`，执行红-绿-重构循环：\n\n1. 在接缝上写失败测试\n2. 跑测试确认红\n3. 写最小实现让测试绿\n4. 重构\n5. 提交',
            ),
            "output": "测试文件（tests/test_xxx.py）+ 实现代码",
            "verify": "测试从红变绿，重构后仍绿；git log 可见原子提交",
        },
        "pr": {
            "scene": "准备合入 PR 前，自动生成符合规范的正文。",
            "dialog": _make_dialog(
                "帮我写 PR 描述",
                '加载 `skills/pr/SKILL.md`，从 diff 提取要点，生成三段式正文：\n\n```markdown\n## Summary\n\n重构结算逻辑...\n\n## Evidence\n\n- **Before:** ...\n  **After:** ...\n\n## Merge Danger\n\n**Door:** 双向门\n**Blast Radius:** Cart 类接口未变\n```',
            ),
            "output": "Markdown 文本（可直接粘贴到 GitHub PR 界面）",
            "verify": "三段齐全（Summary / Evidence / Merge Danger），Evidence 有 before/after 对比",
        },
        "code-review": {
            "scene": "代码写完准备合入前，进行全面审查。",
            "dialog": _make_dialog(
                "review 一下 main 分支相对 develop 的改动",
                '加载 `skills/code-review/SKILL.md`，执行：\n\n1. 确定审查范围：git log develop..main --oneline\n2. 并行两个子代理：Standards 轴 + Spec 轴\n3. 输出分级报告（Critical / Required / Optional / Nit）',
            ),
            "output": "分级审查报告（附代码片段和修复建议）",
            "verify": "所有 Critical 已修复；Required 有明确修复路径",
        },
        "handoff": {
            "scene": "会话即将结束或上下文快满时，把进度交给下个 agent。",
            "dialog": _make_dialog(
                "交接一下，下个会话继续实现导出功能",
                '加载 `skills/handoff/SKILL.md`，生成交接文档：\n\n```markdown\n# Handoff: 导出功能\n\n## 上下文\n- 已完成：Cart 模型\n- 待办：export_to_csv()\n\n## 建议加载的技能\n- skills/implement/SKILL.md\n```\n\n保存到临时目录（不进工作区）',
            ),
            "output": "Markdown 交接文档（含上下文、待办、建议技能）",
            "verify": "文档在临时目录，新 agent 读完能直接接手",
        },
        "to-spec": {
            "scene": "对话已讨论过需求，需要沉淀成规格说明。",
            "dialog": _make_dialog(
                "把刚才聊的写成规格",
                '加载 `skills/to-spec/SKILL.md`，综合对话上下文：\n\n```markdown\n## Problem Statement\n用户需要从购物车导出数据...\n\n## Solution\n在 Cart 类上新增 export_to_csv(path)...\n\n## Seams\n- Cart.export_to_csv(path: str) -> None\n```\n发布到 issue 追踪器，打 ready-for-agent',
            ),
            "output": "规格 Markdown 文件（发布到 issue 追踪器）",
            "verify": "规格包含 Problem/Solution/Seams/Acceptance Criteria 四节",
        },
        "to-tickets": {
            "scene": "规格已定，需要拆成可执行的工单。",
            "dialog": _make_dialog(
                "把规格拆成工单",
                '加载 `skills/to-tickets/SKILL.md`，拆出工单：\n\n```\nticket-1: 定义接口（无阻塞）\nticket-2: 实现空购物车处理（阻塞于 ticket-1）\nticket-3: 实现多商品 CSV 生成（阻塞于 ticket-2）\n```\n本地每张工单一个文件',
            ),
            "output": "一组工单文件（含阻塞关系声明）",
            "verify": "工单图无环；最小工单集可独立运行",
        },
        "implement": {
            "scene": "有工单或规格，开始 TDD 实现。",
            "dialog": _make_dialog(
                "开始实现购物车导出功能",
                '加载 `skills/implement/SKILL.md`，按工单执行：\n\n```\n[Red] 写测试 -> [Green] 实现 -> [Refactor] 重构\n提交：feat(cart): export to CSV\n```\n收尾调 code-review',
            ),
            "output": "可运行的代码 + 测试（按工单原子提交）",
            "verify": "测试全绿；code-review 无 Critical",
        },
        "research": {
            "scene": "需要调研一个问题，产出带来源标注的结论。",
            "dialog": _make_dialog(
                "研究一下微信小程序音频支持的格式",
                '加载 `skills/research/SKILL.md`，执行：\n\n1. 搜索官方文档、社区讨论、测试数据\n2. 整理结论到 docs/wechat-audio-formats.md\n3. 每条论断标注来源',
            ),
            "output": "带来源标注的 Markdown 研究报告",
            "verify": "每条结论有至少一个来源；来源可验证",
        },
        "domain-modeling": {
            "scene": "发现领域术语混乱，需要统一概念。",
            "dialog": _make_dialog(
                "理一下购物车领域的模型",
                '加载 `skills/domain-modeling/SKILL.md`：\n\n1. 扫描代码和文档，找出模糊术语\n2. 挑战术语："item" 是指单个商品还是数量？\n3. 更新 GLOSSARY.md',
            ),
            "output": "更新后的 GLOSSARY.md，可能的 ADR 文件",
            "verify": "代码注释和文档使用统一术语；无歧义",
        },
        "grilling": {
            "scene": "方案还没定型，需要有人挑刺。",
            "dialog": _make_dialog(
                "帮我拷问一下这个架构设计",
                '加载 `skills/grilling/SKILL.md`，执行：\n\n1. 画出设计树（所有决策点）\n2. 逐分支拷问：为什么用 Redis？缓存失效策略？\n3. 逼出每个分支的定论',
            ),
            "output": "设计树，每个分支的定论（已解决或标记为风险）",
            "verify": "设计树所有分支都有定论；无悬而未决的关键决策",
        },
        "prototype": {
            "scene": "不确定设计方案对不对，先做个原型验证。",
            "dialog": _make_dialog(
                "搭个原型验证一下这个状态机",
                '加载 `skills/prototype/SKILL.md`：\n\n1. 判断原型类型：逻辑/状态模型 或 UI 变体\n2. 构建一次性原型\n3. 跑测试验证边界情况',
            ),
            "output": "原型代码 + 验证结论（可行/需调整/不可行）",
            "verify": "原型能跑通关键路径；边界情况有答案",
        },
        "ui-design-field-manual": {
            "scene": "AI 生成的界面太丑，像草台班子。",
            "dialog": _make_dialog(
                "这个 UI 太塑料了，帮我美化",
                '加载 `skills/ui-design-field-manual/SKILL.md`：\n\n1. 检查 26 条军规\n2. 输出设计令牌（CSS 变量）\n3. 输出基调卡和自检报告',
            ),
            "output": "设计令牌（CSS 变量）、基调卡、自检报告",
            "verify": "界面符合 26 条军规；无 AI 塑料风",
        },
        "de-ai-rewrite": {
            "scene": "文稿 AI 腔太重，需要改写得更自然。",
            "dialog": _make_dialog(
                "去 AI 味：在当今数字化转型的时代背景下...",
                '加载 `skills/de-ai-rewrite/SKILL.md`，三遍打磨：\n\n**第一遍：删除 AI 模式**\n- 删"在当今...时代背景下"\n- 删"具有至关重要的意义"\n\n**第二遍：注入真实人声**\n- 加具体细节和时间\n- 加人的反应\n\n**第三遍：校对**\n- 确认原意保留\n- 确认检测工具看不出 AI 痕迹',
            ),
            "output": "改写后的自然文本，无 AI 腔模式",
            "verify": '无「此外」「至关重要」「总而言之」等套话；事实性信息保留',
        },
        "agent-doc-memory": {
            "scene": "项目文档散乱，agent 记不住上下文。",
            "dialog": _make_dialog(
                "帮我建一个文档记忆工作区",
                '加载 `skills/agent-doc-memory/SKILL.md`：\n\n1. 扫描现有文档\n2. 创建 INDEX.md 索引\n3. 创建 GLOSSARY.md 术语表\n4. 审计孤儿文档和断链',
            ),
            "output": "文档工作区（INDEX.md, GLOSSARY.md, ADR/, specs/ 等）",
            "verify": "新 agent 进入后能查 INDEX.md 快速理解项目",
        },
        "to-questionnaire": {
            "scene": "需要向某人收集信息做决策。",
            "dialog": _make_dialog(
                "帮我做份问卷，问团队要不要上 Redis",
                '加载 `skills/to-questionnaire/SKILL.md`：\n\n1. 识别决策点\n2. 生成问卷\n3. 输出可直接发给团队的问卷',
            ),
            "output": "问卷 Markdown，可直接发给目标人群",
            "verify": "问题能支撑决策；无诱导性问题",
        },
        "wait-what": {
            "scene": "用户说没看懂上一条消息。",
            "dialog": _make_dialog(
                "等一下，你在说什么",
                '加载 `skills/wait-what/SKILL.md`：\n\n1. 用 ASD-STE100 简化英语重讲\n2. 补上下文\n3. 引用 GLOSSARY.md 里的术语',
            ),
            "output": "简化后的解释，引用 GLOSSARY.md",
            "verify": "用户说看懂了",
        },
        "setup-matt-pocock-skills": {
            "scene": "首次使用工程技能前，配置仓库。",
            "dialog": _make_dialog(
                "初始化仓库，配置工程技能",
                '加载 `skills/setup-matt-pocock-skills/SKILL.md`：\n\n1. 创建 issue 追踪器\n2. 设置分诊标签词汇\n3. 创建领域文档布局\n4. 输出配置报告',
            ),
            "output": "配置好的仓库结构（issue 追踪器、标签、文档目录）",
            "verify": "其他工程技能可以正常引用这些配置",
        },
        "port-agent-skills": {
            "scene": "要把外部 skill 仓库转成 WorkBuddy 格式。",
            "dialog": _make_dialog(
                "把这个 Claude Code skill 仓库转成 WorkBuddy 格式",
                '加载 `skills/port-agent-skills/SKILL.md`：\n\n1. 侦察上游仓库结构\n2. 按转换规范批量转换 SKILL.md\n3. 校验引用完整性\n4. 安装到 skills/ 目录',
            ),
            "output": "转换后的 WorkBuddy skill 包 + 校验报告",
            "verify": "validate.py 零错误；引用无断链",
        },
        "implement-spec": {
            "scene": "完整规格说明，需要并发实现多个工单。",
            "dialog": _make_dialog(
                "按规格实现购物车导出功能",
                '加载 `skills/implement-spec/SKILL.md`：\n\n1. 读规格和关联工单\n2. 构建阻塞图，识别可并发工单\n3. 在集成分支上并发调度子代理\n4. 完成后跑 code-review\n5. 结掉所有工单',
            ),
            "output": "集成分支上的完整实现，code-review 报告，所有工单已结",
            "verify": "集成分支测试全绿；code-review 无阻断项",
        },
        "grill-me": {
            "scene": "想让别人帮自己挑刺。",
            "dialog": _make_dialog(
                "拷问我这个方案",
                '加载 `skills/grill-me/SKILL.md`，委托给 `grilling` 技能执行深度访谈',
            ),
            "output": "设计树 + 每个分支的定论",
            "verify": "同 grilling",
        },
        "grill-with-docs": {
            "scene": "拷问的同时想留下文档。",
            "dialog": _make_dialog(
                "拷问我并顺便把文档写了",
                '加载 `skills/grill-with-docs/SKILL.md`，边拷问边生成：\n- ADR 文件\n- 术语表片段（更新 GLOSSARY.md）',
            ),
            "output": "ADR 文件 + 更新的 GLOSSARY.md",
            "verify": "每个关键决策都有 ADR；术语表无歧义",
        },
        "improve-codebase-architecture": {
            "scene": "觉得架构太浅，想系统化重构。",
            "dialog": _make_dialog(
                "帮我看看哪里能重构",
                '加载 `skills/improve-codebase-architecture/SKILL.md`：\n\n1. 扫描代码库\n2. 找出浅模块\n3. 生成 HTML 报告\n4. 用户选一个模块，深入拷问',
            ),
            "output": "HTML 报告 + 深入讨论记录",
            "verify": "报告指向具体可重构点",
        },
        "codebase-design": {
            "scene": "想深化模块设计，提升可测试性。",
            "dialog": _make_dialog(
                "帮我 deepen 这个模块",
                '加载 `skills/codebase-design/SKILL.md`：\n\n1. 扫描代码，识别浅模块\n2. 输出深化建议（模块边界、接口设计、接缝）\n3. 可视化报告（HTML）',
            ),
            "output": "深化建议 + 可视化 HTML 报告",
            "verify": "建议可执行；接口设计提升可测试性",
        },
        "retro": {
            "scene": "一次会话结束，想复盘改进。",
            "dialog": _make_dialog(
                "复盘一下这次会话",
                '加载 `skills/retro/SKILL.md`：\n\n1. 回顾会话过程\n2. 找出可改进的候选项\n3. 输出改进建议',
            ),
            "output": "复盘报告 + 改进候选项",
            "verify": "候选项具体可执行",
        },
        "triage": {
            "scene": "有 issue/PR 需要分类和分诊。",
            "dialog": _make_dialog(
                "帮我 triage 一下这些 issue",
                '加载 `skills/triage/SKILL.md`：\n\n1. 读取 issue/PR 列表\n2. 分类：bug / feature / docs / ...\n3. 核验：是否可复现？是否有足够信息？\n4. 必要时拷问澄清\n5. 输出 agent 可执行的简报',
            ),
            "output": "分类后的 issue 列表 + agent 执行简报",
            "verify": "每个 issue 有明确分类和执行建议",
        },
        "wayfinder": {
            "scene": "项目太大，需要规划路线。",
            "dialog": _make_dialog(
                "这个项目太大了，帮我规划一下",
                '加载 `skills/wayfinder/SKILL.md`：\n\n1. 识别关键决策点\n2. 生成决策票据地图（issue tracker）\n3. 逐张推进，直到路线清晰',
            ),
            "output": "决策票据地图（系列 issue）",
            "verify": "地图覆盖所有关键决策；路线清晰可执行",
        },
        "wizard": {
            "scene": "需要引导用户完成手动配置步骤。",
            "dialog": _make_dialog(
                "帮我配置一下 CI secrets",
                '加载 `skills/wizard/SKILL.md`：\n\n1. 识别需要人工操作的步骤\n2. 生成交互式向导\n3. 逐阶段确认',
            ),
            "output": "交互式 bash 向导脚本",
            "verify": "向导能引导用户完成配置，每步有确认",
        },
        "writing-for-agents": {
            "scene": "要写 skill 或 AGENTS.md 给 agent 用。",
            "dialog": _make_dialog(
                "帮我写一份 AGENTS.md",
                '加载 `skills/writing-for-agents/SKILL.md`：\n\n1. 讲解写作原则（上下文指针、两种负载、完成判据...）\n2. 协助用户写出 AGENTS.md',
            ),
            "output": "符合 agent 阅读习惯的 AGENTS.md",
            "verify": "其他 agent 能无歧义理解和使用",
        },
        "teach": {
            "scene": "想系统学习某个主题。",
            "dialog": _make_dialog(
                "教我用 TDD",
                '加载 `skills/teach/SKILL.md`：\n\n1. 创建 MISSION.md 任务书\n2. 创建 GLOSSARY.md 术语表\n3. 规划学习路径（HTML 课程）\n4. 跨会话维护学习记录',
            ),
            "output": "学习材料（MISSION.md, GLOSSARY.md, HTML 课程）",
            "verify": "学习路径清晰；术语表完整",
        },
        "ai-project-pilot": {
            "scene": "要推进一个 AI 项目落地。",
            "dialog": _make_dialog(
                "帮我推进这个 AI 助手项目",
                '加载 `skills/ai-project-pilot/SKILL.md`，四阶段推进：\n\n1. 立项：项目章程、成功标准\n2. 计划：WBS、里程碑、资源与风险\n3. 执行监控：状态报告、偏差纠正\n4. 验收上线：验收记录、运营交接包',
            ),
            "output": "项目章程、WBS、状态报告、验收记录等文档",
            "verify": "各阶段文档齐全；成功标准可测量",
        },
        "ask-matt": {
            "scene": "不知道下一步该用什么技能。",
            "dialog": _make_dialog(
                "我现在该干嘛？",
                '加载 `skills/ask-matt/SKILL.md`，根据当前处境推荐：\n- 想法模糊 -> idea-refine\n- 需求已清 -> to-spec\n- 代码有问题 -> diagnosing-bugs\n- ...（按路由表）',
            ),
            "output": "推荐的下一步行动和技能",
            "verify": "推荐与当前处境匹配",
        },
    }

    ex = example_contents.get(id_, None)
    if not ex:
        # 通用模板
        text = f"""# {id_} 使用示例

**类别**：{_category_label(category)} | **版本**：{version}

## 场景

加载 `skills/{id_}/SKILL.md`，按完成判据执行相关任务。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `{triggers}` |
| agent | 加载 `skills/{id_}/SKILL.md`，按完成判据执行 |

## 产出

（参见核心过程）

## 验证

对照 `references/` 下的 checklist 自检

## 资产位置

- 定义：`skills/{id_}/SKILL.md`
- 元数据：`skills/{id_}/manifest.yaml`
"""
    else:
        text = f"""# {id_} 使用示例

**类别**：{_category_label(category)} | **版本**：{version}

## 场景

{ex['scene']}

## 对话片段

{ex['dialog']}

## 产出

{ex['output']}

## 验证

{ex['verify']}

## 资产位置

- 定义：`skills/{id_}/SKILL.md`
- 元数据：`skills/{id_}/manifest.yaml`
"""

    out_dir = EXAMPLES / "skills" / id_
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "README.md").write_text(text, encoding="utf-8")
    print(f"  WROTE skills/{id_}/README.md")


def write_expert_example(id_: str, meta: dict):
    """为专家生成示例。"""
    desc = (meta.get("description") or "").strip()
    category = meta.get("category", "other")
    version = meta.get("version", "1.0.0")
    skills = meta.get("skills", [])
    skills_str = ", ".join(skills) if skills else "无内嵌技能"
    name = meta.get("name", id_)
    triggers = _extract_triggers(desc)

    example_contents = {
        "lao-dao-editor": {
            "scene": "有 AI 腔文稿需要改写。",
            "dialog": _make_dialog(
                "去 AI 味：在当今数字化转型的时代背景下...",
                '选择专家 "老刀"（`lao-dao-editor`），内部编排 `de-ai-rewrite` 技能：\n\n**第一遍：删除 AI 模式**\n- 删"在当今...时代背景下"\n- 删"具有至关重要的意义"\n\n**第二遍：注入真实人声**\n- 加具体细节和时间\n- 加人的反应\n\n**第三遍：校对**\n- 确认原意保留\n- 确认检测工具看不出 AI 痕迹\n\n产出：自然文本版本',
            ),
            "output": "改写后的自然文本",
            "verify": "无 AI 套话；事实信息完整；读起来像人写的",
        },
        "doc-memory-steward": {
            "scene": "项目知识散落各处，需要建立文档记忆。",
            "dialog": _make_dialog(
                "帮我建一个项目知识库",
                '选择专家 "纪文远"（`doc-memory-steward`），编排 `agent-doc-memory` 技能：\n\n1. 扫描现有文档\n2. 创建 INDEX.md\n3. 创建 GLOSSARY.md\n4. 审计孤儿文档和断链\n\n产出：文档工作区',
            ),
            "output": "文档工作区（INDEX.md, GLOSSARY.md 等）",
            "verify": "新 agent 能查 INDEX 快速理解项目",
        },
        "diagram-architect": {
            "scene": "需要画技术图表。",
            "dialog": _make_dialog(
                "画一个微服务架构图",
                '选择专家 "江图南"（`diagram-architect`）：\n\n1. 定图型：架构图\n2. 定出口：SVG（内联）+ PNG（落盘）\n3. 调度绘图能力库（svg-diagram / dashmotion / archify 等）\n4. 过质检闸门（svg-lint）\n5. 交付\n\n产出：SVG + PNG 图表',
            ),
            "output": "SVG + PNG 图表文件",
            "verify": "图表无断链；符合设计系统；质检闸门全过",
        },
        "agent-memory-advisor": {
            "scene": "要选型智能体记忆方案。",
            "dialog": _make_dialog(
                "帮我选一个记忆架构",
                '选择专家 "智能体记忆选型顾问"（`agent-memory-advisor`）：\n\n1. 按场景分类（写代码/个人智能体/公司大脑）\n2. 对比 10 个开源记忆项目\n3. 挑出能落地的一套\n4. 诊断记忆断环\n\n产出：选型报告 + 断环诊断',
            ),
            "output": "选型报告（推荐方案 + 理由）+ 断环诊断",
            "verify": "方案与场景匹配；断环有修复建议",
        },
        "eng-workflow-coach": {
            "scene": "需要全流程工程指导。",
            "dialog": _make_dialog(
                "我要从零做这个功能",
                '选择专家 "工程流程教练"（`eng-workflow-coach`）：\n\n编排 29 个技能，按场景路由：\n- 想法模糊 -> idea-refine\n- 需求已清 -> to-spec -> to-tickets -> implement\n- 卡住了 -> grilling 拷问到底\n- 交付前 -> code-review\n\n产出：完整交付物',
            ),
            "output": "从规格到代码的完整交付",
            "verify": "全流程覆盖；质量门禁通过",
        },
        "software-architect": {
            "scene": "需要架构决策支持。",
            "dialog": _make_dialog(
                "帮我做架构权衡分析",
                '选择专家 "方权衡"（`software-architect`）：\n\n1. 识别质量属性（性能/可扩展性/一致性...）\n2. 风格选型（微服务/单体/事件驱动...）\n3. 领域建模\n4. 分布式数据设计\n5. 产出 ADR + 图表',
            ),
            "output": "ADR 文档 + 架构图表",
            "verify": "每个决策有理由和权衡分析",
        },
        "spec-driven-dev": {
            "scene": "需求模糊，需要固化成规格。",
            "dialog": _make_dialog(
                "帮我写一份规格说明",
                '选择专家 "章立言"（`spec-driven-dev`）：\n\n1. 章程 -> 规格 -> 澄清 -> 方案 -> 任务清单 -> 校验 -> 收敛\n2. 每步产出对应文档\n\n产出：完整规格包',
            ),
            "output": "规格文档包（章程、规格、任务清单等）",
            "verify": "规格可执行；验收标准明确",
        },
        "engineering-review-board": {
            "scene": "需要全仓库代码审查。",
            "dialog": _make_dialog(
                "帮我审查整个仓库",
                '选择专家 "陆鉴"（`engineering-review-board`）：\n\n1. 建地图（扫描全仓）\n2. 按需调用专项技能：\n   - 架构审查 -> architecture-review\n   - 技术债 -> technical-debt-audit\n   - 安全 -> security-review\n   - 测试 -> testing-strategy\n3. 输出证据驱动的审查报告',
            ),
            "output": "全仓审查报告（按专项分类，附证据）",
            "verify": "每个发现附代码位置；无主观臆断",
        },
        "self-media-studio": {
            "scene": "要做自媒体内容生产。",
            "dialog": _make_dialog(
                "帮我写一篇小红书笔记",
                '选择专家 "柳成文"（`self-media-studio`）：\n\n编排 10 个模块：\n1. 选题情报 -> 2. 内容 brief -> 3. 策略 -> 4. 趋势雷达\n5. 平台文案 -> 6. 短视频 -> 7. 数据分析\n8. 内容交付 -> 9. 微信发布 -> 10. 视频发布\n\n人工确认每个环节\n\n产出：可直接发布的成品',
            ),
            "output": "多平台发布成品 + 数据复盘",
            "verify": "内容符合平台规范；数据可追踪",
        },
    }

    ex = example_contents.get(id_, None)
    if not ex:
        text = f"""# {id_} 使用示例

**类别**：{_category_label(category)} | **版本**：{version}
**编排技能**：{skills_str}

## 场景

选择专家 "{name}"（`{id_}`），加载其人格后执行相关任务。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `{triggers}` |
| agent | 选择专家 "{name}"（`{id_}`），加载其人格 |

## 产出

（参见核心过程）

## 验证

对照完成判据自检

## 资产位置

- 定义：`experts/{id_}/.codebuddy-plugin/plugin.json`
- 人格：`experts/{id_}/agents/{id_}.md`
- 元数据：`experts/{id_}/manifest.yaml`
"""
    else:
        text = f"""# {id_} 使用示例

**类别**：{_category_label(category)} | **版本**：{version}
**编排技能**：{skills_str}

## 场景

{ex['scene']}

## 对话片段

{ex['dialog']}

## 产出

{ex['output']}

## 验证

{ex['verify']}

## 资产位置

- 定义：`experts/{id_}/.codebuddy-plugin/plugin.json`
- 人格：`experts/{id_}/agents/{id_}.md`
- 元数据：`experts/{id_}/manifest.yaml`
"""

    out_dir = EXAMPLES / "experts" / id_
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "README.md").write_text(text, encoding="utf-8")
    print(f"  WROTE experts/{id_}/README.md")


def write_team_example(id_: str, meta: dict):
    """为专家团生成示例。"""
    desc = (meta.get("description") or "").strip()
    category = meta.get("category", "other")
    version = meta.get("version", "1.0.0")
    members = meta.get("members", [])
    member_count = len(members)
    name = meta.get("name", id_)
    triggers = _extract_triggers(desc)
    lead = next((m["expert_id"] for m in members if "team-lead" in m.get("expert_id", "")), "")

    example_contents = {
        "engineering-delivery": {
            "scene": "从需求到上线的完整软件交付。",
            "dialog": _make_dialog(
                "我要从零做用户认证功能",
                '选择专家团 "软件工程交付专家团"（`engineering-delivery`）：\n\n**Phase 1 DEFINE**：齐活林澄清需求，写规格\n**Phase 2 PLAN**：拆成增量任务\n**Phase 3 BUILD**：薄垂直切片实现\n**Phase 4 REVIEW**：四路并行审查\n- 沈查（代码）-> 五轴审查\n- 严过关（测试）-> 覆盖率分析\n- 安守正（安全）-> OWASP 映射\n- 马迅达（性能）-> CWV 记分卡（仅 Web）\n**Phase 5 修复**：按 Critical->Required 顺序修\n**Phase 6 SHIP**：对照 DoD 过门禁\n\n产出：完整交付报告',
            ),
            "output": "规格 -> 代码 -> 审查报告 -> 交付报告",
            "verify": "G1-G5 门禁全过；无未解决 Critical",
        },
        "deep-research-crew": {
            "scene": "需要深度研究并产出带源报告。",
            "dialog": _make_dialog(
                "帮我研究一下 LLM 的微调方案",
                '选择专家团 "深度研究专家团"（`deep-research-crew`）：\n\n七角色流水线：\n1. 导航 -> 2. 清洗 -> 3. 解构 -> 4. 归档 -> 5. 溯源 -> 6. 审核 -> 7. 写作\n\n产出：带源报告',
            ),
            "output": "带来源标注的研究报告",
            "verify": "每条论断有出处；来源可验证",
        },
        "hai-stack": {
            "scene": "做一次软件迭代。",
            "dialog": _make_dialog(
                "帮我迭代这个功能",
                '选择专家团 "软件迭代专家团"（`hai-stack`）：\n\n1. 判断值不值得做\n2. 设计边界\n3. TDD 落地\n4. 证据确认\n5. 文档沉淀\n\n产出：迭代产物 + 文档',
            ),
            "output": "迭代产物 + 技术文档",
            "verify": "迭代目标达成；文档干净",
        },
        "creator-ops": {
            "scene": "做自媒体内容生产。",
            "dialog": _make_dialog(
                "帮我做个小红书爆款笔记",
                '选择专家团 "自媒体创作专家团"（`creator-ops`）：\n\n六位环节专家接力：\n1. 闻先机（选题情报）\n2. 毕成章（文案）\n3. 颜可观（视觉）\n4. 陶成帧（视频）\n5. 郑多平（发布）\n6. 查有数（数据复盘）\n\n产出：可直接发布的成品',
            ),
            "output": "多平台发布成品 + 数据复盘",
            "verify": "内容符合平台规范；数据可追踪",
        },
        "media-content-team": {
            "scene": "做小红书和公众号图文。",
            "dialog": _make_dialog(
                "帮我写一篇公众号文章",
                '选择专家团 "自媒体图文产线团"（`media-content-team`）：\n\n1. 热点选题\n2. 对标拆解\n3. 封面配图\n4. 多平台排版\n\n默认只出草稿，不自动群发\n\n产出：图文草稿',
            ),
            "output": "图文草稿（小红书 + 公众号）",
            "verify": "排版符合平台规范；内容无敏感信息",
        },
    }

    ex = example_contents.get(id_, None)
    if not ex:
        text = f"""# {id_} 使用示例

**类别**：{_category_label(category)} | **版本**：{version}
**成员数**：{member_count} | **主理人**：`{lead or '（未指定）'}`

## 场景

选择专家团 "{name}"（`{id_}`），由主理人编排多角色协作。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `{triggers}` |
| agent | 选择专家团 "{name}"（`{id_}`），由主理人编排多角色协作 |

## 产出

（参见核心过程）

## 验证

对照完成判据自检

## 资产位置

- 定义：`teams/{id_}/settings.json` + `agents/*.md`（{member_count} 名成员）
- 元数据：`teams/{id_}/manifest.yaml`
"""
    else:
        text = f"""# {id_} 使用示例

**类别**：{_category_label(category)} | **版本**：{version}
**成员数**：{member_count} | **主理人**：`{lead or '（未指定）'}`

## 场景

{ex['scene']}

## 对话片段

{ex['dialog']}

## 产出

{ex['output']}

## 验证

{ex['verify']}

## 资产位置

- 定义：`teams/{id_}/settings.json` + `agents/*.md`（{member_count} 名成员）
- 元数据：`teams/{id_}/manifest.yaml`
"""

    out_dir = EXAMPLES / "teams" / id_
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "README.md").write_text(text, encoding="utf-8")
    print(f"  WROTE teams/{id_}/README.md")


def main():
    registry_files = [
        ("skills", REPO / "registry" / "skills.yaml", write_skill_example),
        ("experts", REPO / "registry" / "experts.yaml", write_expert_example),
        ("teams", REPO / "registry" / "teams.yaml", write_team_example),
    ]

    for label, path, writer in registry_files:
        if not path.exists():
            print(f"SKIP {label}: not found")
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        key = {"skills": "skills", "experts": "experts", "teams": "teams"}[label]
        items = data.get(key, [])
        for meta in items:
            if not isinstance(meta, dict):
                continue
            id_ = meta.get("id")
            if not id_:
                continue
            writer(id_, meta)

    print("\nDone.")


if __name__ == "__main__":
    main()
