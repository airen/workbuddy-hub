# 截图美化

> 产品测评、工具教程、软件说明类图文里，**截图才是主角**。裸截图会显得潦草。

## 一、为什么要包壳

裸截图的三个问题：

1. **边界不清**：白底截图放在浅色画板上会"融"进去
2. **尺寸随意**：一张 2400×1200 的截图直接塞进 928 px 宽的内容区会变形
3. **没有语境**：看不出这是浏览器、手机还是桌面应用

**包壳 = 给截图一个"这是界面"的语境。**

## 二、三种壳

### 1. `.frame-shot` 通用边框壳（最常用）

```css
.frame-shot{
  border:1px solid var(--rule);
  background:#fff;
  padding:14px;
  box-shadow:0 1px 0 var(--rule);
  width:100%;
}
.frame-shot img{display:block;width:100%;height:auto}
```

适合：任意截图、局部放大、图表导出图。

### 2. `.device-browser` 浏览器壳

```css
.device-browser{border:1px solid var(--rule);background:#fff;width:100%;overflow:hidden}
.device-browser .bar{
  height:44px;background:var(--tint);border-bottom:1px solid var(--rule);
  display:flex;align-items:center;gap:8px;padding:0 16px;
}
.device-browser .dot{width:12px;height:12px;border-radius:50%;background:var(--rule)}
.device-browser .url{
  margin-left:12px;font-size:20px;color:var(--ink-2);
  font-family:var(--font-mono);
}
.device-browser img{display:block;width:100%;height:auto}
```

```html
<div class="device-browser">
  <div class="bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span>
    <span class="url">app.example.com/dashboard</span></div>
  <img src="assets/img/shot-01.png" alt="控制台界面">
</div>
```

适合：Web 应用、网站、后台界面。

### 3. `.device-phone` 手机壳

```css
.device-phone{
  width:420px;border:12px solid var(--ink);border-radius:44px;
  background:var(--ink);overflow:hidden;margin:0 auto;
}
.device-phone img{display:block;width:100%;height:auto;border-radius:32px}
```

适合：移动端 App、小程序、手机页面。

> ⚠️ 手机壳用了圆角——这是 Swiss 系统的**唯一例外**（因为设备本身就是圆角）。
> 除此之外 Swiss 一律直角。

## 三、截图本身的处理

| 问题 | 处理 |
|---|---|
| 分辨率过高（> 2400 px 宽） | 缩到 1400–1800 px |
| 白底，与画板撞色 | 包壳 + 加边框 |
| 有敏感信息（邮箱、密钥、真实姓名） | **必须打码**，或换成脱敏截图 |
| 有浏览器书签栏 / 标签页 | 裁掉，只留内容区 |
| 系统状态栏时间不一致 | 统一裁掉或统一时间 |
| 深色界面 | 用 `midnight` 主题，壳也改深色 |

### 敏感信息必须处理

```
⚠️ 截图里出现：邮箱、手机号、API Key、真实姓名、内网地址、公司内部数据
→ 一律打码或替换为示例数据，并在交付说明里提醒用户
```

## 四、多张截图的排列

| 数量 | 排列 |
|---|---|
| 1 张 | 整宽，占画布 55–65% |
| 2 张 | 上下叠放，或左右各 48% |
| 3 张 | 一主两副（大 + 两个小） |
| 4 张以上 | 拆成多页，或改做长图 |

**不要在一页里塞 4 张以上截图**——每张都会小到看不清。

## 五、局部放大

需要指出某个按钮/区域时：

```html
<div class="frame-shot zoom">
  <img src="assets/img/shot-01.png" alt="设置入口" style="width:260%">
</div>
```

配合 `overflow:hidden` 与外层定位，把要强调的区域裁到框里。
**用 `.mark` 色块或手绘箭头标出目标**（SVG 箭头，不要用 emoji）。

## 六、自检

- [ ] 截图包了壳，边界清晰
- [ ] 缩放后不变形（保持宽高比）
- [ ] 敏感信息已打码
- [ ] 浏览器书签栏/状态栏已裁掉
- [ ] 一页不超过 3 张截图
- [ ] 深色界面配深色主题
- [ ] 标注用的是色块/SVG 箭头，不是 emoji
