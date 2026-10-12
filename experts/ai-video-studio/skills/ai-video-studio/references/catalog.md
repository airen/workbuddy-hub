# 视频制作 skill 完整目录（16 个）

数据来自一批 AI 视频 skill 的实测与作者原帖。星标为原帖标注（⭐），仅作热度参考。

> ⚠️ 安装命令与前置条件以各仓库最新 README 为准；下表为原素材记录，使用前请让用户确认。

---

## 一、风格化短片 · 不露脸也能出片

### ① huashu-art-motion ⭐3048
- **仓库**：https://github.com/alchaincyf/huashu-art-motion
- **作者**：花叔（alchaincyf）
- **做什么**：35 张样式卡（一张一个视觉风格）+ 9 套讲解语法。卡片管画面长什么样，语法管什么时候切、怎么切；同一段文案能出完全不同的片子。
- **安装**：`npx skills add https://github.com/alchaincyf/huashu-art-motion`
- **依赖**：`uv`、`ffmpeg`、`Playwright` 三样备齐，少一个都起不来。
- **注意**：35 张卡共用同一套构图；换卡换的是配色和质感，不是版式。想要另一种排版得自己改。
- **许可**：MIT

### ② vox-director ⭐2.2k
- **仓库**：https://github.com/Alisa0808/vox-director
- **做什么**：Vox 式解释性动画——一条主线、几个图形元素、一段旁白，把复杂的事拆开讲。不用真人出镜，靠节奏和信息密度。把解说稿交给 agent，画面自己长出来。
- **安装**：`npx skills add https://github.com/Alisa0808/vox-director`
- **依赖**：未标注特殊依赖（按 Vox 式生成，本地 agent 驱动）
- **许可**：MIT

### ③ hand-drawn-video-prompts ⭐253
- **仓库**：https://github.com/kaomei/hand-drawn-video-prompts
- **做什么**：商业手绘风（线条、留白、像人画其实提示词喂出来的）。把提示词按场景拆好，你不用从零想风格词。
- **安装**：`npx skills add https://github.com/kaomei/hand-drawn-video-prompts`
- **依赖**：无特殊标注
- **许可**：MIT

---

## 二、手作与漫画 · 看起来像人做的

### ④ stickman-video-director ⭐1645
- **仓库**：https://github.com/kaomei/stickman-video-director
- **做什么**：火柴人视频。本档里最省事的一条——**不用配任何 key、不用 MCP**，装完就能跑。
- **安装**：`npx skills add https://github.com/kaomei/stickman-video-director`
- **代价（烧钱）**：走 Google Flow，吃积分。**10 秒 720P 约 15 积分**；Google AI Pro 每月给 1000 积分，折合每月 19.99 美元。免费额度用完就得续。
- **许可**：MIT

### ⑤ kid-papercraft ⭐228
- **仓库**：https://github.com/kaomei/kid-papercraft
- **做什么**：萌宝纸艺生日祝福短片。流程短：问你 5 个问题 → 出 3 条 10 秒提示词。门槛低到几乎没有。
- **安装**：`npx skills add https://github.com/kaomei/kid-papercraft`
- **注意（⚠️）**：README 带**严格的非商业免责声明**。自己发着玩没事；接单、卖虚拟商品是另一回事，先看许可。
- **许可**：MIT（但 README 附加非商业免责，需额外确认）

### ⑥ hbg-classical-poem-silk-video ⭐362
- **仓库**：https://github.com/Mr-funny/hbg-classical-poem-silk-video
- **做什么**：古诗做成丝绸质感的短片（古诗词配画那一挂，画面走丝绸质感）。
- **安装**：跑一个 Docker 容器，里面是 `gemini-flow-suite`。
- **注意（⚠️）**：这个仓库**只有一个提交，非常新**。用着顺手就用，但别指望它长期有人维护。
- **许可**：MIT

### ⑦ hbg-life-simulation ⭐136
- **仓库**：https://github.com/Mr-funny/hbg-life-simulation
- **做什么**：同作者另一个，把长文案做成统一漫画 IP 的旁白视频。先锁一个漫画主角（年龄、脸型、发型、服装全定死，每张图都是同一个人——解决大多数 AI 视频「每帧换脸」的毛病）；往下是 Edge TTS 配连续旁白（默认 +0% 语速）、语义字幕按标点断句、静态漫画用 zoom/pan 交替推拉（普通镜头 4–8 秒）、固定音量 BGM；最后一道 MP4 质检（查黑帧、静音、响度）。
- **安装**：`npx skills add https://github.com/Mr-funny/hbg-life-simulation`
- **注意（⚠️）**：默认输出 **1920×1080 横屏**。发竖屏短视频记得改。
- **许可**：MIT

