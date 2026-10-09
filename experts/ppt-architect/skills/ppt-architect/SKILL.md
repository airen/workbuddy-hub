---
name: ppt-architect
display_name: "PPT 架构师"
display_name_en: "PPT Architect"
description: "把任意主题变成可直接交付的演示文稿：按需选 PPTX 或 HTML 格式，内置 14 种专业风格，支持口播备注、参考图匹配、多页批量生成。"
description_zh: "把任意主题变成可直接交付的演示文稿：按需选 PPTX 或 HTML 格式，内置 14 种专业风格，支持口播备注、参考图匹配、多页批量生成。"
description_en: "Transform any topic into production-ready presentations: choose between editable PPTX or browser-ready HTML, apply professional design systems with 14 built-in styles, and deliver polished results ready for formal delivery."
category: content-creation
version: 1.0.0
author: "大漠"
---

# PPT 架构师技能

本技能把任何主题变成可直接交付的演示文稿。支持两种输出格式和 14 种内置风格。

## 输出格式选择

| 格式 | 适用场景 | 工具 |
|---|---|---|
| **PPTX** | 正式汇报、需二次编辑、交给他人修改 | `python-pptx` 库 |
| **HTML** | 在线演示、追求高颜值、远程技术分享 | 单文件 HTML + CSS |

用户未指定时，根据场景自动选择：
- 关键词「汇报」「提案」「客户」「正式」→ PPTX
- 关键词「分享」「演示」「技术」「网页」→ HTML

## 14 种内置风格

每种风格定义一套设计令牌（Design Tokens），直接应用到输出中。

### 设计令牌定义

