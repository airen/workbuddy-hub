# 复刻机（replica-machine）

把「参考品」变成「自己的东西」：**REA 负责看清，WorkBuddy 负责写出来，主理人负责需求与交付，独立验证员负责比对。**

> 素材来源：结合开源逆向工程 MCP **REA**（`github.com/morluto/rea`，MIT）的网站/Electron 分析能力与 WorkBuddy 自身的编码能力，封装成一条可复用的复刻流水线。

## 它解决什么

看到一个好用的网站或功能，想弄清它怎么实现的、再照着做一个——难点从来不是"写代码"，而是**先看清**：

- 它的页面结构长什么样？
- 一次点击背后发了哪些请求、由哪段脚本发起？
- 数据怎么被组装、界面怎么变？

猜出来的复刻品经不起第二次点击。复刻机把这件事拆成四个角色，各管一段，中间用证据串起来。

## 团队成员

| 成员 | 名字 | 职责 | 持有技能 |
|---|---|---|---|
| 主理人 | 柯复刻 | 需求定界、授权把关、编排调度、交付裁决 | replica-delivery、replica-blueprint |
| 逆向侦察分析师 | 甄探源 | 用 REA 侦察页面结构 / 脚本 / 交互 / 网络请求，产出证据包与拆解清单 | rea-recon、replica-blueprint |
| 复刻实现工程师 | 程一码 | 把证据包转成实现蓝图，按蓝图复刻实现、薄切片推进 | replica-blueprint、replica-build |
| 一致性验证员 | 严较真 | 拿复刻品与参考站逐项比对（视觉 / 交互 / 网络 / IPC），产出差异报告 | replica-parity-check |

## 内置技能（5 个）

- `rea-recon` — REA 逆向侦察（MCP 配置、网站与 Electron 两类目标的采集、证据标准、降级通道）
- `replica-blueprint` — 把侦察证据转成可施工的实现蓝图
- `replica-build` — 按蓝图复刻实现，薄切片推进与自测留证
- `replica-parity-check` — 四轴一致性比对与差异报告
- `replica-delivery` — 需求定界、授权把关、验收标准、交付报告

## 前置：装好 REA

REA 以 MCP 服务形态接入。WorkBuddy 侧的配置写在 `~/.workbuddy-ai/mcp.json`：

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

写入后到 WorkBuddy 的「自定义连接器」入口点一次「信任」，再**重启客户端**。也可以用 `npx rea-agents@latest setup` 自动注册。详见 `skills/rea-recon/references/rea-mcp-setup.md`。

> 环境要求：Node.js 22（≥22.19）/ 24（≥24.11）/ 26+；网站分析需 Chrome 系浏览器。REA 不可用时，`rea-recon` 提供了 DevTools / Playwright 降级通道。

## 典型用法

```
复刻这个网站：先用 REA 研究它的页面结构、脚本和网络请求，再照着实现一个
研究这个站的某个功能是怎么实现的：它发了哪些请求、脚本怎么写的
把复刻品和参考站逐项比对，看视觉、交互和网络还差在哪
```

## 工作流

| Workflow | 触发 | 编排 |
|---|---|---|
| A 完整复刻 | 给参考站要成品 | 定界 → 侦察 → 蓝图 → 实现 → 验证 → 修复 → 交付 |
| B 只做侦察 | 「这功能怎么实现的」 | 定界 → 侦察（甄探源单跑） |
| C 只做验证 | 「比一比差在哪」 | 严较真单跑 → 差异报告 |
| D 疑难排查 | 行为对不上 | 补侦察定位 → 修复 → 复验 |

## 门禁

| 门禁 | 位置 | 规则 |
|---|---|---|
| G0 | 定界 → 侦察 | 没有授权依据或范围无法界定，不启动 |
| G1 | 侦察 → 蓝图 | 证据包缺关键证据或以推测为主，回炉补侦察 |
| G2 | 蓝图 → 实现 | 存在无法绕开的阻塞性未知项，回炉补侦察 |
| G3 | 每个切片 | 没有运行证据，不进下一个切片 |
| G4 | 验证 → 交付 | 存在未解决的阻断级差异，不放行 |

## 合规

复刻只针对**自有、已获授权或开源许可**的目标。团队不使用参考站受版权保护的图片、字体、图标与文案；素材逐项替换并记入交付报告。授权存疑时先问，不"先做了再说"。详见 `skills/replica-delivery/references/legal-boundary.md`。

## 上架信息

- 类型：专家团（`expertType: team`）
- 平台类目：`02-Engineering`
- 打包：`python scripts/package.py teams/replica-machine` → `build/replica-machine.zip`

## 许可

MIT
