# Style Atlas Batch Status

## Batch 1 — basic systems

| Order | Style | Status | Output | Technical check | Notes |
|---:|---|---|---|---|---|
| 01 | Flat illustration / 扁平插画 | generated — human text QA pending | `images/01-flat-illustration-annotated-v2.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. Review via `images/batch-01-annotated-contact-sheet-v1.jpg`. |
| 02 | Semi-realistic illustration / 半写实插画 | generated — human text QA pending | `images/02-semi-realistic-illustration-annotated-v2.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. |
| 03 | 3D toy / 3D 玩具 | generated — human text QA pending | `images/03-3d-toy-annotated-v2.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. |
| 04 | Clay / 黏土风 | generated | `images/04-clay-v1.png` | PASS — PNG, 1672×941, RGB | Original unbranded benchmark scene. |
| 05 | Comic / 漫画 | generated | `images/05-comic-v1.png` | PASS — PNG, 1672×941, RGB | Original unbranded benchmark scene. |
| 06 | Pixel art / 像素艺术 | generated | `images/06-pixel-art-v1.png` | PASS — PNG, 1672×941, RGB | Original unbranded benchmark scene. |

## Scene approval

**Selected scene:** Direction C — 三个节点，各有职责，接力完成修复.

**First production test batch:** only 01 Flat illustration, 02 Semi-realistic illustration, and 03 3D toy. Each must render the exact integrated Chinese labels `发现`, `定位`, `断点`, `接回`, `验证` on physical scene carriers. Do not start 04–18 until the user reviews this three-style batch.

## Batch 2 — first three modern / manga systems

| Order | Style | Status | Output | Technical check | Notes |
|---:|---|---|---|---|---|
| 07 | Hand-drawn technical sketch / 手绘技术草图 | generated — human text QA pending | `images/07-hand-drawn-technical-sketch-annotated-v1.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. Contact sheet: `images/batch-02-annotated-contact-sheet-v1.jpg`. |
| 08 | Classic Japanese children’s manga-animation / 经典日式儿童漫画动画 | generated — human text QA pending | `images/08-classic-japanese-childrens-manga-animation-annotated-v1.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. |
| 09 | Japanese gag-reaction manga-animation / 日式搞笑反应漫画动画 | generated — human text QA pending | `images/09-japanese-gag-reaction-manga-animation-annotated-v1.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. |

## Batch 3 — remaining basic systems

| Order | Style | Status | Output | Technical check | Notes |
|---:|---|---|---|---|---|
| 04 | Clay / 黏土风 | generated — human text QA pending | `images/04-clay-annotated-v2.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. Contact sheet: `images/batch-03-annotated-contact-sheet-v1.jpg`. |
| 05 | Comic / 漫画 | generated — human text QA pending | `images/05-comic-annotated-v2.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. |
| 06 | Pixel art / 像素艺术 | generated — human text QA pending | `images/06-pixel-art-annotated-v2.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. |

## Batch 4 — elastic cartoon, crude doodle, and baimiao

| Order | Style | Status | Output | Technical check | Notes |
|---:|---|---|---|---|---|
| 10 | Modern color rubber-hose tech cartoon / 现代彩色橡皮管技术卡通 | generated — human text QA pending | `images/10-modern-color-rubber-hose-tech-cartoon-annotated-v1.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. Contact sheet: `images/batch-04-annotated-contact-sheet-v1.jpg`. |
| 11 | Rule-Bound Crude Doodle / 规则化粗糙涂鸦 | generated — human text QA pending | `images/11-rule-bound-crude-doodle-annotated-v2.png` | PASS — PNG, 1672×941, RGB | Uses the revised minimum-necessary-expression grammar and action-driven rough fingers. |
| 12 | Traditional Chinese baimiao realistic lianhuanhua / 传统中国白描写实连环画 | generated — human text QA pending | `images/12-traditional-chinese-baimiao-realistic-lianhuanhua-annotated-v1.png` | PASS — PNG, 1672×941, RGB | Required labels: 发现 / 定位 / 断点 / 接回 / 验证. |

## Retry rule

Record each upstream timeout here before retrying. Do not replace a failed image with an untracked local substitute.
