# SEO Audit Checklist · SEO 审计清单

> 配合 `seo-discovery` 使用。四块逐项过，标 ✓ / ✗ / 假设。

## 一、技术基础（Critical：不改就搜不到）
- [ ] robots.txt 没误拦重要页
- [ ] 有 sitemap.xml 且已提交 Search Console
- [ ] 页面能被收录（site:域名 能搜到）
- [ ] 加载速度（LCP < 2.5s，移动端）
- [ ] 移动端适配
- [ ] HTTPS 全站
- [ ] 无重复内容（canonical 正确）
- [ ] URL 简洁、含关键词

## 二、内容优化（Recommended）
- [ ] 每个核心页有唯一 `<title>`（含主词，≤60 字）
- [ ] 有 `<meta description>`（含主词，≤160 字）
- [ ] 唯一 H1，含主词
- [ ] 正文覆盖主词 + 长尾，自然不堆砌
- [ ] 内容有深度（能答完用户问题）
- [ ] 图片有 alt 文本
- [ ] 内链把相关页串起来

## 三、外链与权威（Nice-to-have → 长期）
- [ ] 有没有被行业站 / 媒体引用
- [ ] 获取方向：客座文章、合作、资源页、产品上架

## 四、AI SEO（新：让 AI 搜索提到你）
- [ ] 核心问题写成 FAQ / 问答块，结构清晰
- [ ] 关键事实配数据 / 来源（提升被引用概率）
- [ ] 用 schema 标记（Org / Article / FAQ / Product）
- [ ] "关于我们 / 品牌"页信息完整（AI 常抓品牌页）

## 关键词映射模板
| 页面 | 主词 | 长尾 1 | 长尾 2 | 搜索意图 |
|---|---|---|---|---|
| 首页 | | | | |
| 功能页 | | | | |
| 博客/方案 | | | | |

## Schema 片段示例（FAQ）
```html
<script type="application/ld+json">
{ "@context":"https://schema.org", "@type":"FAQPage",
  "mainEntity":[{ "@type":"Question","name":"…",
    "acceptedAnswer":{ "@type":"Answer","text":"…" } }] }
</script>
```
