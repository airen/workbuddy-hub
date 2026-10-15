# QA Notes

Preset: Modern color rubber-hose tech cartoon
Status: human visual QA approved on 2026-07-13

## Generated Assets

| Asset | Format / Mode / Size | Size MB | Notes |
|---|---|---:|---|
| `reference-images/cable-juggler-visual-master-v1.png` | PNG / RGB / 1024×1536 | 1.773 | decoded successfully |
| `reference-images/optimized/cable-juggler-visual-master-v1-ref-1024-q85.jpg` | JPEG / RGB / 683×1024 | 0.079 | decoded successfully |
| `action-sheet/images/cable-juggler-elastic-action-sheet-v1.png` | PNG / RGB / 1536×1024 | 1.709 | decoded successfully |
| `article-runs/workflow-knot-untangle/images/01-workflow-knot-untangle.png` | PNG / RGB / 1717×916 | 1.744 | decoded successfully |
| `article-runs/bug-pest-connector-snap/images/01-loose-connector-snap-back.png` | PNG / RGB / 1672×941 | 1.402 | decoded successfully |

## Validation Checklist for Human Review

- Same temporary IP across all assets: comma-curl dark hair, cobalt blue jacket, warm white shirt with orange lightning patch, olive belt, red-orange cable hook, mint route spool.
- Body mechanics read as rubber-hose: elastic arms, tube-like bends, stretched pulling/grabbing, springy action.
- Scenes show technical cause/effect: tangled workflow → elastic pull → clean route; loose connector → stretched hook action → restored signal.
- Style reads as modern color rubber-hose tech cartoon, not pure black-and-white nostalgia, named vintage franchise imitation, creepy mascot, or generic retro poster.
- IP is necessary to the scene; removing the IP should break the explanation.

## Reference Optimization

Original visual master: 1.773 MB. Optimized reference: 0.079 MB. Reduction about 95.5%. The optimized reference was used for action sheet and scene generations.

## Timeout Notes

- Original long visual-master prompt timed out once; shorter visual-master prompt succeeded.
- Connector scene with bug pest timed out twice even with optimized reference. Simplified connector-only recovery prompt succeeded.
- Conclusion: compression reduces payload overhead but does not fully solve long/complex generation-side timeout risk.

## Human Gate

Approved by user on 2026-07-13. Preset may be marked production-approved. Test IP remains temporary.
