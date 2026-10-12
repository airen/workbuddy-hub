# 后期插图路线

> 本专家的首期目标是**图文排版**。插图是**后续能力**——但路线现在就要定死，免得跑偏。

## 一、总原则：矢量优先，不用生图

| 方案 | 采用 | 理由 |
|---|---|---|
| **手写 SVG 插图** | ✅ 首选 | 可控、可复现、体积小、风格统一 |
| **CSS 图形**（色块/线条/网格/几何） | ✅ 首选 | 零依赖，与排版同源 |
| **图标字体 / 开源 SVG 图标集** | ✅ 可用 | 需确认授权并落本地 |
| 生图模型出插画 | ❌ **不用** | 违反本专家的定义性约束 |

**为什么坚持不用生图做插图**：一旦插图来自生图，就回到了"字不可控、改不了、套图不统一"的老问题。插图的风格必须和排版一致，而生图做不到。

## 二、CSS 图形的四种原子

插图的 90% 可以用这四样拼出来：

### 1. 色块

```css
.ill-block{width:120px;height:120px;background:var(--accent)}
```

### 2. 圆 / 半圆

```css
.ill-circle{width:96px;height:96px;border-radius:50%;background:var(--accent)}
.ill-half{width:120px;height:60px;border-radius:60px 60px 0 0;background:var(--ink)}
```

### 3. 线条 / 折线

```css
.ill-line{height:2px;background:var(--ink);width:100%}
.ill-stroke{fill:none;stroke:var(--ink);stroke-width:3}
```

### 4. 网格 / 点阵

```css
.ill-grid{
  background-image:
    linear-gradient(var(--rule) 1px, transparent 1px),
    linear-gradient(90deg, var(--rule) 1px, transparent 1px);
  background-size:32px 32px;
}
.ill-dots{background-image:radial-gradient(var(--rule) 1.5px, transparent 1.5px);background-size:20px 20px}
```

## 三、SVG 插图规范

内联 SVG，不要外链 `.svg` 文件（保持单文件）。

```html
<svg viewBox="0 0 200 160" width="200" height="160" aria-hidden="true">
  <rect x="10" y="90" width="40" height="60" fill="var(--accent)"/>
  <rect x="70" y="50" width="40" height="100" fill="var(--ink)"/>
  <rect x="130" y="20" width="40" height="130" fill="var(--accent)"/>
  <line x1="0" y1="152" x2="200" y2="152" stroke="var(--ink)" stroke-width="2"/>
</svg>
```

**规范**：
- `viewBox` 必须有，宽高比正确
- 颜色走 `var(--...)`，不写死
- 加 `aria-hidden="true"`（装饰性图形不朗读）
- 线条用 `stroke`，填充用 `fill`，不要混用
- **不用渐变、不用阴影、不用滤镜**（与两套视觉系统都不搭）

## 四、风格纪律

插图必须服从当前视觉系统：

| | Editorial | Swiss |
|---|---|---|
| 形状 | 有机、手绘感、略不规则 | 几何、直角、精确 |
| 线宽 | 2–3 px，可有粗细变化 | 1–2 px，恒定 |
| 颜色 | 单色或双色，低饱和 | 单锚点色 + 黑白灰 |
| 密度 | 稀疏，留白多 | 网格化，可密 |
| 禁忌 | 卡通表情、emoji 风 | 圆角、渐变、拟物 |

## 五、什么时候该加插图

| 场景 | 加插图吗 |
|---|---|
| 抽象概念需要可视化（如"可维护性"） | ✅ 加 |
| 数据关系（趋势、占比、对比） | ✅ 加（但用图表，不是插画） |
| 步骤流程 | ✅ 加（流程示意） |
| 纯观点阐述 | ❌ 不加，留白更有力 |
| 已经有照片 | ❌ 不叠加 |
| 内容本身已经够满 | ❌ 不加 |

**判据**：插图要**替代一段说明文字**，而不是**填充一段空白**。

## 六、Roadmap（后期能力，本期不做）

按优先级：

1. **矢量插图库**：沉淀 20–30 个常用 SVG 图形原子（箭头、流程节点、图标、人物剪影）
2. **故事型模板**：把「一个主题」扩写成有起承转合的整套图文（配合 `tuwen-storytelling`）
3. **朋友圈 / 知乎问答模板**：新的出口与版式骨架
4. **图表组件化**：把 KPI 塔、横条图、折线、环形做成可直接调的组件
5. **动态卡**：CSS 动画 + 多帧导出（**不使用视频生图**）

## 七、自检

- [ ] 插图是 SVG / CSS 做的，不是生图
- [ ] 颜色走变量
- [ ] 风格与当前视觉系统一致
- [ ] 插图替代了文字，而不是填充空白
- [ ] 没有渐变、阴影、滤镜
- [ ] 没有 emoji 风
