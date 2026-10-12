---
name: doc-triage
display_name: 整理存量文档
display_name_en: Triage Existing Documents
description: "Organize a pile of existing documents with AI — auto-classify, generate titles, extract structured fields, and OCR scans. Use when the user has a backlog of files to sort, tag, and make searchable. Inspired by nyxtron/paperless-aissist."
category: content
version: 1.0.0
author: 大漠
---

# 整理存量文档

对应开源项目 **nyxtron/paperless-aissist** 的核心能力：给 Paperless-ngx 加 AI 分类、标题生成、字段提取和 OCR。这里把它内化成一个**本地可跑**的整理工作流——用户有一堆散文档，「办妥」先分类、起标题、抽字段，产出一张可检索的清单。

## 适用场景

- "桌面这 8 个扫描件帮我理一理，有发票有合同还有说明书"
- "把这批合同按类别归档，提取关键日期和金额"
- "这些纸质资料拍了照，给我做个能搜的清单"
- 用户有一批存量文档，要"看得清、找得到"

## 输入

- 一批文件（路径/内容/图片），或逐份贴入
- 可选：自定义类目、要提取的字段重点

## 执行步骤

### 1. 取清单
让用户把文件丢进对话或给路径；图片/扫描件先确认是否需要 OCR。

### 2. 逐份处理（套用提示词）
读取 `references/classification-prompt.md`，对每份文档做：
- **分类**：从固定类目选最贴切的一个（财务/发票、合同/商务、报告/内部、设备/说明书、人事/证照、其他）
- **标题**：基于内容起"一眼看懂"的名字
- **字段提取**：按 `references/triage-schema.csv` 的表头输出一行（id, filename, title, category, tags, doc_date, source, ocr_text, related_persons, amount, currency, warranty_until, notes）
- **OCR 兜底**：图片/扫描件未带文字时，说明"需 OCR"，基于可见信息给初稿并标 [OCR待补]

### 3. 汇总交付
- 产出一张 `文档清单.csv`（schema 见 `triage-schema.csv`，含 4 行示例可参考）
- 一句话"这批分到了 X 类，Y 份需补 OCR"
- 分类结果可建议用户据此建文件夹/标签体系

### 4. 常态化（重复工作）
- 高频归档（如每月发票、每季度合同）把类目与字段固定成模板，下次批量跑。
- 整理后重点文档用 `doc-revise-diff` 做版本管理；要"就地检索"参考 `office-sdk-embed`。

## 毕业到原项目（paperless-aissist）的提示

paperless-aissist 是给 **Paperless-ngx** 文档系统加 AI 能力的插件，**前置条件**：
- 你**先得有一套运行中的 Paperless-ngx**（自建文档管理系统）
- 在它之上部署 aissist 插件，才能享受"入库即自动分类/OCR/抽字段"
- 涉及**大量私密文档集中存储**，需自行保障服务器与访问安全
- 「办妥」默认用本地整理工作流产出清单，不依赖 Paperless-ngx；只有当你已自建并运维该系统、且需要"入库自动化"时，才考虑接入 paperless-aissist。

## 边界

- OCR 对模糊/倾斜扫描件可能不准，标 [OCR待补] 让用户复核，不把 OCR 结果当确证。
- 合同/证照/财务类敏感文档，提取的字段仅作整理索引，不下"已核验/已合规"结论。
- 不对用户原始文件做不可逆删除/移动；清单是新增产物，原文件保持原位。
