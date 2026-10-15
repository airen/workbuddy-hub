# Comic IP Onboarder Skill

把照片、头像、毛绒玩具、手办、品牌吉祥物或角色设定，转成可复用漫画 IP 档案的 AI Agent Skill。

这个 skill 适合用来做新角色入驻：先提取稳定的身份锚点，再生成正面全身确认图、三视图、表情动作参考包，并整理成可交给下游漫画信息图工作流继续使用的 `IP_DNA.md`。

## 适合场景

- 把真人照片转成风格化漫画角色档案
- 把玩偶、头像、手办或吉祥物做成可复用 IP
- 为一个新角色建立 `IP_DNA.md`
- 生成正面全身确认图、三视图和 8 张独立表情动作参考图
- 把确认后的角色档案交给下游漫画信息图、文章配图或视觉内容工作流使用

## 核心原则

- 第一张确认图必须是完整全身角色，即使原始素材只有头像或半身。
- 表情动作包必须基于用户确认过的三视图生成，不能只靠文字描述重画。
- 表情动作包固定为 8 张独立单张图片，禁止先生成合集、九宫格或拼贴图再切分。
- 所有提示词默认使用中文。
- 只复用目标风格的分析结构和质检纪律，不复制任何既有 IP 的外貌细节。
- 最终图片必须走图像生成或图像编辑路线，不能用 HTML、SVG、canvas、网页截图或幻灯片截图伪装。

## 仓库结构

```text
.
├── README.md
├── SKILL.md
└── references/
    └── IP_DNA_TEMPLATE.md
```

- `SKILL.md`：主流程说明，包含触发条件、工作流、质检规则和阶段推进话术。
- `references/IP_DNA_TEMPLATE.md`：创建新 IP 档案时使用的模板。

## 使用方式

把这个仓库作为 skill 安装或复制到支持 skills 的 agent 环境中，保持下面的目录结构：

```text
comic-ip-onboarder/
├── SKILL.md
└── references/
    └── IP_DNA_TEMPLATE.md
```

常用调用方式：

```text
调用 comic-ip-onboarder，把这张图做成可复用漫画 IP。先输出 IP_DNA 草案和第一张正面全身纯色确认图提示词，所有提示词都用中文。
```

```text
调用 comic-ip-onboarder，基于已确认的三视图继续生成这个 IP 的表情动作参考包。必须生成 8 张独立单张图片，不要生成合集再切分。
```

## 输出结果

一个完整 IP 档案通常包含：

```text
ip-profiles/<profile-id>/
├── IP_DNA.md
├── front-full-body.png
├── three-view.png
├── expressions/
│   ├── 01-*.png
│   ├── 02-*.png
│   ├── ...
│   └── 08-*.png
└── companion/
    ├── companion-DNA.md
    └── companion-three-view.png
```

其中 `IP_DNA.md` 是最核心的交接文件，图片资产只有在用户确认通过后才进入最终档案。

## 隐私说明

本仓库只包含通用 skill 流程和模板，不包含用户照片、角色资产、私有项目路径、账号信息、接口密钥或生成图片。
