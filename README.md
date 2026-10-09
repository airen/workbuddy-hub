# workbuddy-hub

WorkBuddy 能力资产枢纽（Asset Hub）。把分散的 **Skills（技能）**、**Experts（专家）**、**Teams（专家团）**
按统一结构集中管理，方便人工维护，也方便 WorkBuddy / AI 编程助手自动创建、检查与更新资产。

> 本仓库目前承载「大漠」自研并上架到 open.workbuddy.cn 的核心资产，以及用于本地管理索引的脚本与规范。

## 仓库结构

```
workbuddy-hub/
├── README.md / CONTRIBUTING.md / CHANGELOG.md / LICENSE
├── skills/        # Skill 能力库（每个子目录一个技能，含 SKILL.md）
├── experts/       # Expert 专家库（单专家，含 .codebuddy-plugin + agents/）
├── teams/         # Team 专家团库（含多个 agents/ 与 settings.json）
├── registry/      # 由脚本自动生成的全局索引（skills/experts/teams/categories.yaml）
├── schemas/       # manifest.yaml 的 JSON Schema 校验规则
├── templates/     # 新建资产的脚手架
├── scripts/       # 管理工具：import / sync / build-registry / validate
├── tests/         # 自动化测试（占位，后续补全）
├── docs/          # 设计与维护文档
├── examples/      # 完整使用示例
├── archive/       # 暂未纳入核心的第三方/历史资产（不进 registry）
└── .github/       # CI 工作流（占位，后续补全）
```

## 三类资产

| 类型 | 定义 | 关键文件 | bucket |
|---|---|---|---|
| **Skill** | 某项任务具体怎么做 | `SKILL.md`（frontmatter 为权威元数据） | `skills/<id>/` |
| **Expert** | 由谁思考/判断/执行，用哪些技能 | `.codebuddy-plugin/plugin.json` + `agents/<id>.md` | `experts/<id>/` |
| **Team** | 多专家如何分工协作交付 | 同上 + `settings.json` + 多个 `agents/*.md` | `teams/<id>/` |

每个资产根目录可附加一个 hub 专用的 `manifest.yaml`（由脚本自动生成），用于索引、筛选、引用检查。
**资产的权威定义始终是 WorkBuddy 原生文件**；manifest 只是派生元数据。详见 `docs/workbuddy-compatibility.md`。

## 日常操作

```bash
# 导入一个新资产（zip 或已解压目录），自动识别类型并放入对应 bucket
python scripts/import_asset.py path/to/asset.zip
python scripts/import_asset.py path/to/asset-dir

# 生成 / 刷新所有资产的 manifest.yaml
python scripts/sync_manifests.py            # 只补缺的
python scripts/sync_manifests.py --force    # 全量刷新

# 生成全局索引 registry/*.yaml（含引用完整性检查）
python scripts/build_registry.py

# 校验所有资产格式与结构
python scripts/validate.py

# 安装脚本依赖（首次）
pip install -r scripts/requirements.txt
```

## 资产现状

运行 `python scripts/build_registry.py` 查看最新清单。当前核心资产见 `registry/` 与 `docs/operations/` 中的上架指引。

## 远程仓库

本仓库对应的 GitHub 远程：`https://github.com/airen/workbuddy-hub.git`
（本地提交后，由维护者手动 `git push` 到该 remote。）
