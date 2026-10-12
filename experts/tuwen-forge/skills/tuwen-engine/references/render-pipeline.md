# 渲染管线 · HTML/CSS → Playwright → PNG

## 一、为什么是这条路

| 方案 | 结论 |
|---|---|
| **单文件 HTML + CSS → Playwright 截图** | ✅ **唯一路线** |
| Markdown → 图片 | ❌ 版式能力太弱 |
| 生图模型 | ❌ 本专家定义性禁止 |
| canvas 手绘全部文字 | ❌ 中文排版要自己实现断行/避头尾，成本极高且不稳 |
| 前端构建链（Vite/Webpack） | ❌ 引入不必要的依赖 |

理由：HTML + CSS 是**文本**，Agent 能直接写、读、改、验证；CSS Grid + 严格字号/留白，版式精度远超 Markdown；产物是**确定性**的——同输入同输出，可回归测试。

## 二、渲染链路

```
index.html（单文件，含 N 个 <section class="poster">）
        │
        ▼
Playwright 载入 file:// URL
        │
        ├─ 等 document.fonts.ready   ← 必须，否则中文可能未就绪就截图
        │
        ▼
逐个 .poster 元素截图（element.screenshot）
        │
        ▼
output/<data-name>.png
```

## 三、浏览器解析顺序

`render.cjs` 按下面的顺序尝试，第一个成功的就用：

1. **系统 Google Chrome**（`channel: 'chrome'`）← **本机实测可用**
2. 系统 Microsoft Edge（`channel: 'msedge'`）
3. Playwright 自带 chromium

**都必须带 `--no-sandbox --disable-dev-shm-usage`。** 受管沙箱里不带这两个参数会启动失败：

```
browserType.launch: Target page, context or browser has been closed
（或）sandbox initialization failed: Operation not permitted
```

> 实测记录（2026-10-12）：`channel: 'chrome'` + `--no-sandbox` → 1080×1440 截图成功，69.8 KB。
> Playwright 自带 chromium 因版本不匹配（本机缓存 1148，`playwright-core` 期望 1243）**不可用**——
> 所以**优先走系统 Chrome**，不要依赖自带 chromium。

## 四、playwright 模块怎么找

`render.cjs` / `verify.cjs` 依次尝试：

1. 环境变量 `PLAYWRIGHT_PATH` 指向的目录
2. 脚本相对路径 `../../../node_modules`、`../../node_modules`
3. `NODE_PATH` 里的各段
4. 托管工作区默认路径 `~/.workbuddy-ai/binaries/node/workspace/node_modules`
5. 全局 `node_modules`

⚠️ **必须用 CommonJS `require()` 或 `createRequire`**：ESM 的 `import` **不认 `NODE_PATH`**，
会直接报 `ERR_MODULE_NOT_FOUND`。脚本一律写成 `.cjs`。

## 五、字体栈

模板里已写死 macOS 优先的栈，不要改：

```css
/* Editorial 衬线 */
--font-serif: "Songti SC", "STSong", "Noto Serif SC", "Source Han Serif SC", Georgia, serif;
/* 通用无衬线（Swiss / 正文） */
--font-sans: "PingFang SC", "Hiragino Sans GB", "Helvetica Neue", "Noto Sans SC", system-ui, sans-serif;
/* 数字/等宽（数据卡） */
--font-mono: "SF Mono", "JetBrains Mono", "Menlo", monospace;
```

- **渲染前 `await document.fonts.ready`**：否则可能出现「文字已排好但字体还没换过来」的截图。
- **缺字必须显式失败**：如果页面里出现 `□` 或空白，说明字体栈没覆盖到，**不许交付**，先补字体栈或换字。
- 需要网络字体时**先下载到本地**再 `@font-face` 引入，不要依赖渲染时联网。

## 六、截图参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `deviceScaleFactor` | `1` | `--scale 2` 可出 2x |
| `type` | `png` | 不要用 jpeg（文字边缘会有压缩噪点） |
| 截图对象 | `.poster` 元素 | **不要截全页**，否则会带上页面背景与其它画板 |
| 视口 | `2200 × 1600` | 只影响布局初值，**不决定出图尺寸**——截图取的是元素自身盒子 |
| 等待 | `load` + `fonts.ready` | 再加 100 ms 稳定帧 |

**视口为什么是 2200×1600**：最宽的画板是 2100 px，`body` 左右各 48 px 内边距 → 需要 2196 px，取 2200 留余量。
**长图不会被截断**：元素截图取的是元素盒子，超出视口的部分照样输出。实测 `.poster.long` 6412 px @1x
（视口的 4 倍）、12824 px @2x 均完整出图，与 `platform-specs.md` 声明的 1080×auto 一致。

**日志报的是输出像素**，不是画板尺寸：

```
  ✓ 01-cover.png   1080×1440 @1x   69.8 KB   [3:4]
  ✓ L-long.png     2160×12824 @2x（画板 1080×6412）   178.4 KB   [long]
```

## 七、失败兜底

浏览器起不来时，**不要假装出了图**。按顺序做：

1. 报告具体错误（哪一步、什么消息）
2. 给出手动渲染路径：把 `index.html` 交给用户在浏览器里打开，用打印/截图导出
3. 至少交付 **HTML 源文件**，并说明「图没渲出来，但源文件可直接打开」
4. 在交付说明里写明「本次未成功渲染」

## 八、渲染前自检（脚本已内置）

- [ ] `index.html` 存在且能被浏览器解析（无未闭合标签）
- [ ] 至少有一个 `.poster`
- [ ] 每个 `.poster` 有 `data-theme`
- [ ] 没有引用外部 CSS/JS 文件（必须单文件）
- [ ] 引用的本地图片路径存在
