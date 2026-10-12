# 视频爆款拆解师 · 爆析（viral-video-decoder）

结合 **Hypit** 与 **WorkBuddy**，手把手带用户一步步拆解任意爆款视频，产出可复用的创作模板。

## 两层方法
- **结构层（Hypit）**：把视频还原成 SVML 脚本图——分镜（Segment）、角色提示（Role Cue）、双语文案（Dual Text）、关键选择（Selection）、情绪时刻（Moment）、字幕落点（Text Projection）。
- **分析层（WorkBuddy）**：用证据框架（observed / metric / inferred / unknown）+ 八维套路框架，把「为什么火」翻译成可迁移模板。

## 工作流
定目标 → Hypit 出 SVML 解剖图 → 带回产物 → WorkBuddy 八维分析 → 产出爆款套路模板 →（可选）做变体 / 回流 Hypit。

## 目录
```
agents/viral-video-decoder.md                  # 主理人：编排两步工作流
skills/viral-video-decoder/SKILL.md            # 方法论总纲
skills/viral-video-decoder/references/
  hypit-guide.md                               # Hypit 安装 / 喂视频 / 读 SVML 产物
  evidence-framework.md                        # 证据分级 + 研究包 + 三档深度
  viral-pattern-framework.md                   # 八维拆解框架
  templates.md                                 # 报告模板 / 套路模板 / 映射示例
```

## 外部方法论来源（MIT，仅作框架参考）
- **pinker12/viral-video-analyze** —— 证据分级法（observed / metric / inferred / unknown）与三档分析。
- **KINNONG/viral-video-breakdown** —— 创作者研究包结构（source / keyframes / transcript / story_analysis）。

## 合规
只分析你有权分析的内容，遵守平台条款与当地法律。不鼓励照搬他人内容，目标是可迁移的结构。