```python
STYLES = {
    # 薄荷清新 - 科普讲解、工具教程、环保生活
    "mint-fresh": {
        "name_zh": "薄荷清新",
        "font_heading": "'Noto Sans SC', system-ui, sans-serif",
        "font_body": "'Noto Sans SC', system-ui, sans-serif",
        "colors": {
            "primary": "#2dd4bf",      # 薄荷绿
            "secondary": "#0ea5e9",    # 天蓝
            "accent": "#f59e0b",       # 暖黄
            "bg": "#f0fdfa",           # 薄荷底
            "text": "#134e4a",         # 深青
        },
        "layout": "clean-minimal",
    },
    
    # 商务蓝 - 工作汇报、方案提案、B 端产品
    "business-blue": {
        "name_zh": "商务蓝",
        "font_heading": "'Inter', 'Noto Sans SC', sans-serif",
        "font_body": "'Inter', 'Noto Sans SC', sans-serif",
        "colors": {
            "primary": "#1e40af",      # 深蓝
            "secondary": "#3b82f6",    # 中蓝
            "accent": "#f59e0b",       # 金橙点缀
            "bg": "#ffffff",           # 白底
            "text": "#1e293b",         # 深灰
        },
        "layout": "corporate-grid",
    },
    
    # 暖橙活力 - 个人分享、活动宣传、营销增长
    "warm-orange": {
        "name_zh": "暖橙活力",
        "font_heading": "'Noto Sans SC', system-ui, sans-serif",
        "font_body": "'Noto Sans SC', system-ui, sans-serif",
        "colors": {
            "primary": "#f97316",      # 橙色
            "secondary": "#fb923c",    # 浅橙
            "accent": "#84cc16",       # 绿点缀
            "bg": "#fff7ed",           # 暖白
            "text": "#431407",         # 深褐
        },
        "layout": "dynamic-bold",
    },
    
    # 深色科技 - AI 与科技产品、发布会、开发者内容
    "dark-tech": {
        "name_zh": "深色科技",
        "font_heading": "'JetBrains Mono', 'Noto Sans SC', monospace",
        "font_body": "'Inter', 'Noto Sans SC', sans-serif",
        "colors": {
            "primary": "#22d3ee",      # 青色
            "secondary": "#818cf8",    # 紫
            "accent": "#f472b6",       # 粉
            "bg": "#0f172a",           # 深空蓝
            "text": "#e2e8f0",         # 浅灰
        },
        "layout": "tech-dark",
    },
    
    # 雾紫柔和 - 情绪心理、美妆穿搭、读书感悟
    "lavender-soft": {
        "name_zh": "雾紫柔和",
        "font_heading": "'Noto Serif SC', Georgia, serif",
        "font_body": "'Noto Serif SC', Georgia, serif",
        "colors": {
            "primary": "#a78bfa",      # 紫
            "secondary": "#f0abfc",    # 粉紫
            "accent": "#67e8f9",       # 青
            "bg": "#faf5ff",           # 淡紫底
            "text": "#4c1d95",         # 深紫
        },
        "layout": "soft-organic",
    },
    
    # 纸感手记 - 读书笔记、方法论、个人成长
    "paper-notes": {
        "name_zh": "纸感手记",
        "font_heading": "'Noto Serif SC', 'Songti SC', serif",
        "font_body": "'Noto Serif SC', 'Songti SC', serif",
        "colors": {
            "primary": "#78716c",      # 灰褐
            "secondary": "#a8a29e",    # 浅灰
            "accent": "#d97706",       # 琥珀
            "bg": "#fefce8",           # 米黄
            "text": "#44403c",         # 深褐
        },
        "layout": "handwritten-note",
    },
    
    # 黑金述职 - 晋升述职、高层汇报、年度总结
    "black-gold": {
        "name_zh": "黑金述职",
        "font_heading": "'Playfair Display', 'Noto Serif SC', serif",
        "font_body": "'Inter', 'Noto Sans SC', sans-serif",
        "colors": {
            "primary": "#fbbf24",      # 金色
            "secondary": "#f59e0b",    # 暗金
            "accent": "#dc2626",       # 红点缀
            "bg": "#0a0a0a",           # 纯黑
            "text": "#f5f5f5",         # 近白
        },
        "layout": "luxury-dark",
    },
    
    # 几何色块 - 运营复盘、团队年终、数据报告
    "geo-blocks": {
        "name_zh": "几何色块",
        "font_heading": "'Inter', 'Noto Sans SC', sans-serif",
        "font_body": "'Inter', 'Noto Sans SC', sans-serif",
        "colors": {
            "primary": "#ef4444",      # 红
            "secondary": "#3b82f6",    # 蓝
            "accent": "#22c55e",       # 绿
            "bg": "#ffffff",           # 白底
            "text": "#111827",         # 深灰
        },
        "layout": "geometric-blocks",
    },
    
    # 钴蓝字体 - 设计分享、观点演讲、学术报告
    "cobalt-type": {
        "name_zh": "钴蓝字体",
        "font_heading": "'Space Grotesk', 'Noto Sans SC', sans-serif",
        "font_body": "'Inter', 'Noto Sans SC', sans-serif",
        "colors": {
            "primary": "#1d4ed8",      # 钴蓝
            "secondary": "#60a5fa",    # 浅蓝
            "accent": "#f97316",       # 橙点缀
            "bg": "#ffffff",           # 白底
            "text": "#0f172a",         # 近黑
        },
        "layout": "typography-focused",
    },
    
    # 黑灰荧绿 - 业绩汇报、销售复盘、指标分析
    "ink-lime": {
        "name_zh": "黑灰荧绿",
        "font_heading": "'JetBrains Mono', 'Noto Sans SC', monospace",
        "font_body": "'Inter', 'Noto Sans SC', sans-serif",
        "colors": {
            "primary": "#84cc16",      # 荧绿
            "secondary": "#22c55e",    # 绿
            "accent": "#f97316",       # 橙
            "bg": "#18181b",           # 深灰黑
            "text": "#d4d4d4",         # 浅灰
        },
        "layout": "data-dashboard",
    },
    
    # 蓝粉柔雾 - 实习汇报、校园分享、个人总结
    "pastel-mist": {
        "name_zh": "蓝粉柔雾",
        "font_heading": "'Noto Sans SC', system-ui, sans-serif",
        "font_body": "'Noto Sans SC', system-ui, sans-serif",
        "colors": {
            "primary": "#f9a8d4",      # 粉
            "secondary": "#93c5fd",    # 蓝
            "accent": "#c4b5fd",       # 紫
            "bg": "#fdf2f8",           # 粉白底
            "text": "#831843",         # 深粉
        },
        "layout": "soft-pastel",
    },
    
    # 蓝线发布 - 新品发布、科技大会、产品路线图
    "wave-launch": {
        "name_zh": "蓝线发布",
        "font_heading": "'Inter', 'Noto Sans SC', sans-serif",
        "font_body": "'Inter', 'Noto Sans SC', sans-serif",
        "colors": {
            "primary": "#0ea5e9",      # 天蓝
            "secondary": "#6366f1",    # 靛蓝
            "accent": "#14b8a6",       # 青
            "bg": "#ffffff",           # 白底
            "text": "#0f172a",         # 近黑
        },
        "layout": "launch-wave",
    },
    
    # 墨水杂志 - 观点分享、读书与人文、研究报告
    "ink-magazine": {
        "name_zh": "墨水杂志",
        "font_heading": "'Noto Serif SC', 'Playfair Display', serif",
        "font_body": "'Noto Serif SC', Georgia, serif",
        "colors": {
            "primary": "#1a1a1a",      # 墨黑
            "secondary": "#404040",    # 灰黑
            "accent": "#c45d3e",       # 赭红
            "bg": "#f5f2eb",           # 纸张白
            "text": "#1a1a1a",         # 墨黑
        },
        "layout": "magazine-editorial",
    },
    
    # 硬边网格 - 产品发布、方法论、数据复盘
    "swiss-grid": {
        "name_zh": "硬边网格",
        "font_heading": "'Inter', 'Helvetica Neue', sans-serif",
        "font_body": "'Inter', 'Helvetica Neue', sans-serif",
        "colors": {
            "primary": "#ff4400",      # 瑞士红
            "secondary": "#000000",    # 黑
            "accent": "#ffffff",       # 白
            "bg": "#ffffff",           # 白底
            "text": "#000000",         # 黑
        },
        "layout": "swiss-grid",
    },
}
```

