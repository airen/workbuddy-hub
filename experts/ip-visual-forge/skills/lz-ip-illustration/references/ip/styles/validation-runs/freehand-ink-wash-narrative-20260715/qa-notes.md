# Freehand Ink-Wash Narrative Candidate — Smoke Test Notes

- Date: 2026-07-15
- Preset: Freehand Ink-Wash Narrative / 写意水墨叙事
- Status: candidate; **not production-approved**.
- Scope: one portrait visual-master smoke test only. This confirms the installed skill resolves the new preset and the image-generation path can produce an archived candidate output. It is not a substitute for the mandatory independent validation set.

## Artifacts

| ID | File | Purpose | Automated check |
|---|---|---|---|
| 01 | `images/01-ink-route-restorer-visual-master-smoke-v1.png` | temporary Ink Route Restorer visual master | PASS — PNG, 1024×1536, RGB; decoded with Pillow |
| 02 | `images/02-ink-route-orchestration-explanation-v1.png` | explanation/orchestration scene attempt | PASS — PNG, 1672×941, RGB; decoded with Pillow. The local visual master was serialized as a `data:image/png;base64,...` source in a logged `is_edit: true` request. Original `modality: text` was a plugin response-label bug, corrected on 2026-07-15. |
| 03 | `images/03-ink-route-diagnosis-repair-v1.png` | diagnosis/repair scene attempt | PASS — PNG, 1672×941, RGB; decoded with Pillow. The local visual master was serialized as a `data:image/png;base64,...` source in a logged `is_edit: true` request. Original `modality: text` was a plugin response-label bug, corrected on 2026-07-15. |
| — | `images/freehand-ink-wash-narrative-validation-contact-sheet-v1.jpg` | three-image human-review sheet | PASS — JPEG, 1912×464, RGB; decoded with Pillow. |

## Human Review

- The visual master was explicitly approved by the user on 2026-07-15.
- The two landscape outputs are valid image-to-image attempts: plugin debug logs prove the local visual master was attached as a base64 data URI. Their visual style and identity still require human review against the desired anchor; a correct transport path does not itself establish a pass.
- Preset status remains **candidate** pending visual approval of the complete three-image set.

## Remaining Gate

1. Review scenes 02 and 03 against the approved visual master for identity stability, style differentiation, ink-value hierarchy, article-size legibility, and causal-action clarity.
2. Revise/regenerate any image that visually drifts, then update the contact sheet and QA notes.
3. Obtain explicit human approval of the completed valid set before promotion.

Do not use this temporary test IP as a production IP unless separately approved.
