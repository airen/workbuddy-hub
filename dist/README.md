# WorkBuddy Hub - 上传包说明

本目录包含所有可上传到 open.workbuddy.cn 平台的资产包。

## 📦 资产清单

### 专家（10 个）

| 文件名 | 名称 | 大小 | 状态 |
|--------|------|------|------|
| `agent-memory-advisor.zip` | 智能体记忆选型顾问 | 680KB | ✅ 已验证 |
| `diagram-architect.zip` | 江图南·图表架构师 | 3.1MB | ✅ 已验证 |
| `doc-memory-steward.zip` | 纪文远·项目文档管家 | 447KB | ✅ 已验证 |
| `eng-workflow-coach.zip` | 工程流程教练 | 410KB | ✅ 已验证 |
| `engineering-review-board.zip` | 陆鉴·工程评审总监 | 1.4MB | ✅ 已验证 |
| `lao-dao-editor.zip` | 老刀·资深编辑 | 441KB | ✅ 已验证 |
| `ppt-architect.zip` | 林镜·PPT 架构师 | 258KB | ✅ 已验证（已修复） |
| `self-media-studio.zip` | 柳成文·自媒体内容总监 | 203KB | ✅ 已验证 |
| `software-architect.zip` | 方权衡·软件架构师 | 511KB | ✅ 已验证 |
| `spec-driven-dev.zip` | 章立言·规格驱动开发教练 | 456KB | ✅ 已验证 |

### 专家团（5 个）

| 文件名 | 名称 | 大小 |
|--------|------|------|
| `creator-ops.zip` | 创作运营团队 | 2.2MB |
| `deep-research-crew.zip` | 深度调研团队 | 842KB |
| `engineering-delivery.zip` | 工程交付团队 | 893KB |
| `hai-stack.zip` | Hai Stack 团队 | 3.5MB |
| `media-content-team.zip` | 媒体内容团队 | 6.6MB |

### 技能（32 个）

见上方专家/专家团引用的技能包。

---

## 🚀 上传步骤

### 1. 单个上传

```bash
# 上传专家
# 打开 https://open.workbuddy.cn
# 选择「上传专家」，上传对应的 .zip 文件

# 例如：
# 上传 ppt-architect.zip
```

### 2. 批量上传

```bash
# 上传整体资产包
# 打开 https://open.workbuddy.cn
# 选择「上传专家团」，上传 workbuddy-hub-assets.zip
```

---

## ✅ 平台校验规则

上传前会自动验证以下规则：

1. **必填字段**
   - `name` - 资产唯一标识
   - `displayName.zh/en` - 显示名称
   - `profession.zh/en` - 专业领域
   - `displayDescription.zh/en` - 功能描述

2. **一致性校验**
   - `defaultInitPrompt.zh` 必须与 `quickPrompts[0].zh` 完全一致
   - `defaultInitPrompt.en` 必须与 `quickPrompts[0].en` 完全一致

3. **文件格式**
   - 必须是合法的 JSON
   - 编码必须是 UTF-8

---

## 🔧 重新打包

如需重新打包所有资产：

```bash
cd /path/to/workbuddy-hub
python3 scripts/package_upload.py
```

---

## 📝 修改资产后重新上传

1. 修改源文件（如 `experts/ppt-architect/.codebuddy-plugin/plugin.json`）
2. 运行验证脚本确认无误：
   ```bash
   python3 scripts/validate_upload.py
   ```
3. 重新打包：
   ```bash
   python3 scripts/package_upload.py
   ```
4. 上传新的 zip 文件到平台

---

## 📊 统计信息

- **专家数**: 10
- **专家团数**: 5
- **技能数**: 32
- **总压缩包数**: 47
- **总大小**: 约 23MB

---

最后更新：2026-10-09
