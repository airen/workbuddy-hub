# HTML 报告格式（HTML Report Format）

架构评审渲染成操作系统临时目录里的一个自包含 HTML 文件。Tailwind 和 Mermaid 都来自 CDN。Mermaid 可靠地处理图形状的图示；亲手搭的 div 和内联 SVG 处理更有编辑感的视觉（质量图、剖面图）。把两者混着用：别什么都靠 Mermaid，它很快会显得千篇一律。

## 骨架（Scaffold）

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 页眉（Header）

仓库名、日期，以及一份紧凑的图例：实心框 = module，虚线 = seam，红箭头 = leakage，深色粗框 = deep module。不要引言段落。直接进入候选。

## 候选卡片（Candidate card）

图示承担重量。文字稀疏、平实，使用术语表里的词（来自 `codebase-design` 技能），不加修饰。

每个候选是一个 `<article>`：

- **Title**：短，点出这次深化（例如「Collapse the Order intake pipeline」）。
- **Badge row**：推荐强度（`Strong` = emerald，`Worth exploring` = amber，`Speculative` = slate），再加一个依赖类别的标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **Files**：等宽字体列表，`font-mono text-sm`。
- **Before / After diagram**：核心看点。两栏，并排。见下面的模式。
- **Problem**：一句话。哪里疼。
- **Solution**：一句话。会改什么。
- **Wins**：要点列表，每条 ≤6 个词。例如「Tests hit one interface」「Pricing logic stops leaking」「Delete 4 shallow wrappers」。
- **ADR callout**（如适用）：琥珀色底的框里一行字。

不要成段的解释。如果一个图示需要一段话才能看懂，就重画那个图示。

## 图示模式（Diagram patterns）

挑一个适合这个候选的模式。混着用。别让每个图示都长一个样。多样性正是重点的一部分。

### Mermaid 图（依赖 / 调用流的主力）

当要点是「X 调 Y、Y 调 Z，看看这团乱麻」时，用一个 Mermaid `flowchart` 或 `graph`。把它包进一张 Tailwind 样式的卡片里，免得显得像空降进来的。用 classDef 把泄漏边染红、把深模块染深。时序图很适合表达「前：6 次往返；后：1 次」。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手搭的方框与箭头（当 Mermaid 的布局跟你打架时）

模块用带边框和标签的 `<div>`。箭头用内联 SVG 的 `<line>` 或 `<path>`，绝对定位在一个 relative 容器上。当你希望「后」这张图感觉像一个大粗框的深模块、内部灰掉时，就用它——Mermaid 渲染不出那种正确的分量感。

### 剖面图（适合分层的「浅」）

堆叠水平的色带（`h-12 border-l-4`），展示一次调用穿过的各层。前：6 层薄薄的、每层什么也不干。后：1 条厚带，标注合并后的职责。

### 质量图（适合「接口和实现一样宽」）

每个模块两个矩形：一个代表接口的表面积，一个代表实现。前：接口矩形几乎和实现矩形一样高（浅）。后：接口矩形短，实现矩形高（深）。

### 调用图折叠（Call-graph collapse）

前：一棵函数调用树，渲染成嵌套的方框。后：同一棵树塌缩成一个方框，那些如今变成内部的调用在它里面以淡色显示。

## 样式指引（Style guidance）

- 偏编辑感，不要企业仪表盘。留白慷慨。标题可选衬线（`font-serif` 跟 stone/slate 很搭）。
- 颜色克制：一个强调色（emerald 或 indigo），加上红用于泄漏、琥珀用于警告。
- 图示高度保持 ~320px，好让前/后并排坐下、不用滚动。
- 图示里的模块标签用 `text-xs uppercase tracking-wider`，让它们读起来像示意图，而不是 UI。
- 唯一的脚本是 Tailwind CDN 和 Mermaid ESM import。报告除此之外是静态的：没有应用代码，除了 Mermaid 自身的渲染之外没有交互。

## Top recommendation 小节

一张更大的卡片。候选名、一句话说明为什么、一个指向它卡片的锚点链接。就这些。

## 语气（Tone）

平实的英语，简洁，但架构名词和动词直接来自 `codebase-design` 技能。简洁不是漂移的借口。

**只准用：** module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**绝不替换成：** component、service、unit（用来指 module 时）· API、signature（用来指 interface 时）· boundary（用来指 seam 时）· layer、wrapper（当你想说 module 时）。

**符合这种风格的措辞：**

- "Order intake module is shallow: interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins 要点**用术语表的词来命名收益：*"locality: bugs concentrate in one module"*、*"leverage: one interface, N call sites"*、*"interface shrinks; implementation absorbs the wrappers"*。不要写 *"easier to maintain"* 或 *"cleaner code"*，因为那些词不在术语表里、也不配占位置。

不要含糊其辞，不要清嗓子，不要「值得注意的是……」。一句话如果可以被写成要点，就写成要点。一个要点如果可以被删掉，就删掉。一个词如果不在 `codebase-design` 的术语表里，先去找一个在里面的，再考虑造新词。
