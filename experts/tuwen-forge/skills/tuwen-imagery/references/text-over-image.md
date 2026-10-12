# 文字压图与主体避让

> 满铺图 + 压字，是图文里最容易出彩、也最容易翻车的版式。
> 翻车的唯一原因几乎都是：**字压在了主体上，或者遮罩盖死了图。**

## 一、三步法

```
1. 标主体      → 人脸 / 产品 / 文字 / 高对比区，标出来
2. 定 quiet zone → 找没细节的安静区
3. 加 scrim     → 只在文字所在区域加渐变遮罩
```

**顺序不能反。** 先想"字放哪"，再找图，会找不到图。

## 二、scrim（渐变遮罩）

### 正确做法：局部渐变

```css
.image-led .scrim{
  position:absolute; inset:0;
  background:linear-gradient(180deg, rgba(0,0,0,0) 30%, rgba(0,0,0,.74) 100%);
}
```

- 文字在下方 → 遮罩从下往上加深（`180deg`）
- 文字在上方 → 遮罩从上往下加深（`0deg`）
- **最深处不透明度 0.7 – 0.8**，再深图就看不见了
- **上半部分保持全透明**，让图透出来

### 错误做法

| 错误 | 后果 |
|---|---|
| 全图 `background: rgba(0,0,0,.6)` | 图被压死，变成"灰蒙蒙一片" |
| 遮罩最深处 0.95 | 图完全消失 |
| 遮罩方向与文字位置相反 | 字还是看不清 |
| 用纯黑不用渐变 | 生硬的横切边 |

## 三、文字避让规则

| 主体 | 文字位置 |
|---|---|
| 人脸（竖构图） | 头顶上方 或 画面下方 1/4（避开下巴以下到胸口） |
| 人脸（横构图） | 左侧或右侧空档 |
| 食物（俯拍） | 画面顶部或底部（避开盘子） |
| 产品（居中） | 左侧 或 右侧 |
| 建筑 | 下方地面 / 上方天空 |
| 风景（海平线） | 天空带 或 水面带 |

**绝对不要**：字压在眼睛上、压在产品 logo 上、压在画面里已有的文字上。

## 四、quiet zone 不足时的处理

按顺序尝试：

1. **换图**（最省事）
2. **裁切**，把安静区裁进画板
3. **局部 tint**：只在文字区域加一块半透明色块（不是全图遮罩）
   ```css
   .image-led .overlay{
     background:rgba(0,0,0,.35);
     padding:28px 32px;
     display:inline-block;      /* 只包住文字，不是整行 */
   }
   ```
4. **改成"上图下文"**：图占上半 55%，下半用纯色底放字
   - 这是最稳的兜底，几乎不会翻车

## 五、文字样式（压图时）

| 项 | 建议 |
|---|---|
| 颜色 | `#fff`（唯一允许写死的颜色，因为对比对象是照片） |
| 字号 | ≥ 52 px（图有噪点，小字看不清） |
| 字重 | 400 – 600（太细会被图吃掉） |
| 字距 | 大标题 `-0.01em`；eyebrow `0.18em` |
| 阴影 | ❌ 不要用 `text-shadow` 硬撑，用 scrim 更干净 |
| 行高 | 1.15 – 1.3 |

## 六、完整示例

```html
<section class="poster image-led" data-theme="midnight" data-name="01-cover">
  <div class="bg" style="background-image:url('assets/img/01.jpg');
                          background-position:center 28%"></div>
  <div class="scrim"></div>
  <div class="overlay">
    <span class="eyebrow">旅行笔记</span>
    <h1 class="h-xl">在冰岛<br>等一场极光</h1>
  </div>
</section>
```

```css
.poster.image-led{padding:0;justify-content:flex-end}
.image-led .bg{position:absolute;inset:0;background-size:cover;background-position:center}
.image-led .scrim{position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(0,0,0,0) 34%,rgba(0,0,0,.74) 100%)}
.image-led .overlay{position:relative;z-index:2;padding:0 84px 96px;color:#fff}
```

## 七、自检

- [ ] 文字没有压在人脸/产品/已有文字上
- [ ] scrim 是渐变且只覆盖文字区域，上半部分透明
- [ ] 遮罩最深处 ≤ 0.8
- [ ] 文字字号 ≥ 52 px
- [ ] 用了 scrim 而不是 text-shadow
- [ ] `background-position` 已按主体位置调整
- [ ] quiet zone 不足时已降级为"上图下文"
