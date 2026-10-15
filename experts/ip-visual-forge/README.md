# 颜定 · 角色 IP 视觉统筹（ip-visual-forge）

> 从一张照片或一句人设开始，建立可复用角色档案，再按文章、场景或平台产出风格统一的配图与图解。

**不想真人出镜，也可以用角色建立个人品牌。** 难点不在画得好看，在于**换一篇文章、换一个场景，读者还能认出同一个「你」**。颜定就是为这件事存在的：先把角色固定下来，再让内容去变。

## 这个专家解决什么

| 问题 | 颜定怎么做 |
|---|---|
| 「我有张自拍，但不知道从哪开始」 | 先建档：把照片收敛成 3–5 个不可漂移的识别锚点，再出确认图与三视图 |
| 「我只有一句人设」 | 从零设计：角色设定表 → 视觉规范 → 表情系统 → 品牌物料提示词 |
| 「我要一个头像 / Logo」 | 极简方形标识：3 个方向 × 6 张候选，保证缩到 32×32 还认得出来 |
| 「这篇文章想配图」 | 先确认角色，再按文章内容设计场景图，并给出建议插入位置 |
| 「我想跨文章跨平台一直用」 | 建立/复用角色档案，把视觉规范、动作库、封面、内容配图放进同一套流程 |
| 「想让角色替我讲流程讲知识」 | 让人物通过动作、位置和道具参与图解：知识卡、方法步骤、PPT 演讲页 |
| 「整篇长文要一套统一视觉」 | 统筹封面、方形缩略图、正文论证图，并精确到「插在这句话之后」 |

## 七条路线，按用途选

**不用七条都走。先决定：这个角色现在要替你做什么。**

| 路线 | 技能 | 什么时候走它 | 主产出 |
|---|---|---|---|
| ① 建档 | `comic-ip-onboarder` | 已经有照片 / 玩偶 / 手办 / 头像 / 吉祥物 | `IP_DNA.md` + 正面全身确认图 + 三视图 + 8 张表情动作图 |
| ② 从零设计 | `ip-character-designer` | 只有一句人设或品牌定位 | 角色设定表 + 视觉规范 + 表情系统 + 物料提示词 |
| ③ 头像 / Logo | `ip-as-logo` | 只要一个方形标识，强调缩小后仍可辨识 | 3 个方向 + 6 张 1:1 候选 |
| ④ 文章配图 | `punk-ip-article-illustrations` | 有真人照片，想直接做到文章配图；或用内置角色 Punk | 角色包（draft→confirmed）+ 正文插图 + 插入位置 |
| ⑤ 长期复用 | `lz-ip-illustration` | 跨文章、跨平台长期复用：封面、正文图、小红书卡片、动图 | `ip-profile.md` + `visual-spec.md` + `prompt-pack.md` + `action-library.md` |
| ⑥ 角色图解 | `ip-diagram-creator` | 想让角色替你讲流程、讲知识 | 三张角色固定资产 + 长文配图 / 知识卡 / 方法拆解图 / PPT 页面 |
| ⑦ 长文统一视觉 | `editorial-ip-visuals` | 一整篇文章视觉统一，且要精确插入位置 | 横版封面 + 1:1 缩略图 + 3–4 张 16:9 正文图 + 插入定位表 |

七条路线之上的总调度在 `ip-visual-router`：它负责三问定界（谁 / 干什么 / 出到哪）、
按「你手上现在有什么」选路线、锁定角色契约，并在四条不同档案格式之间做互认与交接。

## 一致性契约（这个专家的核心）

选定路线后，**生成任何内容图之前**，必须先固定四件东西：

1. **角色参考图**——一张被用户明确确认过的全身/主锚图，之后每一张生成都重新附上它。
2. **视觉规范**——配色锚点、线条风格、材质、头身比、背景规则。**即使带了参考图，也要在提示词里用文字重申**：参考图管身份，文字管规则。
3. **识别锚点**——3–5 个「以后绝对不能漂移」的特征。
4. **禁区**——不能变的项，以及不能借用的东西（其他 IP 的外貌、照片原始背景、水印、文字）。

然后每一张图都过两道闸门：

- **生成前**：参考图已作为图像参考输入？视觉规范已用文字重申？本张只解释一个锚点？角色参与核心动作？图内文字已确认？提示词已存档？
- **生成后**：还是同一个人吗？明显沿用了参考图吗？配色/线条/材质/头身比一致吗？文字准确可读吗？误借别的 IP 了吗？角色抢走内容信息了吗？

**参考图只在第一张传，是角色失守的头号原因。**

## 快速开始

```text
我只有一张自拍，想做一个能长期复用的文章配图角色
把这篇文章做成一套统一视觉：封面 + 1:1 缩略图 + 正文论证图
用我的角色做几张知识图解，把一个方法论讲清楚
```

## 包内结构

```text
ip-visual-forge/
├── .codebuddy-plugin/plugin.json
├── agents/ip-visual-forge.md              # 颜定（本包新写）
├── skills/
│   ├── ip-visual-router/                  # 总入口与调度层（本包新写）
│   ├── comic-ip-onboarder/                # ← irenerachel/comic-ip-onboarder-skill
│   ├── ip-character-designer/             # ← Beatatata/ip-character-designer (MIT)
│   ├── ip-as-logo/                        # ← s1dashu/ip-as-logo-skill (MIT)
│   ├── punk-ip-article-illustrations/     # ← adrianpunk/punk-ip-illustrations (个人非商业)
│   ├── lz-ip-illustration/                # ← xing006/lz-ip-illustration
│   ├── ip-diagram-creator/                # ← haloshin/ip-diagram-creator (MIT)
│   └── editorial-ip-visuals/              # ← zaoshangduziteng/Editorial-IP-Visuals
├── avatars/ip-visual-forge.jpg
├── LICENSE                                # 许可与归属（含各上游全文与限制说明）
├── manifest.yaml
└── README.md
```

## 来源与许可

本专家包 = **本包新写的编排层**（`plugin.json` / `agents/` / `skills/ip-visual-router/` /
`README.md` / `avatars/` / `LICENSE`）+ **原样搬运的上游技能内容**（7 个 `skills/*/`）。

上游技能正文**逐字保留**，仅做了两类技术性追加：给缺失的 `SKILL.md` frontmatter 补
`version` 与 `category`；把包内技能目录名对齐 frontmatter 的 `name`。详见 `LICENSE`。

⚠️ **许可状态并不统一，公开分发或商用前请先读 `LICENSE`**：

- **MIT（可自由使用）**：`ip-character-designer`、`ip-as-logo`、`ip-diagram-creator`
- **个人非商业免费，商用需授权付费**：`punk-ip-article-illustrations`
  （Adrian Punk，Punk IP Illustrations Personal Use License 1.0）
- **上游未声明许可（默认保留所有权利）**：`comic-ip-onboarder`、`lz-ip-illustration`、
  `editorial-ip-visuals`
