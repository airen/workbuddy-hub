---
name: workout-log
display_name: 训练记录 · 练了多重
display_name_en: Workout Log
description: "Generates a downloadable, offline workout logger (index.html) that records sets, reps and weight per exercise, compares against the previous session, and includes an inter-set rest timer with a beep. Use when the user wants to log training, track progress, or notes 'last time I lifted X'."
category: other
version: 1.0.0
author: 大漠
---

# 训练记录 · 练了多重

对应开源项目 tonybenoy/treening 的核心能力：上次练了多重又忘了？记录组数、次数和重量，对照上次训练，还带组间休息计时。这里做成一个离线网页，双击即开，数据存浏览器本地。

## 输入

- 用户是否要长期记录训练（默认是，直接生成工具）
- 常练的动作（可选，用于表单自动补全；无则用户自己填）

## 执行步骤

### 1. 生成工具
1. 读取 `references/workout-log.html`（纯前端、含对照上次与休息计时、无外部依赖）
2. 写入用户工作区，命名为 `训练记录.html`
3. `present_files` 交付，说明双击打开即用、数据存本地

### 2. 收尾提示
- 每次训练：填日期 → 逐个加动作（动作 / 组数 / 次数 / 重量）→ "保存本次训练"
- 加动作时自动显示**上次同动作**的记录，方便对照进步
- "复制上次动作"一键把上一场训练的动作搬进来，只改重量/次数
- **组间休息计时**：设好秒数点"开始"，归零时浏览器响三声提示（无需联网/权限）
- 数据在浏览器 `localStorage`，换设备/清缓存前点"导出备份"存一份 JSON

## 内容边界

- 只记录与对照，不做训练计划编排、不评估动作标准、不替代教练
- 不声称"该举多重/该不该加重量"，那是专业教练的事
- 不联网、不收集数据、不要 API key
