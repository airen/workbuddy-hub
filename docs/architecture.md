# 架构设计

## 设计目标

`workbuddy-hub` 解决一个问题：**分散在多处的 WorkBuddy 能力资产（技能/专家/专家团）难以统一查看、检索、校验和再发布**。
它既服务于人工维护，也为后续让 WorkBuddy 或 AI 编程助手自动创建/检查/更新资产打基础。

核心原则：**单一事实来源 + 派生索引**。

- **单一事实来源**：每个资产的权威定义在 WorkBuddy 原生文件里（`SKILL.md` / `.codebuddy-plugin/plugin.json` / `agents/*.md`）。这些文件能直接打包上传到 open.workbuddy.cn。
- **派生索引**：`manifest.yaml` 与 `registry/*.yaml` 都是从原生文件**自动生成**的元数据，用于检索、筛选、引用检查，绝不手写维护第二份。

## 三层结构

```
资产定义层      skills/  experts/  teams/      ← 每个资产是一个目录，内含 WorkBuddy 原生文件
   │  (sync_manifests.py 生成 manifest.yaml)
   ▼
组合/索引层     registry/  schemas/             ← 全局索引 + 格式校验
   │  (build_registry.py 生成 registry；validate.py 按 schema 校验)
   ▼
管理工具层      scripts/  templates/  tests/    ← 创建/校验/打包/发布的自动化
```

- **资产定义层**：按资产类型分桶（`skills/`、`experts/`、`teams/`）。每个子目录名 = 资产 ID。
- **组合层**：`registry/` 是跨资产的全局视图；`schemas/` 是 manifest 的格式契约。
- **管理工具层**：`scripts/` 提供可重复的自动化；`templates/` 提供从零脚手架；`tests/` 放回归测试。

## 数据流向

```
新增/修改资产
   │
   ▼
import_asset.py  →  放入 skills/ experts/ teams/ 的对应 bucket
   │
   ▼
sync_manifests.py  →  读取 plugin.json / SKILL.md，写出 manifest.yaml
   │
   ▼
build_registry.py  →  聚合所有 manifest → registry/*.yaml + 引用完整性检查
   │
   ▼
validate.py  →  按 schemas/*.json 校验 manifest + 结构检查
   │
   ▼
（未来）package.py  →  从 bucket 打包成 open.workbuddy.cn 可上传的 zip
```

## 为什么不在 hub 里另写一套 EXPERT.md / TEAM.md

推荐结构示例里用了 `EXPERT.md` / `TEAM.md` 作为主文档。但 WorkBuddy 平台实际读取的是
`.codebuddy-plugin/plugin.json` + `agents/<id>.md`。为避免「同一份人格描述维护两份、迟早不一致」，
hub 直接以 WorkBuddy 原生文件为权威，仅在根目录附加一个派生的 `manifest.yaml`。详见 `workbuddy-compatibility.md`。

## 引用关系（避免重复维护）

- Team 引用 Expert ID，Expert 引用 Skill ID。
- 更新一个 Skill 时，所有引用它的 Expert / Team 自动受益（因为它们引用的是 ID，而非复制技能内容）。
- 当前核心资产中，专家团成员多为「团队自带」（embedded），未单独登记在 `experts/` 中——这是 WorkBuddy 平台打包的常态，`build_registry.py` 会标记为 `embedded=true` 并仅给出警告，不影响索引。
