# 工程流程教练（Engineering Workflow Coach）

把一个人从「有个想法」带到「代码合进去、有测试、有人审过」的工程流程教练。

内置 **28 个技能**，覆盖完整工程流水线：

- **入口与编排**：ask-matt、setup-matt-pocock-skills、to-spec、to-tickets、implement、
  implement-spec、wayfinder、triage、handoff
- **工程纪律**：tdd、diagnosing-bugs、code-review、codebase-design、domain-modeling、
  prototype、improve-codebase-architecture、research、retro、pr、writing-for-agents、wizard
- **沟通与学习**：grilling、grill-me、grill-with-docs、to-questionnaire、wait-what、teach
- **元工具**：port-agent-skills

## 主流程

```
想法 → to-spec（规格）→ to-tickets（工单）→ implement（实现 + TDD）→ pr（评审）
```

## 来源与许可

其中 27 个技能译自开源仓库 [mattpocock/skills](https://github.com/mattpocock/skills)
（MIT License，Copyright (c) 2026 Matt Pocock），每个技能的
`references/UPSTREAM-LICENSE.md` 均随附原版权声明与许可全文。
`port-agent-skills` 为本项目自研。
