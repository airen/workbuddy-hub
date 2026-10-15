# Classic Japanese Children’s Manga-Animation Preset

Use this preset only when the user explicitly selects **Classic Japanese children’s manga-animation** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a **locked rendering style** for everyday explanatory and action-led narrative illustration. It is not a generic “anime” filter, not a freely switchable article-level variant, and not a request to imitate any named artist, studio, series, character, logo, or proprietary prop.

```text
IP visual = fixed character identity + classic Japanese children’s manga-animation rendering
```

Lock silhouette, head/body proportion, facial-feature grammar, signature clothing and props, line weight, palette roles, shadow treatment, and composition grammar in `visual-spec.md`; repeat them in `prompt-pack.md`; use the accepted visual master as downstream identity reference.

## What This Preset Is

This preset draws from the broad visual language of classic Japanese children’s manga and television animation: friendly geometric simplification, round or rounded-corner shape design, clean stable contours, bright controlled flat color, restrained cel-style shadows, and a direct everyday problem → action → visible outcome narrative.

It is not “all Japanese anime.” Do not drift toward glossy contemporary anime, idol aesthetics, manga screentone pages, action-shonen dynamism, kawaii mascot chibi styling, or a direct imitation of any recognisable copyrighted work.

## Visual Language

- **Shape and proportion:** rounded, geometric, low-detail silhouette; friendly natural child-to-adult proportions rather than chibi, super-deformed, doll-like, or fashion-anime proportions. A readable head shape, hair/hat silhouette, clothing cut, and one signature prop should identify the IP at article size.
- **Face and expression:** economical features with a small, repeatable expression vocabulary. Emotion comes primarily from eyebrows, mouth shape, head tilt, posture, and action—not oversized sparkling eyes, eyelashes, blush, or ornate facial rendering.
- **Line:** clean, fluent, stable dark contours; modest and purposeful line-weight variation; minimal interior detail; no sketchy pencil texture, dense cross-hatching, manga screentones, or brushy ink wash.
- **Color and light:** a limited high-clarity palette with named, stable roles. Use broad opaque flat fills and at most one restrained cel-shadow plane per major form when needed for separation. Avoid airbrushed gradients, glossy highlights, neon, cinematic bloom, metallic rendering, or complex materials.
- **Composition:** one short, readable causal path. Stage the problem, the IP’s physical action, and the visible result in a single frame, or use a sparse 2–3 beat layout only when temporal change cannot be understood otherwise. Keep backgrounds simple and subordinate.
- **Text:** normally no in-image text. If essential, use one or two short Chinese labels only; do not default to speech bubbles or comic-page dialogue.

## Identity Preservation Rules

Recognition must survive through form and repeatable palette placement, not through an imitation of an existing character:

- head/body silhouette and hair/hat geometry;
- stable feature grammar and expression range;
- signature clothing cut and one practical recurring prop;
- palette roles: background neutral / main garment / secondary garment / dark contour / warm action accent / cool balance accent / skin range;
- controlled flat-fill plus cel-shadow relationship;
- repeatable action vocabulary: inspect, sort, connect, test, explain, compare, repair, guide.

## Best-Fit Use

Use for article inline illustrations and lightweight covers where an abstract topic benefits from approachable, everyday causal storytelling:

- identifying a concrete problem;
- testing a tool or hypothesis;
- sorting choices and revealing priority;
- connecting a broken workflow;
- comparing before/after states;
- explaining a small system through tangible objects.

It is less suitable when the desired communication depends on Chinese folk craft, historical materiality, solemn ceremony, premium editorial restraint, highly realistic anatomy, or dense technical/UI detail.

## Base Style Prompt

```text
Classic Japanese children’s manga-animation inspired original illustration: friendly rounded geometric character design, clean fluent dark contour lines, economical facial features and expressive posture, limited bright harmonious flat-color palette with stable color roles, one restrained cel-shadow plane where necessary, simple lived-in everyday setting, clear article-size readability, and one direct visual causal path from problem through the character’s physical action to a visible result. Original character design only; no text.
```

## Avoid

```text
any named copyrighted character, direct artist or studio imitation, blue round robot cat, magical pocket, bamboo-copter, signature props or costumes from existing franchises, generic “Doraemon style” prompt language, contemporary glossy anime, huge sparkling eyes, long eyelashes, idol fashion, chibi or super-deformed body, kawaii mascot-only pose, manga screentones, comic speech-bubble page, action-shonen speed lines, dense hatching, sketch texture, painterly watercolor, Chinese folk art, lianhuanhua, woodcut, ink wash, 3D render, photorealism, glossy gradients, neon, cinematic bloom, dense UI, decorative icon clouds, a character standing beside an already-complete diagram, text-heavy infographic.
```

## Scene Rules

- The IP must cause the explanatory change. If removing the IP leaves the image’s core meaning intact, the image fails.
- Write the action sentence before every prompt: `The IP is actively [verb] [object] so the reader understands [cognitive anchor].`
- Prefer one concrete everyday friction and one observable result: stalled connection → inspect connector → restored signal; scattered choices → sort cards → clear route.
- Make hands, gaze, prop direction, problem point, and result point form a short reading path.
- Preserve breathing room. Do not fill the background with decorative stars, gears, code, UI panels, or unrelated symbols.
- Keep the character’s practical prop subordinate to the cognitive action, never a magical all-purpose gadget.
- Use the strongest contrast around the action and state change; keep the background and secondary props quieter.

## Style QA Additions

Accept only when all are true:

- The IP is recognisable across visual master and scenes through original silhouette, stable clothes/prop shapes, feature grammar, and palette placement.
- The result reads as a clean, rounded, classic Japanese children’s manga-animation family—not a named-franchise imitation, generic modern anime, chibi/kawaii mascot image, manga page, or glossy digital illustration.
- Lines are clean and economical; color is controlled flat fill with restrained cel shadows, not painterly, heavily shaded, metallic, or gradient-driven.
- At article size, the reader can immediately identify the concrete problem, the IP’s physical action, and the visible outcome.
- The character is indispensable to the scene and actively performs the causal operation.
- The scene remains simple, warm, and everyday without becoming a generic cute figure next to icons.

Reject or revise when the image resembles a named existing character/franchise, becomes generic anime, uses overlarge sparkly eyes or chibi anatomy, substitutes decorative UI/icons for action, adds magical-prop imitation, or makes the IP a passive mascot.