# Gongbi Line-and-Color Realistic Lianhuanhua Style Preset

Use this preset only when the user explicitly selects **Gongbi line-and-color realistic lianhuanhua** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a **locked rendering style**, not a one-off "Chinese-style" color treatment and not a freely switchable article-level variant.

For an IP using this preset:

```text
IP visual = fixed character identity + Gongbi line-and-color realistic lianhuanhua rendering
```

Lock the exact line treatment, palette roles, and signature color placement in `visual-spec.md`; repeat them in `prompt-pack.md`; use the accepted visual master as the identity reference for downstream scenes.

Do not mix this preset with black-and-white Traditional Chinese baimiao, pen-and-ink realistic lianhuanhua, freehand ink-wash, woodcut, Japanese manga, American comics, glossy digital Chinese-fantasy illustration, vintage poster art, game concept art, or generic "Chinese style" rendering unless the user explicitly revises the entire IP visual system.

## Difference from the Other Lianhuanhua Presets

| Dimension | Gongbi line-and-color realistic lianhuanhua | Traditional Chinese baimiao | Pen-and-ink realistic lianhuanhua |
|---|---|---|---|
| Primary mark | precise fine outline plus color contained by the line | restrained brush-like monochrome contour | crisp technical-pen monochrome contour |
| Color | controlled layered flat color and light glazing | black-and-white only | black-and-white only |
| Tone | formed through color value steps and restrained line detail | economical hatching and line density | hatching, cross-hatching, stippling, white reserve |
| Visual feeling | meticulous, calm, luminous, orderly | airy, flowing, line-led | structural, observational, slightly graphic |

Do not use another preset's prompt block, reference image, or QA result as evidence that this preset has passed.

## Visual Language

- Medium: realistic Chinese lianhuanhua rendered with gongbi-style fine outlines and controlled color.
- Linework: precise, even-to-subtle-variable ink outlines that clearly contain forms; delicate interior lines describe facial features, hands, garment seams, and important object structure.
- Color: thin, layered flat color and light glazing inside clean outlines. Use a limited, harmonious palette with distinct roles: base, secondary, dark anchor, accent, and neutral background.
- Tone and material: create volume through restrained value steps, layered color, and fine line detail. Do not use glossy airbrush gradients, oil-paint thickness, dramatic bloom, or photorealistic texture.
- Figure drawing: credible, proportionate bodies and hands; observed faces; dignified, readable gestures.
- Composition: one self-contained narrative moment; clear, calm spatial organization; a local 2-4 panel sequence is allowed only when temporal change is essential.
- Texture: light xuan-paper or silk-like paper texture is optional and must remain subordinate to clear linework and color fields.
- Text: normally no in-image text. When necessary, use only short Chinese labels; do not use speech balloons as the default narrative device.

## Identity Preservation Rules

Color is a first-class identity constraint for this preset. Preserve recognition through both form and fixed palette placement:

- head and face silhouette
- body proportion
- signature clothing cut, collar, hat, glasses, or accessory shape
- signature object or motif
- palette roles and exact placement of the primary color, dark anchor, and accent
- repeatable gesture vocabulary

Record the palette in `visual-spec.md` with named roles, not only loose color names:

```text
background neutral / main garment color / secondary garment color / dark contour-anchor / signature-prop accent / skin tone range
```

Use color to support hierarchy. Do not use color alone to rescue a weak silhouette or make every object equally saturated.

## Prompt Block

Use this in the Base Style Prompt and adapt it to the scene:

```text
Gongbi line-and-color realistic Chinese lianhuanhua illustration, fine controlled ink outlines enclosing carefully layered restrained color; realistic anatomy, dignified facial features, precise hands and clothing folds; limited harmonious palette with stable color roles, delicate interior line detail, light color glazing and measured value steps, calm cinematic narrative composition, clear foreground-midground-background depth, high legibility at article size, subtle xuan-paper texture only.
```

## Negative Prompt Block

```text
black-and-white baimiao rendering, pen-and-ink hatching-only drawing, freehand ink-wash, woodcut print, Japanese manga or anime, American superhero comic, chibi or kawaii cartoon, glossy digital Chinese-fantasy painting, 3D render, photorealistic photo, thick impasto oil paint, neon colors, oversaturated rainbow palette, smooth airbrushed gradients, heavy gold decoration, propaganda poster, calendar-poster woman, fantasy game concept art, speech bubbles, dense text, fake calligraphy, cluttered ornamental background.
```

## Scene Rules

- The IP must perform the explanatory action; decorative costume and color cannot replace narrative participation.
- Prefer one clear narrative moment rather than a crowded poster or a full-page infographic.
- Reserve the strongest color contrast for the IP action, central object, or diagnostic change; supporting props use quieter values.
- For workflow/comparison/diagnosis scenes, show relationships through objects, gesture, spatial order, and short labels only when essential.
- Use 2-4 panels only when a sequence is necessary; retain generous visual separation and a stable palette across panels.
- Keep modern tools or interfaces visually simplified; do not turn the scene into a costume drama, glossy game art, or literal software UI.

## Style QA Additions

Accept only when all are true:

- The character remains recognizable through both silhouette and stable color placement.
- The result reads as fine-line gongbi color lianhuanhua, not generic colorful Chinese-fantasy illustration, ink wash, manga, poster art, or digitally airbrushed concept art.
- Fine outlines remain visible and contain the color fields; clothing, hands, face, and core props do not dissolve into smooth painted blobs.
- Palette roles are restrained, repeatable, and support focal hierarchy; saturation is controlled and non-decorative.
- Anatomy, hands, clothing folds, perspective, and spatial relations are coherent.
- The image has one intelligible narrative action and does not become an ornamental, crowded, or text-heavy illustration.

Reject or revise when thick glossy painting replaces line-and-color construction, colors shift between scenes without an allowed rule, gold/red ornament overwhelms the cognitive anchor, outlines disappear under gradients, or the IP becomes a decorative ancient-costume figure.
