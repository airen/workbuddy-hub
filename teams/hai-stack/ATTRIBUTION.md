# 署名与许可（Attribution & License）

本专家包（「软件迭代专家团」）是 [hai-stack](https://github.com/hylarucoder/hai-stack) 方法论在 WorkBuddy 上的封装。

## 上游来源

- **项目**：hai-stack
- **作者**：[@hylarucoder（海拉鲁编程客）](https://github.com/hylarucoder)
- **仓库**：https://github.com/hylarucoder/hai-stack
- **许可证**：CC BY-NC 4.0（署名—非商业性使用 4.0 国际）
- **许可证全文**：https://creativecommons.org/licenses/by-nc/4.0/legalcode
- **版权**：Copyright (c) 2026 hylarucoder

## 本包做了什么改动

1. **编排层**：新增主理人与六名成员的角色定义（`agents/`）、`plugin.json` 展示字段、`settings.json`、本 README 与头像。这部分是本次封装新增的内容。
2. **技能层**：`skills/` 下的 19 个技能**原样复制**自上游仓库，保留原始 `SKILL.md`、中文版 `SKILL.zh_CN.md`、`references/`、`scripts/`、`assets/` 与 `LICENSE`。
   - 唯一的删减：移除了每个技能目录下的 `agents/openai.yaml`（面向其他 Agent 平台的接口声明，WorkBuddy 不使用）。

## 使用条件（CC BY-NC 4.0）

你可以自由地：

- **共享** — 以任何媒介或格式复制和分发本材料
- **演绎** — 修改、转换和基于本材料进行创作

但须遵守以下条款：

- **署名** — 你必须给出适当的署名、提供许可证链接，并说明是否作了修改。
- **非商业性使用** — 你**不得**将本材料用于商业目的。

无附加限制 — 你不得适用法律条款或技术措施，从法律上限制他人做许可证允许的事。

## 商业用途

**商业用途需要单独授权，请联系原作者。**

个人使用、学习、研究与非商业项目可以直接使用；公开发布衍生作品时，请注明来源。

## 第三方许可

`skills/code-review-and-quality/` 改编自 Addy Osmani 的 [agent-skills](https://github.com/addyosmani/agent-skills)，保留其原始 **MIT** 许可证。详见该目录下的 `LICENSE`。
