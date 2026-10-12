# Hypit 使用指南（结构层）

Hypit 是给 AI Coding Agent 用的视频创作系统（Claude Code / Codex 等）。对拆解者而言，它把一条视频还原成可编辑的 SVML「视频脚本图」——这就是我们的结构层输入。

> 来源：https://github.com/hypit-ai/hypit （开源免费）。框架免费，Coding Agent 与模型服务各自计费，安装不附带生成额度。

## 1. 安装
在用户的 Coding Agent / 终端里执行（一次即可，`-g` 表示全局）：
```bash
npx skills add hypit-ai/hypit -g
```
- 核对版本：`hypit version --check`（旧版用 `hypit --version` / `npm view @hypit/hypit@latest version`）。
- 程序与 Skill 分别更新，可保留视频项目只更新安装。
- 无需克隆 Hypit 仓库，Skill 提供制作知识，`hypit` 包提供可执行工具。

## 2. 喂入视频 + 说明意图
在 Agent 中打开视频项目，把视频文件或平台链接交给它，并说明想怎么拆：
```
/hypit 参考这个视频：/path/to/video.mp4。
帮我把它还原成结构化的 SVML 脚本图，标注每个分镜的钩子、节拍、字幕落点和情绪时刻。
```
- 可调项：人物、产品、语言、画幅、行动号召。
- 无对白视频：明确告诉 Hypit 跳过 WhisperX，只做画面与节奏分析。

## 3. 选择服务（理解原片用）
- 有对白：WhisperX 提供「词 + 时间」，帮 Agent 把画面变化与说话内容对应起来。缺时 Agent 会协助本机准备或说明托管选项。
- HypiHub（hypit.ai）一个账户托管 WhisperX + 图片/视频/音色模型；也可用自有 Key，或本地/托管混合。
- 不必一开始定死账户，等素材方案明确需要哪些模型时再解决。

## 4. 确认费用，开始制作
付费前 Agent 会说明用哪个账户、做什么、费率/预计费用。确认后连续推进。真实素材到位后，Agent 会检查版面、字幕、图形、B-roll 是否清楚、时机是否恰当。

## 5. 读产物：SVML 视频脚本图
Hypit 把视频拆成多层（来自官方文档）：
- **Script Surface（脚本面）**：
  - `Segment` 分镜/段落 —— 视频被切成的时间块（这是结构与节拍分析的素材）。
  - `Role Cue` 角色提示 —— 出镜人物/角色及其表演方向。
  - `Dual Text` 双语文案 —— 原声与字幕/译文的对应。
  - `Selection` 关键选择 —— 镜头/素材/风格的关键决策点。
  - `Moment` 情绪时刻 —— 情绪高点或转折点（情绪曲线素材）。
  - `Text Projection` 文本投影 —— 字幕/文案落在具体词上的位置（字幕落点素材）。
- **SVS 样式表**：类 CSS 的配方语言，管影片、字幕、媒体、文本与生成设置。
- **Tracks（轨道）**：字幕、媒体、排版、作者声明音频等并列组件。
- **Film & Render**：把 Tracks 合成 Film 并渲染成视频。
- **Build Result**：执行过程与产物保存处；项目是普通文件，可继续编辑；也可进 Studio 可视化时间线微调。

> 拆解者重点读：**Segment 的切分与时长、Role Cue 的表演方向、Dual Text 的文案、Text Projection 的字幕落点、Moment 的情绪点**。这五项是八维分析（见 viral-pattern-framework.md）的直接素材。

## 6. 把产物带回 WorkBuddy
让 Hypit/Agent 把上述 SVML 文本、关键帧、时间线**导出或截图**，贴回 WorkBuddy 对话，进入分析层（第 3 步）。

## 7. 回流：用模板做变体
拆完得到套路模板后，可在 Hypit 里继续：
```
/hypit 按这份模板重做一条：把主题换成 ___，保留开场钩子和 Moment 结构。
```

## 安全与合规
- 只分析你有权分析的内容，遵守平台条款与当地法律。
- 自有 Key 时告知 Agent 密钥归属的服务并给接口文档；生成额度按需确认。
- 免费可领 100 个带独特音色的 AI 人物（见 Hypit 官方说明），可用于变体制作。
