# Modern Color Rubber-Hose Tech Cartoon Preset

Use this preset only when the user explicitly selects **Modern color rubber-hose tech cartoon** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a **locked rendering style** for elastic action, tool-chain chaos, tangled workflows, and funny physical recovery scenes. It is not a generic vintage cartoon filter, not a per-article gag overlay, and not a request to imitate any named character, studio, series, mascot, logo, or proprietary cartoon universe.

```text
IP visual = fixed character identity + modern color rubber-hose cartoon rendering + elastic action vocabulary
```

Lock silhouette, head/body proportion, facial-feature grammar, signature clothing and props, palette roles, rubber-hose limb rules, line weight, action-symbol grammar, deformation limits, and composition grammar in `visual-spec.md`; repeat them in `prompt-pack.md`; use the accepted visual master and elastic-action sheet as downstream identity references when supported.

## Why This Preset Exists

Japanese gag-reaction manga-animation solves exaggerated faces and emotional reactions. This preset solves exaggerated **body mechanics**:

- arms stretch like soft cables;
- legs bend with springy rhythm;
- workflow lines knot around the IP;
- buttons, plugs, and tools push back physically;
- bugs behave like small comic pests;
- the IP pulls a tangled process back into one readable route.

The goal is **modern technical storytelling with rubber-hose physical comedy**, not pure 1930s nostalgia.

## Visual Language

- **Shape and proportion:** rounded original character with simplified forms and flexible limbs. Arms and legs may bend in continuous tube-like curves without visible hard joints during action, but the base identity must remain stable.
- **Face and expression:** simple expressive face: dot eyes, oval eyes, arched brows, open mouth, clenched small mouth, dazed face. Expression supports action but should not dominate like the gag-reaction manga preset.
- **Body acting:** stretch, recoil, twist, spring, wobble, get pulled by cables, lasso a runaway bug, yank a workflow straight, bounce away from a bad button, or snap a connector back into place. Hands must still clearly manipulate tools or process objects.
- **Line:** clean dark contour, rounded corners, confident cartoon outline, mild line-weight variation. Avoid scratchy roughness, dense hatching, manga screentones, photoreal render, or dirty vintage film damage.
- **Color and light:** modern bright flat color with stable palette roles. Use limited simple shading only for separation. Avoid pure black-and-white antique cartoon by default; avoid glossy 3D, neon cyberpunk, or over-textured retro paper.
- **Composition:** one visible physical metaphor for a technical issue: tangled cable, runaway prompt card, spring-loaded workflow, tool-chain knot, bug pest, or snapped route. Stage the problem, elastic action, and visible recovery in one frame.
- **Text:** normally no in-image text. If essential, use one or two short Chinese labels only. Avoid speech bubbles and comic strip layouts by default.

## Required Elastic Action Set

When creating an IP in this preset, generate or define a small **elastic action sheet** before calling the IP stable:

1. neutral explaining stance;
2. arm stretched to grab a loose connector;
3. body recoiling from a bad button;
4. tangled in cable/workflow line;
5. pulling a knot straight;
6. catching a small bug pest;
7. springing back into balance;
8. proudly presenting a restored route.

Each action must preserve:

- same head shape and feature grammar;
- same hairstyle/hat geometry;
- same clothing and signature prop relationship;
- same palette roles;
- same clean dark contour and flat-color treatment.

Reject an action sheet when the IP turns into unrelated rubber figures, loses clothing/prop identity, or becomes an old black-and-white franchise imitation.

## Identity Preservation Rules

Recognition must survive elastic deformation:

- base silhouette, head shape, hair/hat geometry;
- feature grammar and expression range;
- signature clothing cut and one practical recurring prop;
- stable palette roles: background neutral / main garment / secondary garment / dark contour / warm action accent / cool result accent / skin range;
- allowed deformation range: stretched arms, bent tube limbs, springy posture, squash-and-stretch torso during action;
- forbidden deformation range: changing species, age, costume, hairstyle, prop family, or becoming a named existing character.

## Best-Fit Use

Use for technical writing, workflow explanation, product notes, and debugging stories where the article benefits from physical comedy and visible process mechanics:

- tool chains tangled together;
- automation pulls the user off track;
- prompt cards bounce back or scatter;
- APIs, connectors, or model calls behave like elastic cables;
- bug pests run away from the IP;
- a messy route gets pulled straight;
- a broken connector snaps back into place.

It is less suitable for solemn launches, premium editorial restraint, Chinese nostalgic craft styles, highly realistic anatomy, calm explanation with no physical conflict, or precise UI walkthroughs.

## Base Style Prompt

```text
Modern color rubber-hose tech cartoon original illustration: stable rounded IP character with clean dark contour lines, bright modern flat colors, flexible tube-like arms and legs, elastic squash-and-stretch body acting, funny physical workflow metaphor, one technical problem made tangible through tangled cables or runaway tools, the IP physically pulls, grabs, twists, catches, or snaps the process back into a clear route, simple readable composition, article-size clarity. Original character design only; no text.
```

## Avoid

```text
any named copyrighted character, direct artist or studio imitation, Mickey Mouse, Felix the Cat, Cuphead, Bendy, Betty Boop, black-and-white vintage franchise imitation, pie-cut eyes as a franchise cue, white gloves as a required signature, generic old cartoon filter, film grain damage, rubber-hose style without modern tech context, horror mascot, creepy pasta, glossy 3D, photorealism, generic anime, manga screentones, Chinese folk art, lianhuanhua, woodcut, ink wash, dense UI, decorative icon cloud, passive character standing next to a diagram, funny limbs that do not explain a technical problem.
```

## Scene Rules

- The elastic action must clarify the article idea. Stretchy limbs without process mechanics fail.
- Write the action sentence before every prompt: `The IP is actively [stretching/pulling/untangling/catching/snapping] [workflow object] so the reader understands [technical failure or recovery].`
- Prefer a three-part causal frame: `tangle or runaway tool → elastic physical action → clean route/result`.
- Keep one main physical gag per image. Do not stack every cable, bug, button, and spring at once.
- Make hands, stretched limb path, cable/tool direction, problem point, and result point form a short reading path.
- The IP may stretch, bend, or squash, but accepted identity anchors must remain visible.
- Use modern tech props and clean color to avoid drifting into pure antique cartoon nostalgia.

## Style QA Additions

Accept only when all are true:

- The IP is recognisable across neutral and elastic action states.
- The result clearly reads as modern color rubber-hose tech cartoon, not a named vintage franchise imitation or generic retro filter.
- The body action is more elastic and physical than ordinary cartoon posing.
- At article size, the reader can immediately identify the technical problem, the IP’s elastic physical action, and the visible outcome.
- The character remains indispensable to the scene and actively causes the recovery operation.
- The gag does not bury the explanation.

Reject or revise when the image becomes pure nostalgia, named-character-adjacent, creepy mascot art, passive decoration, or stretchy action with no technical cause/effect.

## Validation Status

Production-approved preset. Independent validation passed with human visual approval on 2026-07-13.

Validation archive:

```text
references/ip/styles/validation-runs/modern-color-rubber-hose-tech-cartoon-20260713/
```

Validation assets include:

1. one portrait visual master;
2. one optimized reference image for downstream image-to-image calls;
3. one elastic action sheet;
4. one landscape explanation/orchestration scene;
5. one landscape diagnosis/repair/recovery scene;
6. archived prompts, images, dimensions, reference optimization notes, and `qa-notes.md`;
7. explicit human visual approval.
