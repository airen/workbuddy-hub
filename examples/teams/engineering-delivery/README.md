# engineering-delivery 使用示例

**类别**：开发与工程 | **版本**：1.0.0
**成员数**：5 | **主理人**：`engineering-delivery-team-lead`

## 场景

从需求到上线的完整软件交付。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `我要从零做用户认证功能` |
| agent | 选择专家团 "软件工程交付专家团"（`engineering-delivery`）：

**Phase 1 DEFINE**：齐活林澄清需求，写规格
**Phase 2 PLAN**：拆成增量任务
**Phase 3 BUILD**：薄垂直切片实现
**Phase 4 REVIEW**：四路并行审查
- 沈查（代码）-> 五轴审查
- 严过关（测试）-> 覆盖率分析
- 安守正（安全）-> OWASP 映射
- 马迅达（性能）-> CWV 记分卡（仅 Web）
**Phase 5 修复**：按 Critical->Required 顺序修
**Phase 6 SHIP**：对照 DoD 过门禁

产出：完整交付报告 |

## 产出

规格 -> 代码 -> 审查报告 -> 交付报告

## 验证

G1-G5 门禁全过；无未解决 Critical

## 资产位置

- 定义：`teams/engineering-delivery/settings.json` + `agents/*.md`（5 名成员）
- 元数据：`teams/engineering-delivery/manifest.yaml`
