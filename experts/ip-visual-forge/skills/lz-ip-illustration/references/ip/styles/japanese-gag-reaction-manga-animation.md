# Japanese Gag-Reaction Manga-Animation Preset

Use this preset only when the user explicitly selects **Japanese gag-reaction manga-animation** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a **locked rendering style** for exaggerated comic reaction, failed attempts, recovery, and action-led technical storytelling. It is not a generic anime filter, not a per-article mood effect, and not a request to imitate any named character, artist, studio, series, prop, logo, or franchise.

```text
IP visual = fixed character identity + Japanese gag-reaction manga-animation rendering + stable reaction vocabulary
```

Lock silhouette, head/body proportion, facial-feature grammar, signature clothing and props, palette roles, reaction-symbol grammar, line weight, expression range, elastic deformation limits, and composition grammar in `visual-spec.md`; repeat them in `prompt-pack.md`; use the accepted visual master and expression sheet as downstream identity references when supported.

## Why This Preset Exists

The existing **Classic Japanese children’s manga-animation** preset is intentionally clean, warm, rounded, and explanatory. It is good for friendly everyday problem solving, but it suppresses the exaggerated funny reactions that some technical stories need.

This preset keeps the approachable manga-animation readability but restores the comic reaction layer:

- bug-induced panic;
- tool-chain confusion;
- prompt or workflow backfire;
- shocked pause before diagnosis;
- frantic hands-on repair;
- visible relief after the fix works.

The goal is not “cute anime.” The goal is **stable IP identity plus funny, reusable reaction acting**.

## Visual Language

- **Shape and proportion:** rounded, simplified, low-detail character design with stronger squash-and-stretch than the classic children’s preset. Temporary deformation is allowed during reactions, but the base silhouette, clothing, props, and palette must remain recognisable.
- **Face and expression:** build a reusable reaction vocabulary: dot eyes, horizontal-line eyes, blank shock eyes, wide circular shock eyes, triangular or square open mouth, wavy mouth, clenched teeth, flattened face, sweat drops, forehead stress marks, dizzy stars, vertical panic shading, and smoke/steam marks. Avoid sparkly beauty eyes, idol faces, or polished modern anime glamour.
- **Body acting:** elastic arms, springy posture, stumble, recoil, jump-back, frantic reaching, exaggerated pointing, defeated slump, sudden recovery, and relieved exhale. Hands and body must show the technical action, not only the emotion.
- **Line:** clean readable dark contour with occasional comic emphasis lines around reaction moments. Avoid dense screentone pages, heavy hatching, manga panel clutter, or rough low-quality scribble.
- **Color and light:** bright controlled flat color with stable palette roles. Use cel-shadow sparingly. Reaction marks may use one accent color, but do not turn the image into neon, glossy anime, or noisy sticker art.
- **Composition:** one comic beat or a compact 2–3 beat sequence. Stage the technical problem, the IP’s exaggerated reaction, and the recovery or result. The gag must clarify the idea, not replace it.
- **Text:** normally no in-image text. If essential, use one or two short Chinese labels only. Avoid speech bubbles by default; this is an article illustration preset, not a manga-page preset.

## Required Reaction Set

When creating an IP in this preset, generate or define an **8-reaction expression sheet** before calling the IP stable:

1. normal explaining;
2. shock;
3. panic / scramble;
4. speechless / deadpan;
5. smug small win;
6. defeated by bug;
7. refocus / recover;
8. relieved after fix.

Each expression must preserve:

- same head shape and feature grammar;
- same hairstyle/hat geometry;
- same clothing and signature prop relationship;
- same palette roles;
- same line and color treatment.

Reject an expression sheet when the IP turns into eight different characters or when the faces become generic emoji stickers.

## Identity Preservation Rules

Recognition must survive both normal and distorted states:

- base silhouette, head shape, hair/hat geometry;
- feature grammar, including how eyes and mouth transform under stress;
- signature clothing cut and one practical recurring prop;
- stable palette roles: background neutral / main garment / secondary garment / dark contour / reaction accent / action-result accent / skin range;
- allowed deformation range: head squash, mouth enlargement, elastic arms, recoil posture;
- forbidden deformation range: changing species, age, costume, hairstyle, prop family, or becoming a named existing character.