## 内容架构规则

### 每页内容限制

- **标题**：不超过 12 字
- **正文**：每页不超过 6 行，每行不超过 20 字
- **要点**：3-5 条为宜
- **口播备注**：可选，每页 50-100 字

### 页面结构模板

```markdown
## [页码] 标题

### 要点
1. 要点一
2. 要点二
3. 要点三

### 可视化建议
- 图表类型：柱状图/流程图/时间轴
- 配图建议：[描述]

### 口播备注（可选）
演讲者说：...
```

## PPTX 生成流程

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN

def create_pptx(slides_config, style):
    """
    slides_config: list of dict, 每页配置
    style: 风格名，如 'ink-magazine'
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9
    prs.slide_height = Inches(7.5)
    
    for i, slide in enumerate(slides_config):
        # 根据页码选择版式
        if i == 0:
            slide_layout = prs.slide_layouts[6]  # 空白
        elif i == len(slides_config) - 1:
            slide_layout = prs.slide_layouts[6]  # 结束页
        else:
            slide_layout = prs.slide_layouts[6]  # 空白（自定义）
        
        slide = prs.slides.add_slide(slide_layout)
        
        # 应用风格
        apply_style(slide, style)
        
        # 添加标题
        add_title(slide, slide['title'])
        
        # 添加内容
        add_content(slide, slide.get('bullet_points', []))
        
        # 添加口播备注
        if slide.get('speaker_notes'):
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = slide['speaker_notes']
    
    return prs
```

## HTML 生成流程

```python
def create_html(slides_config, style):
    """生成单文件 HTML 演示文稿"""
    
    style_config = STYLES[style]
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PPT Presentation</title>
    <style>
        :root {{
            --color-primary: {style_config['colors']['primary']};
            --color-secondary: {style_config['colors']['secondary']};
            --color-accent: {style_config['colors']['accent']};
            --color-bg: {style_config['colors']['bg']};
            --color-text: {style_config['colors']['text']};
            --font-heading: {style_config['font_heading']};
            --font-body: {style_config['font_body']};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: var(--font-body);
            background: var(--color-bg);
            color: var(--color-text);
            overflow: hidden;
        }}
        
        .slide {{
            width: 100vw;
            height: 100vh;
            display: none;
            padding: 60px 80px;
            position: relative;
        }}
        
        .slide.active {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        h1 {{
            font-family: var(--font-heading);
            font-size: 3rem;
            color: var(--color-primary);
            margin-bottom: 1rem;
        }}
        
        h2 {{
            font-size: 2rem;
            margin-bottom: 1.5rem;
        }}
        
        ul {{
            list-style: none;
            font-size: 1.5rem;
            line-height: 1.8;
        }}
        
        li {{
            padding-left: 1.5rem;
            position: relative;
        }}
        
        li::before {{
            content: '•';
            color: var(--color-accent);
            position: absolute;
            left: 0;
        }}
        
        .notes {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            font-size: 0.9rem;
            max-width: 300px;
            display: none;
        }}
        
        .controls {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
        }}
        
        button {{
            padding: 10px 20px;
            background: var(--color-primary);
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
        }}
        
        .progress {{
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: var(--color-accent);
            transition: width 0.3s;
        }}
    </style>
</head>
<body>
    <div class="progress" id="progress"></div>
"""
    
    # 生成每页内容
    for i, slide in enumerate(slides_config):
        html_template += f"""
    <div class="slide {'active' if i == 0 else ''}" data-index="{i}">
        <h1>{slide['title']}</h1>
"""
        if slide.get('bullet_points'):
            html_template += "        <ul>\n"
            for point in slide['bullet_points']:
                html_template += f"            <li>{point}</li>\n"
            html_template += "        </ul>\n"
        
        if slide.get('speaker_notes'):
            html_template += f'        <div class="notes">{slide["speaker_notes"]}</div>\n'
        
        html_template += "    </div>\n"
    
    # 添加控制脚本
    html_template += """
    <div class="controls">
        <button onclick="prevSlide()">上一页</button>
        <button onclick="nextSlide()">下一页</button>
        <button onclick="toggleNotes()">备注</button>
    </div>
    
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        
        function showSlide(index) {
            slides[currentSlide].classList.remove('active');
            currentSlide = (index + totalSlides) % totalSlides;
            slides[currentSlide].classList.add('active');
            updateProgress();
        }
        
        function nextSlide() {
            showSlide(currentSlide + 1);
        }
        
        function prevSlide() {
            showSlide(currentSlide - 1);
        }
        
        function toggleNotes() {
            const notes = slides[currentSlide].querySelector('.notes');
            if (notes) {
                notes.style.display = notes.style.display === 'block' ? 'none' : 'block';
            }
        }
        
        function updateProgress() {
            const progress = ((currentSlide + 1) / totalSlides) * 100;
            document.getElementById('progress').style.width = progress + '%';
        }
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
            if (e.key === 'n') toggleNotes();
        });
    </script>
</body>
</html>"""
    
    return html_template
```

## 使用示例

### 示例 1：墨水杂志风格 PPT

```
用户：把这篇文章做成 12 页的口播 PPT，每页带口播备注，用墨水杂志风格。

Agent 执行：
1. 解析文章，提取核心观点
2. 按 12 页规划内容结构
3. 每页生成标题、要点、口播备注
4. 应用 ink-magazine 风格（衬线字体、纸张底色、赭红点缀）
5. 输出 .pptx 文件
```

### 示例 2：HTML 演示文稿

```
用户：主题是"AI 工具号年度复盘"，给我出三张风格样张，我挑一个再往下做。

Agent 执行：
1. 生成三套不同风格的 HTML 预览（dark-tech / ink-magazine / swiss-grid）
2. 每套包含封面 + 目录 + 2-3 个内容页
3. 用户选择后，生成完整演示文稿
```

## 质量控制

生成后必须检查：
- [ ] 每页文字不超过 6 行
- [ ] 配色与选定风格一致
- [ ] 字体层级清晰（标题 > 正文 > 备注）
- [ ] 无拼写错误
- [ ] 如有图表，数据准确
- [ ] 口播备注与页面内容对应
