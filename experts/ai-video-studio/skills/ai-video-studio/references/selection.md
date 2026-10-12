# 选型决策树

用户说目标 → 顺着问 → 落到 skill。每条都标了「要不要 key / 烧不烧钱 / 许可」，方便装前排雷。

## Q0：你打算怎么用？自用还是商用？
- **商用（接单 / 给客户 / 变现）** → 先查 `license-matrix.md`。**dbskill（CC BY-NC）直接排除**；creator-buddy 需先确认 LICENSE；kid-papercraft 有非商业免责，慎用。
- **自用 / 练手** → 继续往下选。

## Q1：你想要什么类型的片？

### A. 风格化短片（不露脸、重视觉）
- 要「一张一个视觉风格、同一段文案出不同片子」 → **huashu-art-motion**（备 uv/ffmpeg/Playwright）
- 要「Vox 式解释动画，把复杂事拆开讲」 → **vox-director**
- 要「商业手绘风解说 / 带货」 → **hand-drawn-video-prompts**

### B. 手作 / 漫画（看起来像人做的）
- 想要**最省事、零 key** → **stickman-video-director**（但走 Google Flow 积分：10s 720P≈15 积分，Pro 每月 1000 积分 / 19.99 美元）
- 要做「萌宝纸艺生日祝福」且门槛极低 → **kid-papercraft**（5 问→3 条 10s，注意非商业免责）
- 要做「古诗丝绸质感」 → **hbg-classical-poem-silk-video**（Docker + gemini-flow-suite，仓库很新、慎依赖）
- 要做「长文案→统一漫画 IP 旁白」 → **hbg-life-simulation**（Edge TTS，默认横屏、竖屏要改）

### C. 资讯 / 解说 / 科普
- 做「新闻 / 热点长视频」 → **simon-skills**（video-common 须同层目录；火山引擎 TTS；Remotion/React 版本钉死）
- 做「科普：动画解说 / 故事动画 / 剧情影像」 → **director**（接 LibTV + 即梦）
- 做「图书带货短视频」 → **book-sales-video**（三个 key + 本地 OpenChatCut MCP，自由度大但最重）

### D. 图文 / 文案（视频的上游）
- 把「字幕 / 金句做成图」 → **native-subtitle-quote-image**
- 要「文案 / 选题 / 脚本」这一整层 → **dbskill**（CC BY-NC 非商用）
- 要「公众号 / 小红书多线内容」 → **creator-buddy**（LICENSE 待确认）

### E. 没对口 skill，但想抄爆款套路
- 古风武侠英语剧 / 治愈号「小蘑菇秃秃」 → 见 `viral-breakdown.md`，先把可重复的套路跑通，再决定要不要固化成自己的 skill。

## Q2：你的前置条件齐了吗？（装前必问）
- 有没有 key？（豆包 TTS / Pexels / WEREAD / 火山引擎 / 即梦 / LibTV）
- 本地有没有跑环境的本事？（uv / ffmpeg / Playwright / Docker / OpenChatCut MCP）
- 接不接受按积分烧钱？（stickman-video-director 走 Google Flow）
- 平台是横屏还是竖屏？（hbg-life-simulation 默认横屏，要改）

> 任何一项不满足，先让用户备齐再装。别把一键安装整段甩出去盲装。
