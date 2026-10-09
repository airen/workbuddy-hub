---
name: react-best-practices
display_name: React 与 Next.js 工程实践
display_name_en: React Best Practices
description: "Applies Vercel and React official engineering practices to React and Next.js code: server/client component boundaries, data fetching placement, caching and revalidation, bundle size, types and error boundaries. Use when migrating to Next.js, cleaning up a legacy frontend, or onboarding new contributors to one shared style."
category: development-tools
version: 1.0.0
author: 大漠
---

# React 与 Next.js 工程实践

把 React 与 Next.js 的官方与 Vercel 实践落到代码里，让团队按同一套方式写前端。

## 适用场景

- 迁移到 Next.js（App Router）
- 整理老项目，收敛写法
- 新成员需要一套统一规范
- 页面变慢、打包体积变大，需要定位写法层面的原因

## 输入

- 项目的技术栈版本（React / Next.js 版本、路由方式）
- 组件或页面的现有实现
- 性能与体积目标（有的话）

## 执行步骤

### 步骤 1 — 先确认版本与路由方式

App Router 与 Pages Router 的实践差异很大。动手前先确认：项目用的是哪个、React 是哪个大版本、有没有开启相关实验特性。

**不确定就先读 `package.json` 和目录结构，不要凭印象。**

### 步骤 2 — 划清服务端与客户端边界

默认写服务端组件。只有以下情况才加 `'use client'`：

- 用到状态、生命周期、事件处理
- 用到浏览器 API（localStorage、window、IntersectionObserver）
- 用到依赖上述能力的第三方库

**把 `'use client'` 放在尽可能深的叶子节点。**在页面顶部加一次，整棵子树都被拖到客户端。

### 步骤 3 — 数据获取放对位置

| 场景 | 做法 |
|---|---|
| 服务端渲染取数 | 在服务端组件里直接 await，不要绕一层 API 路由 |
| 需要缓存 | 用 fetch 的缓存选项或框架提供的缓存机制，明确设置再验证策略 |
| 需要更新 | 用 revalidation 或按需失效，不靠刷新页面 |
| 客户端交互取数 | 用带状态管理的请求库，处理加载与错误态 |

避免：在客户端组件里请求自己的 API 路由来拿本可在服务端直接取的数据（多一跳网络往返）。

### 步骤 4 — 控制打包体积

- 大依赖动态引入（`dynamic import`），不要进首屏包
- 图标库按需引入，不整体导入
- 检查是否有重复版本的同一依赖

### 步骤 5 — 类型与错误边界

- 组件 props 有明确类型，不用 `any`
- 页面级有错误边界与加载态
- 异步操作的错误被显式处理，不静默吞掉

### 步骤 6 — 逐项核对清单

改完后按这张表自查：

- [ ] `'use client'` 只出现在必要的叶子组件
- [ ] 数据获取在服务端完成，无多余的自我请求
- [ ] 缓存与重验证策略是显式设置的，不是默认值碰运气
- [ ] 无整体导入的大依赖
- [ ] props 有类型，无 `any`
- [ ] 有加载态与错误态
- [ ] 列表渲染有稳定 key

## 输出

- 改动清单（文件 + 改了什么 + 为什么）
- 自查表逐项结论
- 未验证项标注（尤其是版本相关的行为）

## 反模式

- **整个页面标 `'use client'`**：把不需要客户端的部分也拖下水
- **凭印象写框架行为**：版本差异会导致建议完全错误，不确定先查官方文档并标注
- **客户端请求自己的 API 路由**：多一跳网络往返，且丢失服务端直取的能力
- **默认相信缓存默认值**：不同版本的默认缓存行为变过多次，必须显式设置
- **为了规范一次性大改**：按模块渐进改造，每步可回退
- **不测就宣称性能优化**：优化必须有效果测量，否则只是改动

## 参考

- React 官方文档：https://react.dev
- Next.js 官方文档：https://nextjs.org/docs