---

## 三、资讯与解说 · 把内容讲清楚

### ⑧ simon-skills ⭐382
- **仓库**：https://github.com/trustfuture/simon-skills
- **做什么**：新闻 / 资讯号那条线，三个 skill 打包——`investigation-video`（资讯短片）、`whiteboard-video`（白板讲解）、`video-common`（公共底座）。
- **安装**：`npx skills add https://github.com/trustfuture/simon-skills`
- **坑（⚠️）**：`video-common` 得跟另外两个放在**同一层目录**，不然另外两个找不到它。跑起来还要火山引擎的 TTS 环境；`Remotion` 和 `React` 的版本是**钉死的**，别自己升。
- **许可**：MIT

### ⑨ director ⭐793
- **仓库**：https://github.com/s1dashu/director
- **做什么**：科普号三档模式——动画解说 / 故事动画 / 剧情影像。先选模式再开工。命令行接的是 LibTV 和即梦，自己不出画面，靠这两个把手伸出去调。
- **安装**：`npx skills add https://github.com/s1dashu/director`
- **依赖**：LibTV CLI + 即梦账号
- **许可**：MIT

### ⑩ book-sales-video ⭐219
- **仓库**：https://github.com/Kianzzz/book-sales-video
- **做什么**：知识类带货，冲着图书带货去（走知识类内容变现）。输入一本书名，自动生成图书带货短视频。
- **安装**：`npx skills add https://github.com/Kianzzz/book-sales-video`
- **依赖（最多）**：**三个 key**——豆包 TTS、Pexels、WEREAD，外加一个**本地跑的 OpenChatCut MCP**。没有云端一键路径，本地环境得自己搭。想省事不是首选；想自己控流程，自由度更大。
- **许可**：MIT

---

## 四、图文与文本 skill（视频的上游）

### native-subtitle-quote-image ⭐2.6k
- **仓库**：https://github.com/chengyi-ai/native-subtitle-quote-image
- **作者**：程意（chengyi-ai）
- **做什么**：把字幕和金句做成图——封面、字幕条、朋友圈配图，把一段话变成一张能直接发的图。视频负责被刷到，图负责被记住。
- **安装**：`npx skills add https://github.com/chengyi-ai/native-subtitle-quote-image`
- **许可**：MIT

### dbskill ⭐10,573
- **做什么**：文本侧的老大，视频的上游是文案。一大批 skill 目录堆在一起。
- **安装**：走 `npx -y skills add <包名>` 装（⚠️ 原素材未给出确切仓库地址与包名；作者为 dontbesilent，具体安装命令请用户从原帖确认，本专家不替你猜命令）。
- **许可（⚠️ 重点）**：**CC BY-NC 4.0，非商用**。自己用没问题，商用要另外谈。
- **注意**：看数字之前先看许可。

### creator-buddy ⭐1,613
- **做什么**：公众号、小红书等几条线一起管，约三十来个 skill，覆盖公众号 / 小红书 / xhs / 视频。
- **安装**：原帖「10 个 Skill 搭建日更爆文的公众号写作系统」（⚠️ 原素材未给出确切仓库地址，需用户从原帖确认）。
- **许可（⚠️ 重点）**：README 写 MIT，但**仓库根目录没有 LICENSE 文件**，两者对不上。用之前先问作者确认。

---

## 五、清单之外（无 skill 可装，但套路可拆）

见 `references/viral-breakdown.md`：
- **古风武侠英语剧**：月涨粉 5 万。把英语单词塞进 80 年代邵氏武侠壳里，一句台词一个词。
- **AI 治愈号「小蘑菇秃秃」**：五个月吸粉 200 万。圆乎乎角色在木色厨房做应季甜点，卖情绪不卖信息。

两个号都没有开源 skill，但有可复用的「能重复的套路」。同一件事：爆款底层是一套能重复的套路——先有人把套路跑通，才有后面这些 skill 把它固化下来。
