---
name: recipe-by-ingredient
display_name: 按食材找菜谱与采购清单
display_name_en: Recipe by Ingredient
description: "Given what's in the fridge, matches Chinese home-cooking recipes from a bundled dataset, recommends dishes you can cook now, and produces a shopping list of missing ingredients. Use when the user asks 'what to cook', lists fridge ingredients, or wants a shopping list."
category: other
version: 1.0.0
author: 大漠
---

# 按食材找菜谱与采购清单

对应开源项目 Jiayu-zheng1/EveryDay_Food 的核心能力：冰箱里有食材却不知道做什么？按食材搜中文菜谱，选好菜还能生成购物清单。这里把"搜菜谱 + 出采购单"做成一个**数据驱动**的技能，离线可用。

## 输入

- 用户冰箱 / 现有食材（原话或列表）
- 可选：想做的菜数、忌口（不吃辣 / 素食 / 过敏）、偏好（快手 / 下饭 / 硬菜）

## 执行步骤

### 1. 整理现有食材
把用户给的食材归一化成"词条"（去量词、去"一点/几个"等修饰，保留核心名词，如"两个番茄"→"番茄"）。记为一个集合 `have`。

### 2. 读取数据集并匹配
读取 `references/recipes.json`（`recipes` 数组）。对每道菜：
- `missing = 菜.ingredients − have`（常备调料油盐酱醋糖葱姜蒜等默认已有，不计入缺料；只有 `ingredients` 与特殊调料如豆瓣酱/可乐/咖喱块才计缺）
- 若 `missing` 为空 → 标 **"现在就能做"**
- 若 `missing` 长度为 1–2 → 标 **"差一点"**
- 若 `missing` 更长 → 标 **"缺料较多"**（一般不主动推荐，除非用户要凑数）

### 3. 排序与筛选
1. 先列所有"现在就能做"的，按 tags 贴近用户偏好（快手/下饭/素食/硬菜）优先
2. 再列"差一点"的，作为可顺手补齐的选项
3. 若用户给了忌口（如"不吃辣"），过滤掉 tags 含 微辣/川菜 且明显辣的菜；素食则只留 素 标签菜
4. 默认推荐 3–5 道，别一次铺 20 道

### 4. 出采购清单
让用户从"差一点"的菜里挑想做的，或直接对全部推荐菜取并集：
`shopping = union(各推荐菜的 missing)`
去重后列成清单，按"生鲜 / 调料"大致分组（简单分即可）。

### 5. 交付
- **聊天内直接给**：推荐菜（菜名 + 一句话做法要点）+ 采购清单
- **用户要可保存的清单时**：把采购清单写成 Markdown 文件（如 `采购清单.md`），或按用户要求格式输出。无需生成 HTML，纯文字清单最实用。

## 输出格式（示例）

```
冰箱里现在有：鸡蛋、番茄、青椒、豆腐、一块排骨

今晚能做（现在就开火）
1. 番茄炒蛋 — 番茄炒出汁，回锅鸡蛋，少许糖
2. 青椒炒蛋 — 鸡蛋炒散，下青椒丝快炒
3. 家常豆腐 — 豆腐煎黄，下青椒木耳，生抽蚝油焖

差一点就能做（补 1–2 样）
- 青椒肉丝：还差 猪肉丝
- 麻婆豆腐：还差 猪肉末、豆瓣酱

采购清单
- 生鲜：猪肉丝（或肉末）1 份
- 调料：豆瓣酱 1 瓶
```

## 内容边界

- 菜谱来自内置数据集，非实时联网；若用户要更细做法，可基于 `steps` 展开，但标注"家常做法，按口味调整"
- 不声称"营养配比""热量"，除非用户要且明确是估算
- 数据集可在 `references/recipes.json` 自行增删，新增菜照结构加一条即可
- 不做医疗/食疗断言（如"番茄防癌"），只讲做法
