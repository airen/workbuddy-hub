# REA MCP 配置（WorkBuddy 侧）

REA 以 MCP 服务形态接入智能体。WorkBuddy 侧的配置文件是：

```
~/.workbuddy-ai/mcp.json
```

> 注意文件名是 `mcp.json`，**不是** `.mcp.json`（带点前缀的那个）。

## 一、写入配置

把 `rea` 合并进 `mcpServers`（**不要覆盖已有服务**）：

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

需要可复现安装时，钉死版本：

```json
"args": ["-y", "rea-agents@1.2.3", "mcp"]
```

## 二、生效步骤

1. 写入配置后，MCP **不会自动生效**。
2. 打开 WorkBuddy 的「自定义连接器」入口（连接器管理页右上角），对新增的 `rea` 服务点一次「信任」。
3. **重启 WorkBuddy 客户端**，让它重新扫描 MCP 配置。

## 三、环境要求

| 项 | 要求 |
|---|---|
| Node.js | 22（≥22.19）/ 24（≥24.11）/ 26+ |
| npm | 需要 |
| 浏览器 | 网站分析需 Chrome 系浏览器 |
| 原生引擎 | 仅深度二进制分析需要 Hopper / Ghidra / IDA；静态 JS / .NET 不需要 |

## 四、替代路径：自动 setup

不用手改 JSON，也可以跑：

```bash
npx rea-agents@latest setup
```

它会让选择客户端、审阅计划并批准，随后注册 MCP 服务与配套调查指引，并备份已有配置。完成后重启客户端。

## 五、更新

- npm 全局安装：`rea update`（若装过 `npm install --global rea-agents`）
- npx 方式：`npx rea-agents@latest setup`

更新后按提示重启客户端。

## 六、排障

| 现象 | 处理 |
|---|---|
| MCP 服务不出现 | 确认写的是 `~/.workbuddy-ai/mcp.json`（无点前缀）；确认点过「信任」并重启过客户端 |
| `npx` 拉不到包 | 确认 Node 版本满足要求；确认网络可访问 npm registry |
| 连不上浏览器目标 | 确认浏览器用 `--remote-debugging-port` 启动且端口一致；确认 `list-browser-targets` 能列出目标 |
| 网站目标结果为空 | 确认目标 URL 在浏览器里已打开；确认观察窗口时长够覆盖操作 |
| 行为异常 | 先更新 REA 再重试；仍不行则提交 issue，附版本、目标类型、复现步骤与错误输出 |

## 七、合规提示

- REA 为合法的逆向工程研究、分析与重建提供工具；使用者有责任取得所需授权并遵守适用法律。
- 分析在本机运行，但工具结果会交给智能体，其模型提供方有自己的数据政策。
