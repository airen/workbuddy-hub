---
name: rea-recon
display_name: REA 逆向侦察
display_name_en: REA Recon
description: "Drives REA, the reverse-engineering MCP, to inspect a reference website or Electron app without source: page structure, loaded scripts and their source, the network requests behind each interaction, and per-request screenshots. Covers install/registration, the capture workflow for both web and Electron targets, a fallback channel when REA is unavailable, and the evidence standard every finding must meet."
category: development-tools
version: 1.0.0
author: 大漠
---

# REA 逆向侦察

用 REA 把参考目标"看穿"：它有哪些页面、加载了哪些脚本、一次交互背后发了什么请求、数据怎么被组装。全程本机分析，不需要源码。

> 一条结论要么能指向捕获到的请求 / 脚本 / 截图，要么就归进"未知项"。没有第三种。

## 适用场景

- 要复刻一个网站，先得弄清它的页面结构、脚本与网络行为
- 想搞清某个功能"是怎么实现的"（点了什么、发了什么请求、数据怎么变）
- 目标是没有源码的 Electron / 打包应用
- 需要为后续视觉 / 网络比对留下可核验的基线

## 前置：让 REA 可用

**环境要求**：Node.js 22（≥22.19）/ 24（≥24.11）/ 26+，以及 npm。网站分析需要 Chrome 系浏览器；静态 JavaScript 分析不需要原生引擎（Hopper / Ghidra / IDA 只在深度原生二进制分析时才需要）。

**注册方式**（二选一）：

1. **自动**：`npx rea-agents@latest setup`，选择客户端、审阅计划并批准，它会注册 MCP 服务并安装配套调查指引，完成后重启客户端。
2. **手动**：把下面这段并入 WorkBuddy 的 MCP 配置 `~/.workbuddy-ai/mcp.json` 的 `mcpServers`：

```json
{
  "mcpServers": {
    "rea": {
      "command": "npx",
      "args": ["-y", "rea-agents@latest", "mcp"]
    }
  }
}
```

需要可复现安装时，把 `rea-agents@latest` 换成钉死的 `rea-agents@<版本>`。

> 手动写入后 MCP 不会自动生效：到 WorkBuddy 的「自定义连接器」入口点一次「信任」，再重启客户端。更新用 `rea update`（npm 全局安装）或 `npx rea-agents@latest setup`（npx 方式）。

**就绪检查**：先跑一次 `npx -y rea-agents@latest --help` 确认可执行；需要时用 `doctor` 类命令诊断具体目标类型。

## 采集流程

### A. 网站目标

**1. 用远程调试端口打开目标页**（独立的浏览器配置，避免污染日常浏览器）：

```bash
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/rea-recon-browser \
  "<目标页面 URL>"
```

macOS / Windows 上用已安装浏览器的可执行路径。REA 会连上这个浏览器，你可以手动操作页面。

**2. 找到页面目标 ID**：

```bash
npx -y rea-agents@latest list-browser-targets http://127.0.0.1:9222 --json
```

在返回列表里选 URL 匹配的目标，记下它的 `TARGET_ID`。

**3. 开一个观察窗口，执行交互，读结果**：

```bash
npx -y rea-agents@latest inspect-web-page \
  http://127.0.0.1:9222 <TARGET_ID> \
  --observation-ms 10000 \
  --include-accessibility-text \
  --include-json-body-shapes --json
```

命令连接后，**在浏览器里执行你要研究的操作**（如点击按钮）。窗口结束后返回：所选页面、该窗口内的网络活动、JSON 响应形状、可访问性文本。

**4. 读脚本源码，找到请求的发起者**：

```bash
npx -y rea-agents@latest inspect-web-page \
  http://127.0.0.1:9222 <TARGET_ID> \
  --include-script-sources --json
```

从请求记录里读"发起者"（是哪个脚本发起的），再读该脚本源码，弄清数据从哪来、怎么被组装、怎么改变 DOM。

> 一次观察窗口之外的请求不在结果里。要研究多个交互，就**一个交互开一个窗口**，分别采集。

**5. 截图**：按请求 / 按关键状态各留一张，供后续视觉比对。

### B. Electron / 打包应用目标

静态分析读文件、不运行应用：

```bash
npx -y rea-agents@latest analyze-javascript-application /absolute/path/to/app --json
```

结果包含模块、导入关系、Electron 边界及相关证据。沿"按钮 → preload API → IPC 通道 → 主进程"追踪一条功能链路，把跨进程的每一跳都记进证据包。

## 降级通道（REA 不可用时）

REA 装不上、目标不被支持或环境受限时，退到通用通道，但**必须在证据包里显式标注本次用的是降级通道**：

- **Chrome DevTools 协议**：连远程调试端口，用 Network 域抓请求、用 Debugger / Runtime 域读脚本与 DOM。
- **Playwright / 浏览器自动化**：脚本化打开页面、监听 `request` / `response`、导出 HAR、截图。

降级通道的证据要同样满足下面的证据标准；两者的差距（如拿不到 JSON body 形状）要在"采集通道与限制"一节写明。

## 证据标准

每条关于参考站行为的结论，必须满足其一：

| 结论类型 | 需要的证据 |
|---|---|
| "页面结构是这样" | DOM 层次 / 路由 / 可访问性文本的捕获片段 |
| "它发了这个请求" | 请求记录：URL、方法、状态、响应结构、触发时机 |
| "这个交互会怎样" | 一次观察窗口内的交互 → 请求 → DOM 变化的对应记录 |
| "这段脚本做了 X" | 脚本源码片段 + 行号/位置引用 |
| "Electron 里走了这条链路" | 模块 / 导入 / IPC 通道 / 进程边界的证据 |

**不满足上述任一条件的，只能写成"推测（待验证）"或归入未知项清单**，不得与事实混排。

## 输出：证据包

按 `references/evidence-pack-template.md` 的结构产出，七节齐全：目标与范围、页面/模块清单、交互→请求→脚本对照表、数据契约、素材与资产清单、未知项清单、采集通道与限制。

## 注意事项

- **只分析有权分析的目标**。授权依据缺失时先回问，不自行开工。
- **REA 在本机分析**，但工具结果会交给智能体，其模型提供方有自己的数据政策；涉及敏感目标时先与用户确认。
- 结果包含支撑结论的证据与**限制**，照实转述限制，不把"没观察到"写成"不存在"。
- 遇到错误先更新 REA（`rea update` / `npx rea-agents@latest setup`）再重试。

## 参考

- `references/rea-mcp-setup.md` — WorkBuddy 侧 REA MCP 配置与排障
- `references/web-recon-playbook.md` — 网站目标的采集清单
- `references/electron-recon-playbook.md` — Electron 目标的采集清单
- `references/evidence-pack-template.md` — 证据包模板
