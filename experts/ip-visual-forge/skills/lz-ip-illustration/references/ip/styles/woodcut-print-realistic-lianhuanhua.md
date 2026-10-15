# Woodcut-Print Realistic Lianhuanhua Style Preset

Use this preset only when the user explicitly selects **Woodcut-print realistic lianhuanhua** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a **locked rendering style**, not a generic folk-art texture, not a revolutionary-poster shortcut, and not a freely switchable article-level variant.

For an IP using this preset:

```text
IP visual = fixed character identity + Woodcut-print realistic lianhuanhua rendering
```

Lock the silhouette, black-white mass placement, signature props, and carving-mark direction in `visual-spec.md`; repeat them in `prompt-pack.md`; use the accepted visual master as the identity reference for downstream scenes.

Do not mix this preset with Traditional Chinese baimiao, pen-and-ink realistic lianhuanhua, gongbi line-and-color, freehand ink-wash, Japanese manga, American comics, glossy digital illustration, propaganda poster art, vintage poster art, game concept art, or generic "Chinese style" rendering unless the user explicitly revises the entire IP visual system.

## Difference from the Other Lianhuanhua Presets

| Dimension | Woodcut-print realistic lianhuanhua | Traditional Chinese baimiao | Pen-and-ink realistic lianhuanhua | Gongbi line-and-color realistic lianhuanhua |
|---|---|---|---|---|
| Primary mark | carved black-white mass and directional knife cuts | restrained brush-like monochrome contour | crisp technical-pen contour and hatching | fine ink outline containing restrained color |
| Tone | high-contrast planes and carved texture | economical line density | hatching, cross-hatching, stippling, white reserve | color value steps and fine interior lines |
| Detail strategy | simplify into readable carved forms | fine contour and garment line | observational pen-built detail | meticulous line-and-color detail |
| Visual feeling | bold, tactile, forceful, collective | airy, flowing, line-led | structural, observational, slightly graphic | meticulous, calm, luminous, orderly |

Do not use another preset's prompt block, reference image, or QA result as evidence that this preset has passed.

## Visual Language

- Medium: black-and-white realistic Chinese lianhuanhua rendered as a carved woodcut print.
- Form: recognizably realistic human proportions and meaningful hand/face/gesture construction, simplified into strong planes rather than photographic detail.
- Mark-making: deliberate directional knife-cut lines and carved bands follow form, light direction, material, and movement. Marks must feel cut from a block, not scribbled with a pen.
- Tone: strong black-white mass organization with limited midtone created by carved line density. Use decisive white-paper cuts and black areas; avoid smooth grayscale, airbrushing, or photographic shading.
- Composition: one self-contained narrative moment with a bold, readable silhouette and immediate action. A local 2-4 panel sequence is allowed only when temporal change is essential.
- Texture: visible print grain and light irregularities are allowed only when they support the carved medium and do not obscure faces, hands, tools, or action.
- Text: normally no in-image text. When necessary, use only short Chinese labels; do not use speech balloons as the default narrative device.

## Identity Preservation Rules

The rendering is monochrome and detail-compressed, so preserve recognition through structural anchors:

- head and face silhouette
- body proportion and characteristic stance
- signature clothing shape, cap/hat, collar, or accessory outline
- signature object silhouette and grip
- fixed placement of the major black, white, and carved-midtone masses
- repeatable gesture vocabulary

Record a black-white mass map in `visual-spec.md`:

```text
background white reserve / primary dark silhouette area / secondary dark anchor / carved-midtone direction / signature prop contrast / face readability reserve
```

Do not rely on tiny facial details, color, decorative patterns, or incidental print noise to identify the IP.

## Prompt Block

Use this in the Base Style Prompt and adapt it to the scene:

```text
Woodcut-print realistic Chinese lianhuanhua illustration, black-and-white late-20th-century serialized picture-book print; realistic human proportions simplified into bold carved planes, decisive black-white mass composition, directional knife-cut bands and carved line texture following form and movement, controlled print grain, readable face and hands, strong narrative silhouette, high legibility at article size.
```

## Negative Prompt Block

```text
revolutionary propaganda poster, heroic raised-fist political poster, generic folk-art icon, flat decorative stamp, Japanese manga or anime, American superhero comic, chibi or kawaii cartoon, glossy digital painting, 3D render, smooth grayscale, photorealistic photo, pen-and-ink hatching drawing, baimiao brush line, gongbi color painting, freehand ink-wash, colorful image, neon palette, distressed photocopy texture, random scratches, illegible face, dense text, speech bubbles, fantasy game concept art.
```

## Scene Rules

- The IP must perform the explanatory action; forceful texture cannot substitute for clear narrative participation.
- Prefer one bold narrative moment rather than a crowded poster or full-page infographic.
- Use black-white mass hierarchy to separate the IP, core action, and supporting objects; keep faces, hands, and signature tools readable through white reserve.
- For workflow/comparison/diagnosis scenes, turn relationships into physical connections, separations, breaks, repairs, or directional movement that the carved composition can show clearly.
- Use 2-4 panels only when sequence is necessary; retain clear block separation and enough white reserve in every panel.
- Keep modern tools or interfaces visually simplified; do not turn the scene into literal software UI, political poster art, or generic industrial decoration.

## Style QA Additions

Accept only when all are true:

- The character remains recognizable through silhouette, stance, signature prop shape, and stable black-white mass placement.
- The result reads as realistic woodcut-print lianhuanhua, not a propaganda poster, folk-art icon, rough stamp, ink drawing, manga, or glossy digital illustration.
- Carved marks follow material, form, light, or movement; they do not become random scratches, evenly striped texture, or unreadable visual noise.
- The black-white contrast creates a clear focal hierarchy and preserves face, hand, tool, and action readability at intended article or card size.
- Anatomy, hands, perspective, and spatial relations remain credible despite simplified planes.
- The image has one intelligible narrative action and does not become a slogan-like, crowded, or ornamental composition.

Reject or revise when a heroic-poster pose, political symbols, decorative folk patterns, generic black-and-white stamping, excessive grain, or heavy black fill overwhelms the cognitive anchor or erases identity.
