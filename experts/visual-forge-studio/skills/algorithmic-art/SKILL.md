---
name: algorithmic-art
display_name: 生成艺术
display_name_en: Algorithmic Art
description: "Creates algorithm-driven graphics and visual effects with p5.js: generative patterns, particle systems, flow fields and animated visuals driven by parameters rather than hand-drawn frames. Use when visuals need to be produced by code — backgrounds, generative covers, data-driven art or motion experiments."
category: design-tools
version: 1.0.0
author: 大漠
---

# 生成艺术

用 p5.js 做由算法驱动的图形和视觉效果。

> 生成艺术的价值在于**参数可控**：改一个数就能得到一整个系列，而不是逐张手画。

## 适用场景

- 生成式背景、封面、壁纸
- 粒子系统与流场效果
- 数据驱动的视觉化图形
- 需要批量产出且风格统一的视觉素材

## 输入

- 想要的视觉方向（气质、参考、用途）
- 输出形态：静态图 / 动效 / 可交互
- 约束：尺寸、时长、性能目标（要不要在移动端跑）

## 执行步骤

### 步骤 1 — 定视觉规则

先用一句话说清规则，再写代码。例：

- "从画布中心向外扩散的粒子，速度随距离衰减"
- "按噪声场流动的线条，颜色随位置在两套色之间渐变"

规则说不清，写出来的代码只会是一堆随机数的堆砌。

### 步骤 2 — 选算法骨架

| 想要的效果 | 常用做法 |
|---|---|
| 有序的重复图案 | 循环 + 参数化变换（旋转、缩放、偏移） |
| 有机流动感 | 噪声场（Perlin / Simplex）+ 粒子跟随 |
| 聚集 / 分散 | 力导向、吸引子、排斥规则 |
| 生长感 | 分形、L-system、递归分支 |
| 渐变与融合 | 颜色插值 + 混合模式 |

### 步骤 3 — 参数化

把所有关键变量提到顶部：数量、速度、衰减、色相范围、随机种子。

**固定随机种子**，否则每次刷新都不一样，无法复现和挑选。

### 步骤 4 — 配色

从主题系统取色，或在两个锚点色之间插值。避免全色相随机——那会得到"彩虹噪声"，不是设计。

### 步骤 5 — 性能与输出

- 静态图：画够帧数后导出图片
- 动效：控制帧率与粒子数量，移动端要降规格
- 检查：粒子数翻十倍时会不会卡？容器尺寸变化时会不会错位？

### 步骤 6 — 产出系列

用同一套参数模板 + 不同种子 / 少量参数变化，产出一个系列。记录每版的参数，方便复现。

## 输出

- 可运行的代码（含参数区与随机种子）
- 成品图或动效文件
- 参数记录（哪张图用了哪组参数）

## 反模式

- **规则不清就写随机数**：结果是噪声，不是设计
- **不固定种子**：无法复现，挑好的那张再也找不回来
- **全色相随机**：视觉上会变成彩虹噪声
- **粒子数不设上限**：浏览器直接卡死
- **不考虑容器尺寸变化**：换个屏幕就错位
- **只给代码不给成品**：需求方要的是图，不是让他自己去跑代码

## 参考

- p5.js：https://p5js.org
- 配色用 `theme-factory`；需要批量产出静态图时配合 `image-optimizer` 压体积。
是缩略图

## 参考

- 需要真实质感图片时用 `image-generation`；出图后用 `image-optimizer` 压体积。
