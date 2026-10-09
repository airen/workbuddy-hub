---
name: implement
display_name: "按规格实现"
display_name_en: "Implement"
description: "该技能用于按一份规格说明或一组工单把用户描述的工作实现出来：在事先约定好的接缝（seam）上驱动 TDD，定期跑类型检查与单测、最后跑一次完整测试套件，收尾时用 code-review 技能评审并把工作提交到当前分支。适用于「开始实现」「按工单做」「把规格做出来」「动手写吧」「implement」这类需求。"
description_zh: "按规格或工单把工作实现出来，驱动 TDD，收尾跑代码评审"
description_en: "Implement a piece of work from a spec or tickets, driving TDD and closing with a review."
category: development-tools
version: 1.0.0
author: "大漠"
disable-model-invocation: true
agent_created: true
---

# 实施（implement）

实施用户在规格说明或工单里描述的工作。

尽可能在事先约定好的接缝（seam）上使用 `tdd` 技能。

定期跑类型检查、定期跑单个测试文件，最后跑一次完整测试套件。

完成后，用 `code-review` 技能评审这项工作。

把工作提交到当前分支。
