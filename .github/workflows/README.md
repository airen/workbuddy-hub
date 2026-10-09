# GitHub Actions 工作流

本目录规划 CI 自动化（当前阶段为占位，尚未启用）：

- `validate.yml`：PR 自动校验。在 `ubuntu-latest` 上安装 `scripts/requirements.txt`，运行
  `python scripts/sync_manifests.py`、`python scripts/build_registry.py`、`python scripts/validate.py`，
  任一失败则阻断合并。
- `release.yml`：版本发布。打 tag 时生成 `registry/` 快照并（可选地）调用打包逻辑产出可上传 zip。

启用方式：把上述两个 `.yml` 文件放入本目录，并在仓库 Settings → Actions 中开启。

> 注意：CI 中运行脚本需要 Python 3.11+ 与 `pyyaml`、`jsonschema`（见 `scripts/requirements.txt`）。
