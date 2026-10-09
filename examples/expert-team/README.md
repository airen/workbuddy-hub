# 示例：「软件工程交付专家团」完成一次功能交付

**引用资产**：`teams/engineering-delivery`（development 类，5 名成员）

## 触发方式

在 WorkBuddy 中选择专家团「软件工程交付专家团」，并提出：

- 「我要从零做 X」
- 「这个功能从规格到上线」
- 「新项目 / 新功能 / 重大变更」

## 输入 / 输出

- **输入**：一句模糊需求（例如「给用户加导出 CSV 的功能」）
- **输出**：规格文档 → 拆好的任务清单 → 已实现已测试的增量
  → 四路审查报告 → 修复记录 → 最终交付报告（含上线判断）

## 过程（六阶段）

主理人（`engineering-delivery-team-lead`，齐活林）编排：

1. **DEFINE**：一次只问一个问题，澄清需求到 ~95% 置信度，写出规格与验收标准
2. **PLAN**：拆成小而可验证的增量任务，标依赖顺序
3. **BUILD**：薄垂直切片实现 → 测试 → 验证 → 原子提交
4. **REVIEW**：四位成员**并行**回传结论——
   - 沈查（code-reviewer）：五轴代码审查
   - 严过关（test-engineer）：覆盖率缺口 + Prove-It 复现
   - 安守正（security-auditor）：OWASP 映射 + PoC
   - 马迅达（performance-auditor）：**仅 Web 项目**，Core Web Vitals 记分卡
5. **修复**：主理人按 Critical → Required 顺序修，原审查员复验
6. **SHIP**：对照 `definition-of-done.md` 过底线，给出明确上线 / 不上线判断

## 质量门禁

- 没有书面规格不进入拆解（G1）
- 没有通过的测试不进入下一增量（G2）
- 四路结论未齐不进入修复（G3）
- **存在未解决 Critical 不给上线判断**（G4）

## 验证

最终报告包含：交付物清单、门禁结论、每位审查员的原始结论、
未解决遗留项及原因——而不是一句「做完了」。

## 资产路径

- 团队定义：`teams/engineering-delivery/settings.json` + `agents/*.md`（5 名成员）
- 工作流入口：`teams/engineering-delivery/agents/engineering-delivery-team-lead.md`
- 共享检查清单：`teams/engineering-delivery/references/`
- 元数据：`teams/engineering-delivery/manifest.yaml`
