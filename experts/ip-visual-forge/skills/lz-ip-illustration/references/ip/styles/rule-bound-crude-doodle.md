# Rule-Bound Crude Doodle Preset

Use this preset only when the user explicitly selects **Rule-Bound Crude Doodle** / **规则化粗糙涂鸦** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Validation Status

**Production-approved preset.** Independent source-faithful validation passed on 2026-07-15 with a 文人 Agent portrait visual master, the original Direction 09 repair anchor, one non-technical landscape transformation scene, archived prompts/assets, automated decode checks, and explicit human visual approval. Validation archive: `references/ip/styles/validation-runs/rule-bound-crude-doodle-20260715/`.

## Position in the IP System

This is a locked modern expressive rendering style, not an interchangeable article-level filter.

```text
IP visual = fixed character identity + rule-bound crude doodle rendering
```

Lock silhouette, facial asymmetry range, contour-error grammar, hand grammar, limb-proportion range, palette roles, object simplification rules, and action silhouette in `visual-spec.md`. Repeat these locks in `prompt-pack.md`; use an accepted visual master as downstream identity reference when image-to-image support is verified.

## What This Preset Is

Rule-Bound Crude Doodle is deliberately crude, but never random. It should look as if a person with no formal art training used a thick black marker to make the scene understandable with the fewest useful marks. Its inaccuracies are stable style tendencies: overshot line endings, double-traced contours, lopsided head construction, eyes at slightly different heights, rough action-driven hands or short irregular fingers, inconsistent limb length, and crudely simplified objects or machines.

The action silhouette and causal story must remain immediately readable. This is not a generic “rough sketch” or a tasteful editorial doodle. Complexity is removed before rendering: if deleting a line, local detail, or object does not weaken the action, causal relation, outcome, or minimum IP recognition, delete it.

## Visual Language

- **Line:** thick black marker, strongly uneven weight, overshot ends, double-traced contours, visible restarts and overlaps. Use only marks needed for the action, outcome, or minimum identity anchor. Never clean vector outlines with cosmetic wobble.
- **Face and body:** lopsided head; slight, stable facial asymmetry; eyes can sit at different heights; limbs may differ in length or bend awkwardly. Hands are action-driven and rough: a mitten-like lump, 2–4 short uneven finger strokes, a forked grab, or another crude mark is allowed when it makes grasping, pulling, pointing, or supporting legible. Do not require a fixed hand shape; do not render clean anatomy, articulated joints, or carefully counted fingers.
- **Objects:** reduce every prop or machine to the fewest blunt shapes that preserve its role in the scene. A prop may have one distinguishing mark only when needed for IP recognition or causal action. No keyboard keys, page stacks, stitching, clothing folds, UI internals, machine parts, texture, shading, or decorative fill unless removing that mark would make the scene unreadable.
- **Color:** white or pale paper ground; black as dominant line; only tiny functional indigo, red, and green accents. Color communicates a state or action, not decoration.
- **Composition:** begin with one crystal-clear physical action and its minimum causal counterpart. The scene can be asymmetrical and crowded locally, but must not become random scribble chaos, a neat dashboard, or a pile of identity props.
- **Tone:** anti-cute, anti-polished, anti-refined. Awkwardness is intentional but may be unevenly distributed, like a casual untrained doodle rather than a repeated typeface effect.
- **Text:** no readable text unless a later explicit scene requirement overrides this; never use tiny labels as a substitute for visible causality.

## Identity Preservation Rules

Recognition must survive through the crude rendering:

- retain the selected IP’s silhouette and only the minimum clothing/prop anchors needed for recognition in this scene; do not reproduce every signature item by default;
- repeat the same broad contour-error tendency and awkwardness range across scenes, while allowing hands, line restarts, overshoots, and local asymmetry to vary naturally with the action;
- keep an action silhouette readable before decorative marks;
- use accent colors only for functional states, such as fault, connection, trace, or success;
- preserve the allowed roughness range; do not drift into a cute mascot, polished cartoon, detailed rough illustration, or illegible chaos.

## Best-Fit Use

- personal-brand covers and inline scenes with an independent, anti-polished point of view;
- diagnosis, repair, comparison, and transformation stories where physical action must be instantly legible;
- opinion pieces, maker notes, and practical articles that benefit from a deliberately unvarnished visual voice;
- playful social cards where the character remains recognisable without becoming cute.

It is less suitable for premium corporate branding, dense diagrams, small-label-heavy explanations, photorealistic material rendering, formal traditional art, or emotionally soft/cute character storytelling.

## Base Style Prompt

```text
Rule-bound crude doodle illustration, original recurring IP character, intentionally very rough thick black marker drawing by someone with no formal art training. First reduce the scene to the minimum marks that make the action, causal relation, outcome, and minimum IP recognition clear; omit every other detail. Strongly uneven hand-drawn lines, some overshot ends, some double-traced contours, lopsided head, eyes at slightly different heights, rough action-driven hands that may use a lump or 2–4 short uneven finger strokes, inconsistent limb length, and blunt primitive prop shapes. The errors feel casually uneven rather than mechanically repeated, while the physical action silhouette and causal story remain crystal clear. White or pale paper background; only tiny functional indigo, red, and green accents. No texture, clothing folds, prop internals, UI detail, hatching, shading, refined vector geometry, random scribble chaos, readable text, or imitation of any named artist, studio, character, or franchise.
```

Add the content action separately. Do not require engineering props or repair metaphors unless the requested scene actually needs them.

## Avoid

```text
polished editorial doodle, tasteful hand-drawn illustration, soft hand-filled color blocks, cute mascot, childlike character, generic sketchnote, neat modular infographic, dense dashboard, clean vector geometry, uniform perfect contours, manga/anime, rubber-hose limbs, photorealism, 3D render, ornate decoration, random illegible scribbling, named-work imitation
```

## Scene Rules

- Write one concrete physical action sentence before every prompt.
- Make the action read from silhouette and object relationship, not labels.
- Keep faults, traces, connections, choices, or outcomes visually functional when the topic calls for them.
- Before rendering, apply the deletion test: remove every line, local detail, object, or identity prop that does not change action clarity, causal relation, outcome, or minimum recognition.
- Apply the same blunt, low-information grammar to character and props. Hands may be crude lumps or a few irregular finger strokes when the action needs them; never turn them into polished anatomy.
- Do not repair the intended roughness with symmetry, polished color blocks, cute expressions, clean geometry, internal prop detail, shading, hatching, or decorative texture.

## Style QA Additions

Accept only when all are true:

- The image reads as Rule-Bound Crude Doodle, not polished freeform doodle, sketchnote, cute cartoon, or random scribble.
- Thick uneven lines, overshot ends, double contours, facial asymmetry, action-appropriate crude hands (including optional short irregular fingers), limb inconsistency, and a low-information object grammar are visibly present without becoming a mechanical checklist.
- The IP stays recognisable and the primary action reads immediately.
- The image remains anti-cute and anti-polished without becoming visually broken or unreadable.
- Accent colors are rare and functional.
- Removing nonessential visual information would not make the scene clearer; props, clothing, and systems have already been reduced to the minimum necessary marks.

Reject or revise when the model cleans up the linework, makes the character cute/symmetrical, turns the result into a refined editorial illustration, or loses action causality in chaotic marks.
