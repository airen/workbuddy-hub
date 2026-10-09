---
name: image-optimizer
display_name: 图片优化
display_name_en: Image Optimizer
description: "Resizes images, converts them to WebP and trims file weight so pages load faster, while preserving visual quality and the original file. Use before putting images on the web, when a page is heavy, or when a batch of assets needs standardising."
category: design-tools
version: 1.0.0
author: 大漠
---

# 图片优化

调整图片尺寸，转换为 WebP，减少网页图片带来的加载负担。

## 适用场景

- 图片要放到网页上
- 页面加载慢，图片占大头
- 一批素材需要统一尺寸与格式
- 生成的图体积过大

## 输入

- 待处理图片
- 展示尺寸（实际渲染的像素尺寸，不是屏幕尺寸）
- 质量要求：可接受的最大体积、是否需要透明通道

## 执行步骤

### 步骤 1 — 先确认真实展示尺寸

看图在页面里**实际渲染多大**（考虑响应式与高清屏），按这个尺寸的 1.5～2 倍输出。

例：页面里显示为 400px 宽，输出 800px 宽就够。输出 4000px 是纯浪费。

### 步骤 2 — 备份原图

**先备份再处理。**优化后的图无法还原细节，需要返工改尺寸时原图是唯一退路。

### 步骤 3 — 选格式

| 场景 | 格式 |
|---|---|
| 照片、渐变丰富的图 | WebP（或 AVIF，若目标环境支持） |
| 需要透明通道 | WebP（保留 alpha）或 PNG |
| 简单图标、单色图形 | SVG（可无损缩放且体积极小） |
| 必须兼容极老环境 | 保留 JPEG / PNG 兜底 |

给出 WebP 时，保留一份原格式兜底，并在页面里用 `<picture>` 或等效方式提供回退。

### 步骤 4 — 压质量参数

从默认质量开始，逐步下调，直到**肉眼可见画质下降**就回退一档。不要为了数字好看压到明显模糊。

判断标准：把压缩后的图放在实际展示尺寸下看，不是放大看。

### 步骤 5 — 批量处理与命名

批量时统一命名规则（如 `name@2x.webp`），并记录每类图的输出参数，保持一致性。

### 步骤 6 — 验证结果

- [ ] 在实际展示尺寸下画质可接受
- [ ] 体积相比原图有明显下降（记录前后数字）
- [ ] 透明通道（如需）保留正确
- [ ] 格式回退方案已就位
- [ ] 原图备份存在

## 输出

- 优化后的图片文件
- 前后体积对比记录
- 所用参数（尺寸、格式、质量）
- 回退方案说明

## 反模式

- **不备份就覆盖原图**：需要更大尺寸时无法还原
- **按原图尺寸输出**：页面只显示 400px 却输出 4000px
- **压到明显模糊换取体积**：用户看到的是糊图
- **只给 WebP 不给回退**：老环境直接开天窗
- **图标也用位图**：SVG 更小且清晰
- **不记录参数**：下次处理同一批图会得出不同结果

## 参考

- 优化前的图片可能来自 `image-generation` 或 `canvas-design`。
