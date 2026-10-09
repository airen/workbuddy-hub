# 新建资产模板

本目录提供三类资产的「从零新建」脚手架。hub 内的资产**直接采用 WorkBuddy 官方打包格式**，
外加一个 hub 专用的 `manifest.yaml` 做索引/筛选元数据。

| 模板 | 用途 | 关键文件 |
|---|---|---|
| `templates/skill/` | 新建技能 | `SKILL.md`（frontmatter 即权威元数据） |
| `templates/expert/` | 新建单专家 | `.codebuddy-plugin/plugin.json` + `agents/<id>.md` + `manifest.yaml` |
| `templates/team/` | 新建专家团 | `.codebuddy-plugin/plugin.json` + `settings.json` + `agents/*.md` + `manifest.yaml` |

## 使用方式

```bash
# 1. 复制模板到对应 bucket
cp -r templates/expert   experts/my-new-expert
# 2. 把占位 id（your-expert-id 等）全局替换为真实 kebab-case ID
# 3. 填写 plugin.json、agents/<id>.md、SKILL.md 正文
# 4. 生成 hub 元数据并校验
python scripts/sync_manifests.py --force
python scripts/build_registry.py
python scripts/validate.py
```

> `manifest.yaml` 不需要手写维护——`sync_manifests.py` 会从 plugin.json / SKILL.md 自动推导生成。
> 详见 `docs/workbuddy-compatibility.md`。
