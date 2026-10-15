# QA Notes

Preset: Japanese gag-reaction manga-animation
Status: human visual QA approved on 2026-07-13

## Generated Assets

| Asset | Format / Mode / Size | Notes |
|---|---|---|
| `reference-images/bug-panic-mechanic-visual-master-v1.png` | PNG / RGB / 1024×1536 | decoded successfully |
| `expression-sheet/images/bug-panic-mechanic-8-reactions-v1.png` | PNG / RGB / 887×1774 | decoded successfully |
| `article-runs/prompt-backfire/images/01-prompt-backfire-sort-route.png` | PNG / RGB / 1823×863 | decoded successfully |
| `article-runs/connector-panic-repair/images/01-loose-connector-panic-repair.png` | PNG / RGB / 1536×1024 | decoded successfully |

## Validation Checklist for Human Review

- Same temporary IP across all assets: short messy black hair with left hook, teal work jacket, cream shirt with red warning patch, mustard belt, coral clipboard, mint connector tester.
- Expression sheet contains a reusable reaction vocabulary: normal, shock, panic, deadpan, smug, defeated, refocus, relieved.
- Funny/gag reaction is visibly stronger than the existing classic Japanese children’s manga-animation preset.
- Scenes show problem → exaggerated reaction → physical diagnosis/repair/sorting → visible result.
- No named-franchise imitation, no blue robot cat, no magical pocket, no speech-bubble manga page, no glossy modern anime.

## Machine Verification

All PNGs decoded successfully with PIL. Expression sheet came back as a vertical 2×4 sheet despite landscape request; content still serves the required 8-reaction validation role.

## Human Gate

Approved by user on 2026-07-13. Preset may be marked production-approved. Test IP remains temporary.
