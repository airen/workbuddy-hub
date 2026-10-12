# 安装命令、环境准备与高频坑

## 一、通用安装方式

绝大多数走 `npx skills add <仓库地址>`：

```bash
npx skills add https://github.com/alchaincyf/huashu-art-motion
npx skills add https://github.com/Alisa0808/vox-director
npx skills add https://github.com/kaomei/hand-drawn-video-prompts
npx skills add https://github.com/kaomei/stickman-video-director
npx skills add https://github.com/kaomei/kid-papercraft
npx skills add https://github.com/Mr-funny/hbg-classical-poem-silk-video
npx skills add https://github.com/Mr-funny/hbg-life-simulation
npx skills add https://github.com/trustfuture/simon-skills
npx skills add https://github.com/s1dashu/director
npx skills add https://github.com/Kianzzz/book-sales-video
npx skills add https://github.com/chengyi-ai/native-subtitle-quote-image
```

- **dbskill**：走 `npx -y skills add <包名>`（⚠️ 原素材未给确切包名，作者 dontbesilent，命令请用户从原帖确认）。
- **creator-buddy**：原素材未给仓库地址，需用户从原帖「10 个 Skill 搭建日更爆文的公众号写作系统」确认。
- **hbg-classical-poem-silk-video**：不是 npx，是跑一个 **Docker 容器**（里面是 gemini-flow-suite）。

## 二、环境依赖准备（装前核对）

| skill | 需要的环境 |
|---|---|
| huashu-art-motion | `uv` + `ffmpeg` + `Playwright`（三样少一个都起不来） |
| hbg-classical-poem-silk-video | Docker + gemini-flow-suite |
| simon-skills | 火山引擎 TTS 环境；Remotion / React 版本钉死 |
| director | LibTV CLI + 即梦账号 |
| book-sales-video | 豆包 TTS key + Pexels key + WEREAD key + 本地 OpenChatCut MCP |
| stickman-video-director | 无 key，但需 Google AI Pro / Flow 积分 |
| 其余 | 一般无特殊依赖 |

> 安装提醒：skill 可能有环境依赖，让 Claude / Codex 帮你处理就好，装好按 skill 流程与说明去制作视频。

## 三、高频坑（来自原素材）

1. **simon-skills 的 video-common 必须和另外两个放在同一层目录**，否则另外两个找不到它。
2. **simon-skills 的 Remotion / React 版本钉死**，别自己升。
3. **hbg-life-simulation 默认 1920×1080 横屏**，发竖屏短视频记得改。
4. **hbg-classical-poem-silk-video 只有一个提交**，很新、别指望长期维护。
5. **kid-papercraft / dbskill / creator-buddy 许可要盯**：非商业免责 / CC BY-NC / README 与 LICENSE 对不上。
6. **stickman-video-director 走积分**：10s 720P≈15 积分，Pro 每月 1000 积分（19.99 美元），免费额度用完要续。

## 四、一键安装整段（原素材给的「丢给 Agent」版本）

> 注意：原素材建议**别一次全装**，先挑你要的那两条。下面这段仅在你确定要批量装时用。

```
请帮我依次安装以下仓库的全部 skill，装完告诉我每个仓库装了什么：

https://github.com/alchaincyf/huashu-art-motion
https://github.com/Alisa0808/vox-director
https://github.com/kaomei/hand-drawn-video-prompts
https://github.com/kaomei/stickman-video-director
https://github.com/kaomei/kid-papercraft
https://github.com/Mr-funny/hbg-classical-poem-silk-video
https://github.com/Mr-funny/hbg-life-simulation
https://github.com/trustfuture/simon-skills
https://github.com/s1dashu/director
https://github.com/Kianzzz/book-sales-video
https://github.com/chengyi-ai/native-subtitle-quote-image
```

## 五、装好之后（强烈建议）

安装好 skill 后，**根据你的审美、设计或流程重新定制这个 skill**——只有符合你要求的 skill 才是最好的 skill。
- 如果你本地已有类似的 skill，可以让 AI 学习、强化你自己的 skill，不一定就要直接安装；
- 如果你不熟悉，可以先试用一下 skill 再说。
