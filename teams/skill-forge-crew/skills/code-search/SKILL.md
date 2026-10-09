---
name: code-search
display_name: 代码定位检索
display_name_en: Code Search
description: "Locates code fast in large repositories using ripgrep for text and ast-grep for structure: symbols, error strings, call sites, and syntax patterns. Use before reading a big repo, when finding where something is defined or used, or when preparing a change whose blast radius is unknown."
category: development-tools
version: 1.0.0
author: 大漠
---

# 代码定位检索

在大型代码库里快速找到要读、要改的地方。

> 先定位，再读。整仓通读是上下文最贵的用法。

## 适用场景

- 刚接手一个陌生仓库，需要找某功能在哪
- 改一个东西前要确认影响面（谁在调用）
- 报错信息来自哪里
- 要找出所有符合某种写法的地方（比如所有 `any`、所有直接操作 DOM 的地方）

## 输入

- 要找什么：符号名 / 错误串 / 文件路径 / 写法模式
- 搜索范围（全仓 / 某个目录 / 排除测试）
- 环境里有哪些工具可用（ripgrep、ast-grep、或编辑器的搜索能力）

## 执行步骤

### 步骤 1 — 先确认工具可用性

不要假设工具存在。先检查环境里有没有 `rg`、`ast-grep`，没有就用可用的替代（如内置搜索工具）。**工具不存在时明确告诉用户，不要假装跑过。**

### 步骤 2 — 按线索类型选搜法

| 要找的东西 | 怎么搜 |
|---|---|
| 一个符号的定义 | 搜 `fn <name>` / `class <name>` / `const <name>` |
| 一个符号的所有引用 | 搜符号名，再用文件类型过滤 |
| 一段错误文案的来源 | 直接搜文案原文（去掉变量部分） |
| 某类写法 | 用语法搜索（ast-grep），不要靠正则硬凑 |
| 配置文件在哪 | 按文件名搜，不按内容搜 |

### 步骤 3 — 先窄后宽

第一次搜索限定范围：指定目录、指定文件后缀、排除 `node_modules` / `dist` / `vendor`。搜不到再放宽，不要一上来就全仓搜——结果太多等于没搜。

- **排除凭据文件**：`.env*`、`.npmrc`、`.direnv`、`*.pem`、`*.key`、`*.p12`、证书，以及任何含 `credentials` / `secret` / `token` 的配置文件，默认排除在检索范围外。确需检索时只输出**文件路径 + 行号**，不输出整行原文。

### 步骤 4 — 用语法搜索找"写法"

文本搜索找不到结构。要找"所有awaited 但没有 try 包裹的调用""所有类组件""所有 `useEffect` 依赖数组为空"，用语法搜索匹配语法节点，而不是正则猜缩进。

### 步骤 5 — 收敛到具体位置

拿到候选后：

1. 按路径判断是不是目标模块（排除测试、示例、生成代码）
2. 排除明显不相关的（第三方包、构建产物）
3. 剩下的按相关度排序，**只读前几个**

### 步骤 6 — 记录影响面

改之前把调用点列出来：直接调用方、间接依赖方、测试。这份列表就是改动的 blast radius。

## 输出

- 命中的位置清单（文件:行号）
- 排除掉的干扰项及原因
- 影响面评估（谁会受改动影响）
- **脱敏约定**：命中行若含疑似密钥 / 令牌 / 凭据，引用时用 `<已脱敏>` 占位并注明文件与行号，**不把真实值写进任何报告或转发消息**

## 反模式

- **整仓读一遍再动手**：上下文被无关代码吃光
- **第一次就全仓搜**：结果几百条，等于没搜
- **用正则硬凑结构**：缩进、换行一变就失效，该用语法搜索
- **不排除生成代码**：`dist`、`vendor`、锁文件里的命中全是噪音
- **假设工具存在**：没检查就宣称搜过，是编造结果
- **只看第一个命中**：同名符号在不同模块语义可能完全不同

## 参考

- ripgrep：https://github.com/BurntSushi/ripgrep
- ast-grep：https://ast-grep.github.io
