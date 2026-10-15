# Rule-Bound Crude Doodle — QA Handoff

## Status

Production validation passed on 2026-07-15 after explicit human visual approval.

## Assets

| # | File | Role | Automated file result |
|---|---|---|---|
| 01 | `images/01-wenren-agent-crude-doodle-visual-master-v1.png` | portrait test of 文人 Agent identity plus crude-error grammar | PASS — RGB, 1024×1536 |
| 02 | `images/02-original-direction-09-repair-anchor-v1.png` | original successful Direction 09 repair anchor; copied unchanged | PASS — RGB, 1672×941 |
| 03 | `images/03-wenren-agent-nontechnical-transformation-v1.png` | non-engineering test of the same grammar | PASS — RGB, 1672×941 |
| — | `images/rule-bound-crude-doodle-validation-contact-sheet-v1.jpg` | side-by-side visual review | PASS — RGB, 2280×790 |

## Prompt provenance

- 01 prompt: `prompts/01-portrait-visual-master.md`
- 02 prompt: `prompts/02-original-direction-09-repair-anchor.md` — exact original Direction 09 prompt copied from the nine-grid exploration run.
- 03 prompt: `prompts/03-nontechnical-transformation.md`
- Candidate locks: `candidate-brief.md`

## Provider observation

The two newly generated images were given the current 文人 Agent visual-master file path as `image_url`, but both tool receipts reported `modality: text`. Treat the prompt-level style test as valid, but do not claim verified image-to-image identity transmission from those receipts.

## Human visual gate

Approve only if:

1. 01 and 03 visibly share Direction 09’s rule-bound crude grammar, rather than the earlier polished Freeform Doodle direction.
2. Thick uneven line, overshot end, double contour, lopsided face, uneven eyes, action-appropriate crude hands or simple irregular fingers, limb inconsistency, minimum-necessary object grammar, and anti-cute tone are all visibly present without becoming a mechanical checklist.
3. 文人 Agent remains recognisable enough through the distortion.
4. 03 demonstrates that the style works without technical props or an engineering plot.
5. The action stays clear before visual ornament.

**Promotion passed.** The user explicitly approved this source-faithful validation set on 2026-07-15. Rule-Bound Crude Doodle is production-approved; archive this run as its production validation record. The `modality: text` observation remains a documented image-reference transport limitation, not a reason to negate the human-approved rendering-style result.
