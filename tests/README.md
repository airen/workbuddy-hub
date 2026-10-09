# 自动化测试

本目录用于回归测试 hub 的管理工具与资产契约。

当前阶段（核心骨架）尚未编写 pytest 用例；资产与索引的正确性通过以下脚本保证：

- `scripts/validate.py`：按 `schemas/*.json` 校验每个资产的 `manifest.yaml`，并做结构检查（SKILL.md / plugin.json / agents/ 齐备）。
- `scripts/build_registry.py`：聚合索引并做引用完整性检查（专家→技能、团队→成员）。

计划补充（后续）：

- `tests/test_schemas.py`：对 `schemas/*.json` 做自我校验，确保示例 manifest 能通过。
- `tests/test_references.py`：校验 registry 中专家/团队的引用都能解析，无悬空 ID。
- `tests/fixtures/`：存放用于测试的样例 manifest / 资产片段。

运行：

```bash
pip install -r scripts/requirements.txt pytest
pytest tests/
```
