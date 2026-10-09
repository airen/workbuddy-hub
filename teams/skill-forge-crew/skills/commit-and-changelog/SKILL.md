---
name: commit-and-changelog
display_name: 提交说明与更新日志
display_name_en: Commit and Changelog
description: "Reads the staged diff and writes a Conventional Commits message with type, scope and body; then turns commit history into a changelog in either a user-readable or a developer-technical register. Use when a commit message needs writing, when preparing a release, or when summarizing a period of progress."
category: development-tools
version: 1.0.0
author: 大漠
---

# 提交说明与更新日志

让每次提交都解释得清楚，让每个版本都交代得明白。

## 适用场景

- 改完代码，不知道这次提交该怎么概括
- 发布前需要一份更新日志（给用户看，或给开发看）
- 阶段性汇报，需要把一堆提交整理成人能读的进展
- 提交历史混乱，需要回填规范化的说明

## 输入

- 暂存区的 diff（提交说明场景）
- 提交范围（更新日志场景）：两个 tag 之间、某个时间点之后、或某个作者的全部提交
- 目标读者：用户 / 开发 / 两者都要

## 执行步骤

### 第一部分 — 写提交说明

#### 步骤 1 — 读真实的 diff

只基于 `git diff --staged` 的实际改动写。不读 diff 就写提交说明，等于编故事。

#### 步骤 2 — 判断类型

| 类型 | 用于 |
|---|---|
| `feat` | 新功能、新能力 |
| `fix` | 修复缺陷 |
| `refactor` | 重构，既不新增功能也不修 Bug |
| `perf` | 性能改进 |
| `docs` | 只改文档 |
| `test` | 只改测试 |
| `chore` | 构建、依赖、工具配置 |
| `revert` | 回滚此前的提交 |

一次提交只用一个类型。**混着改就拆成两次提交**，不要写 `feat: 加功能并修了个 Bug`。

#### 步骤 3 — 确定范围

范围写被改动影响最大的模块名（如 `auth`、`api`、`web`），不要用笼统的 `misc`。

#### 步骤 4 — 写正文

格式：

```
<type>(<scope>): <一句话摘要>

<为什么改（可选，说明动机）>

<影响面 / 破坏性变更（有就写）>
```

摘要用祈使句、不加句号、控制在 50 字符左右。破坏性变更在正文里以 `BREAKING CHANGE:` 开头单独写。

好例子：
```
fix(api): 修复分页参数越界时返回空列表的问题

offset 超过总数时原逻辑返回空数组而非 422，客户端误判为"没有数据"。
```

坏例子：
```
fix: 修了点东西
```

### 第二部分 — 整理更新日志

#### 步骤 5 — 取提交范围

明确区间：`git log v1.2.0..v1.3.0`，或从上次发布的 tag 到 HEAD。**区间要先跟用户确认**，不要用默认值蒙。

#### 步骤 6 — 按类型归类

把提交按 feat / fix / perf / refactor / 其他归类，合并同类项（五个 `fix` 如果都是同一个模块，合成一条）。

#### 步骤 7 — 选语域

| 语域 | 写法 |
|---|---|
| 用户版 | 说"你能用到什么、变了什么"，不提内部模块名、不提重构 |
| 技术版 | 保留模块名、PR 编号、破坏性变更和迁移指引 |

#### 步骤 8 — 标注破坏性变更

任何需要用户改代码 / 改配置的变化，单独放最前面一节，写明：**变了什么、为什么要变、怎么迁移。**

## 输出

- 提交说明：`<type>(<scope>): <摘要>` + 可选正文
- 更新日志：按版本或时间段组织，分「新增 / 修复 / 变更 / 破坏性变更」几节

## 反模式

- **不读 diff 就写**：凭印象写的提交说明会与实际改动不符
- **一次提交混多个类型**：让回滚变得不可能
- **摘要写得太长**：超过 72 字符在大部分工具里会被截断
- **更新日志照抄提交记录**：未经合并归类的提交列表对用户毫无价值
- **把重构写进用户版日志**：用户不关心内部结构调整
- **破坏性变更埋在正文里**：必须单独成节并给迁移指引

## 参考

- Conventional Commits 规范：https://www.conventionalcommits.org
