#!/usr/bin/env python3
"""校验转换后的 WorkBuddy skill 是否符合规范。

用法:
    python3 validate_skill.py <skills-root> [<skills-root> ...]

`<skills-root>` 是装着各 skill 目录的父目录（如 ~/.workbuddy-ai/skills）。
每个子目录若含 SKILL.md 就被当作一个技能来校验。

校验项：
  1. frontmatter 字段齐全：
     - 两种形态都接受：本地自用（name / description / agent_created）
       与市场发布（再加 display_name / display_name_en / description_zh /
       description_en / category / version / author）
     - agent_created 必须为 true
  2. name 字段 == 目录名
  3. description 是中文且长度合理
  4. 正文无残留的 harness 专属字段与安装命令
  5. 正文无残留的「/技能名」斜杠引用
  6. 正文无裸 sub-agent
  7. 正文里的相对链接（.md/.sh/.py/.cjs/.json）真实存在

注意：`disable-model-invocation`、`user-invocable`、`allowed-tools` **是 WorkBuddy 支持的字段**
（见 https://open.workbuddy.cn/docs/skill），**不**列入禁用清单。别把它们当成别家的残留删掉。

退出码：0 = 无硬性问题，1 = 有硬性问题。

两处豁免，避免误报：
  - 「来源与致谢」小节被排除在检查 4/5/6 之外 —— 那段文字会正当地提及被移除的字段名。
  - 正文里出现 `<!-- validate: allow-legacy-terms -->` 的文件，跳过检查 4 与检查 6
    （用于本身就在讲转换、或在教 harness 字段机制的技能）。

注意：根目录下若混有第三方 / 市场安装的技能，它们的 frontmatter 形态各不相同，
可能被判为硬性问题。此时把待校验的技能先收拢到一个独立目录再跑。
"""
import os, re, sys

FORBIDDEN = [
    "argument-hint",
    ".claude-plugin",
    "claude plugins install",
    "npx skills@latest",
]

# 市场发布格式要求的字段（出现了其中任一，就要求全套齐全）
MARKET_FIELDS = ["display_name", "display_name_en", "description_zh",
                 "description_en", "category", "version", "author"]

# category 的合法取值，从市场真实技能反查得到（官方文档示例里的 writing 不在其中）
CATEGORIES = {
    "development-tools", "productivity-tools", "content-creation", "data-analysis",
    "business-operations", "knowledge-learning", "collaboration", "investment-finance",
}

SLASH_TARGETS = [
    "grill-me", "grill-with-docs", "grilling", "tdd", "code-review", "to-spec",
    "to-tickets", "implement", "implement-spec", "wayfinder", "retro", "triage",
    "prototype", "diagnosing-bugs", "research", "domain-modeling", "codebase-design",
    "pr", "wizard", "ask-matt", "setup-matt-pocock-skills", "handoff", "teach",
    "to-questionnaire", "wait-what", "writing-for-agents",
    "improve-codebase-architecture",
]


def check(root, only=None):
    problems, warnings, stats = [], [], []
    if not os.path.isdir(root):
        return [f"{root}: 不是目录"], [], []

    for name in sorted(os.listdir(root)):
        d = os.path.join(root, name)
        skill_md = os.path.join(d, "SKILL.md")
        if not os.path.isdir(d) or not os.path.isfile(skill_md):
            continue
        if only is not None and name not in only:
            continue

        text = open(skill_md, encoding="utf-8").read()

        # 有些技能本身就在「讲怎么转换」或「讲 harness 的字段机制」，
        # 会正当地提到这些字段名。这类文件在正文里放一个开关关掉该检查：
        #   <!-- validate: allow-legacy-terms -->
        allow_legacy = "validate: allow-legacy-terms" in text

        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            problems.append(f"{name}: frontmatter 缺失或格式错误")
            continue
        fm = m.group(1)

        # 正文检查一律只看 frontmatter 之后的内容 ——
        # frontmatter 里的英文简介（如 description_en）用 sub-agents 是正确英文，不该报。
        body = re.split(r"^##\s*来源与致谢\s*$", text[m.end():], flags=re.M)[0]

        keys = re.findall(r"^([A-Za-z_][\w-]*):", fm, re.M)
        if "name" not in keys or "description" not in keys:
            problems.append(f"{name}: frontmatter 缺 name / description（实为 {keys}）")
        # 市场发布格式：出现任一市场字段，就要求全套齐全
        present = [k for k in MARKET_FIELDS if k in keys]
        if present and len(present) != len(MARKET_FIELDS):
            missing = [k for k in MARKET_FIELDS if k not in keys]
            problems.append(f"{name}: 像是市场发布格式，但缺字段 {missing}")
        if not re.search(r"^agent_created:\s*true\s*$", fm, re.M):
            problems.append(f"{name}: agent_created 不是 true")
        nm = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
        if not nm or nm.group(1) != name:
            problems.append(f"{name}: name 字段 = {nm.group(1) if nm else None}，与目录名不一致")
        dm = re.search(r"^description:\s*(.+)$", fm, re.M)
        if not dm or len(dm.group(1).strip()) < 30:
            problems.append(f"{name}: description 缺失或过短")
        elif not re.search(r"[\u4e00-\u9fff]", dm.group(1)):
            problems.append(f"{name}: description 不含中文")

        cm = re.search(r"^category:\s*(\S+)\s*$", fm, re.M)
        if cm and cm.group(1) not in CATEGORIES:
            warnings.append(
                f"{name}: category={cm.group(1)} 不在已知枚举内（{sorted(CATEGORIES)}）")

        if not allow_legacy:
            for bad in FORBIDDEN:
                if bad in body:
                    problems.append(f"{name}: 正文残留 `{bad}`")
        for t in SLASH_TARGETS:
            for mm in re.finditer(r"(?<![\w/`])/" + re.escape(t) + r"(?![\w-])", body):
                warnings.append(f"{name}: 疑似残留斜杠引用 `/{t}` @偏移 {mm.start()}")
        if re.search(r"(?<!代)(?<!后台)sub-agent", body) and not allow_legacy:
            warnings.append(f"{name}: 出现裸 `sub-agent`")

        for lm in re.finditer(r"\]\(([^)#\s]+\.(?:md|sh|py|cjs|json))\)", body):
            target = lm.group(1)
            if target.startswith(("http://", "https://")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(d, target))):
                problems.append(f"{name}: 链接断链 `{target}`")

        refs = sum(
            len([f for f in os.listdir(os.path.join(d, sub)) if not f.startswith(".")])
            for sub in ("references", "scripts", "templates", "assets")
            if os.path.isdir(os.path.join(d, sub))
        )
        stats.append((name, text.count("\n"), refs))
    return problems, warnings, stats


def main():
    roots = sys.argv[1:] or ["."]
    rc = 0
    for root in roots:
        problems, warnings, stats = check(root)
        print("=" * 72)
        print(f"根目录: {root}    技能数: {len(stats)}")
        print("=" * 72)
        for n, l, r in stats:
            print(f"  {n:<38}{l:>8} 行  {r:>3} 个附属文件")
        if stats:
            print("-" * 72)
            print(f"  SKILL.md 合计 {sum(l for _, l, _ in stats)} 行，"
                  f"附属文件合计 {sum(r for _, _, r in stats)} 个")
        print()
        print(f"❌ 硬性问题: {len(problems)}")
        for p in problems:
            print("   " + p)
        print(f"⚠️  提示性告警: {len(warnings)}")
        for w in warnings:
            print("   " + w)
        print()
        if problems:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
