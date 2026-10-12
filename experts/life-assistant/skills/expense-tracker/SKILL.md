---
name: expense-tracker
display_name: 记账本 · 钱花哪了
display_name_en: Expense Tracker
description: "Generates a downloadable, offline expense tracker (index.html) that logs income/expense by account and category, shows spending charts, and stores data locally with CSV export/import. Use when the user wants to track spending, see where money went, or keep a personal ledger."
category: other
version: 1.0.0
author: 大漠
---

# 记账本 · 钱花哪了

对应开源项目 lexical-yoda/ExpenseTracker 的核心能力：月底想知道钱花哪了？自己部署这本账，按账户、分类记收支，用图表看开销。原项目把交易数据存在 Excel 文件里；这里改成**零依赖的离线网页**，双击即开，数据存浏览器本地，并可导出 CSV 在 Excel 里打开，兼顾"能看图"和"不折腾部署"。

## 输入

- 用户是否要长期记账（默认是，直接生成工具）
- 想记哪些账户 / 分类（无则使用内置默认：账户 现金/银行卡/支付宝/微信/信用卡，分类 餐饮/交通/购物/居住/娱乐/医疗/工资/其他）

## 执行步骤

### 1. 生成工具
1. 读取 `references/expense-tracker.html`（纯前端、零依赖、已含图表与 CSV 导入导出）
2. 若用户有自定义账户/分类，改 `accounts`/`categories` 相关 `select` 选项即可；否则原样交付
3. 写入用户工作区，命名为 `记账本.html`
4. `present_files` 交付，说明双击打开即用、数据存本地

### 2. 收尾提示
- 数据全在浏览器 `localStorage`，换设备/清缓存前点"导出 CSV"备份；CSV 可直接用 Excel 打开
- "导入 CSV"可把备份或别处数据合并进来（表头：日期,类型,分类,账户,金额,备注）
- 图表为分类支出条形图 + 各账户余额小计，月度可切换查看
- 金额为粗略记录，仅作回顾，非税务/理财依据

## 内容边界

- 只做记录与回顾，不做理财建议、不分析"该不该花"
- 不联网、不收集数据、不要 API key
- 不声称数据能跨设备自动同步（本地方案做不到，需用导出/导入手动迁移）