## Best-Fit Use

Use for technical writing, product notes, and workflow stories where the article benefits from humor, self-mockery, or visible failure recovery:

- agent or automation went off track;
- prompt overfit and produced nonsense;
- tool chain broke at one unexpected connector;
- multiple solutions looked correct until tested;
- config, model, dependency, or API behavior surprised the author;
- the IP diagnoses the mess, tries again, and restores a clear route.

It is less suitable for solemn launches, premium brand editorials, cultural craft styles, strict UI walkthroughs, photoreal scenes, or content that needs calm authority rather than comic reaction.

## Base Style Prompt

```text
Japanese gag-reaction manga-animation inspired original illustration: stable rounded original IP character with clean dark contour lines, bright controlled flat colors, reusable exaggerated comic reaction vocabulary, elastic but readable body acting, dot eyes or blank shock eyes, wide open mouth or deadpan mouth as needed, sweat drops and stress marks used sparingly, one everyday technical problem, the IP physically reacts, diagnoses, and changes the situation, compact readable causal composition, article-size clarity. Original character design only; no text.
```

## Avoid

```text
any named copyrighted character, direct artist or studio imitation, Doraemon, blue robot cat, magical pocket, bamboo-copter, signature props or costumes from existing franchises, generic “Doraemon style” prompt language, glossy modern anime, idol aesthetics, beauty eyes, long eyelashes, excessive blush, chibi mascot-only pose, sticker emoji sheet, manga screentone page, dense comic panels, speech-bubble-heavy layout, action-shonen speed-line battle scene, horror grotesque, low-quality scribble, sloppy off-model drawing, photorealism, 3D render, Chinese folk art, lianhuanhua, woodcut, ink wash, dense UI, decorative icon cloud, passive character standing next to a diagram.
```

## Scene Rules

- The reaction must serve the article idea. A funny face without diagnosis, action, or result fails.
- Write the action sentence before every prompt: `The IP is actively [reacting/diagnosing/repairing/testing] [object] so the reader understands [failure mode or recovery].`
- Prefer a three-beat causal structure: `surprise or failure → exaggerated reaction and diagnosis → visible recovery or next test`.
- Keep one main gag per image. Do not stack every reaction mark at once.
- Make hands, gaze, prop direction, reaction marks, problem point, and result point form a short reading path.
- The IP may be temporarily distorted by surprise, but the accepted identity anchors must remain visible.
- Use reaction symbols as punctuation, not decoration. They must point to a state change.

## Style QA Additions

Accept only when all are true:

- The IP is recognisable across normal, shocked, panicked, defeated, and relieved states.
- The expression system feels funny, exaggerated, and reusable, not merely “cute” or politely expressive.
- The result reads as original Japanese gag-reaction manga-animation, not named-franchise imitation, generic modern anime, chibi sticker art, manga page, or glossy digital illustration.
- At article size, the reader can immediately identify the technical problem, the IP’s reaction, the IP’s physical action, and the visible outcome.
- The character remains indispensable to the scene and actively causes the diagnostic or recovery operation.
- The image preserves clean readability; the gag does not bury the explanation.

Reject or revise when the image becomes a specific franchise imitation, loses IP identity during funny faces, uses generic emoji/sticker expressions, replaces action with decoration, or becomes a noisy comic page instead of an article illustration.

## Validation Status

Production-approved preset. Independent validation passed with human visual approval on 2026-07-13.

Validation archive:

```text
references/ip/styles/validation-runs/japanese-gag-reaction-manga-animation-20260713/
```

Validation assets include:

1. one portrait visual master;
2. one 8-reaction expression sheet;
3. one landscape explanation/orchestration scene;
4. one landscape diagnosis/repair/recovery scene;
5. archived prompts, images, dimensions, and `qa-notes.md`;
6. explicit human visual approval.
