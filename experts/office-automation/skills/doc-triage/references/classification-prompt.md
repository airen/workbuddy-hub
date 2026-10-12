# 文档整理 · AI 分类与字段提取提示词（classification-prompt）

把一批存量文档交给「办妥」整理时，用下面这份提示词模板（复制到对话里，替换 `{{占位}}`）。它对应 paperless-aissist 的"AI 分类、标题生成、字段提取、OCR"思路，先内化成本地可跑版本。

---

## 模板

```
你是一位文档整理助手。我有一批需要归档的文档（路径/内容如下）。请为每份文档做四件事：

1. 分类（category）：从固定类目里选最贴切的一个
   候选类目：财务/发票、合同/商务、报告/内部、设备/说明书、人事/证照、其他
2. 生成标题（title）：基于内容起一个能一眼看懂的名字（含关键实体/日期）
3. 提取字段（按下方 schema 输出 CSV 一行）：
   id, filename, title, category, tags, doc_date, source, ocr_text, related_persons, amount, currency, warranty_until, notes
4. OCR 兜底：若文档是图片/扫描件且未提供文字，先说明"需 OCR"，并基于可见信息尽量填，标 [OCR待补]

文档清单：
{{粘贴文件名列表，或逐份贴入文本/图片内容}}

输出要求：
- 一份汇总 CSV（表头用上面的 schema）
- 每张表的 category 只能取候选类目之一
- tags 用 JSON 数组，3 个以内、贴合检索
- doc_date / warranty_until 用 YYYY-MM-DD，未知留空
- 金额类文档务必填 amount + currency
- 涉及保密/对外的，在 notes 标注"脱敏后对外"
```

---

## 使用示例

用户："帮我整理桌面上这 8 个扫描件，有发票有合同还有一份路由器说明书。"

助手动作：
1. 让用户把文件丢进对话（或给路径）。
2. 套用上面模板，逐份产出 分类 / 标题 / 字段。
3. 汇总成一张 `文档清单.csv`（schema 见 `triage-schema.csv` 表头）。
4. 对图片型文档提示"需 OCR"，给出基于可见信息的初稿并标 [OCR待补]。
5. 交付 `文档清单.csv` + 一句话"这批文档分到了 X 类，Y 份需补 OCR"。

## 后续衔接

- 整理清楚后，重点文档可用 `doc-revise-diff` 做版本管理。
- 要"就地编辑/检索"可参考 `office-sdk-embed` 给内部知识库嵌表格能力。
