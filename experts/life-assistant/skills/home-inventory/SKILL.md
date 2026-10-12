---
name: home-inventory
display_name: 家当清单 · 东西放哪了
display_name_en: Home Inventory
description: "Generates a downloadable, offline home inventory (index.html) that records items with photo, room and location, plus warranty dates and invoice notes, with search/filter and warranty reminders. Use when the user asks where something is stored, wants to catalog belongings, or track warranties/invoices."
category: other
version: 1.0.0
author: 大漠
---

# 家当清单 · 东西放哪了

对应开源项目 asdteke/HomeInventory 的核心能力：东西收起来就找不到？自己部署家庭物品清单，记录照片、房间和位置，连保修日期、发票资料也能一起记。这里做成一个离线网页，双击即开，数据存浏览器本地。

## 输入

- 用户是否要长期登记家当（默认是，直接生成工具）
- 搬家 / 大扫除 / 保修管理 / 找东西，哪种诉求更强（决定交付时强调哪块）

## 执行步骤

### 1. 生成工具
1. 读取 `references/home-inventory.html`（纯前端、照片自动压缩、无外部依赖）
2. 若用户有固定房间划分，可按需调整 `room` 下拉选项；否则原样交付
3. 写入用户工作区，命名为 `家当清单.html`
4. `present_files` 交付，说明双击打开即用、数据存本地

### 2. 收尾提示
- 每件可记：名称、房间、具体位置、数量、照片、购买日期、**保修到期**、发票/凭证/序列号
- 保修到期会自动提醒：30 天内标"即将到期"，已过标"已过保"
- 顶部搜索可按名称/位置/凭证检索；按房间筛选
- 数据在浏览器 `localStorage`，换设备/清缓存前点"导出备份"存一份 JSON（含照片）

## 内容边界

- 照片以 base64 存在本机，不上传任何服务器；多图会占本地空间，建议只拍关键凭证
- 不联网、不收集数据、不要 API key
- 保修日期仅为提醒，不构成法律/售后承诺，请以官方凭证为准
