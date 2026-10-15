# Pen-and-Ink Realistic Lianhuanhua Style Preset

Use this preset only when the user explicitly selects **Pen-and-ink realistic lianhuanhua** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a **locked rendering style**, not a one-off monochrome filter and not a freely switchable article-level variant.

For an IP using this preset:

```text
IP visual = fixed character identity + Pen-and-ink realistic lianhuanhua rendering
```

Lock it in `visual-spec.md`, repeat it in `prompt-pack.md`, and use the accepted visual master as the identity reference for downstream scenes.

Do not mix this preset with Traditional Chinese baimiao, woodcut, ink-wash, gongbi color painting, Japanese manga, American comics, vintage poster art, game concept art, or generic "Chinese style" rendering unless the user explicitly revises the entire IP visual system.

## Difference from Traditional Chinese Baimiao

Both presets are black-and-white realistic Chinese lianhuanhua traditions, but they are not interchangeable:

| Dimension | Pen-and-ink realistic lianhuanhua | Traditional Chinese baimiao realistic lianhuanhua |
|---|---|---|
| Primary mark | decisive steel-pen or technical-pen line | restrained brush-like ink contour line |
| Tone | more explicit line-density modeling | lighter, more economical tonal suggestion |
| Texture | hatching, cross-hatching, selective stippling | controlled contour, selective fine hatching |
| Visual feeling | crisp, structural, observational, slightly graphic | elegant, flowing, line-led, more airy |

Do not use one preset's prompt block, reference image, or QA result as evidence that the other preset has passed.

## Visual Language

- Medium: black-and-white Chinese realistic lianhuanhua rendered as a pen-and-ink drawing.
- Linework: crisp, deliberate pen contours with controlled variation; fine hatching, cross-hatching, and selective stippling build form, material, and depth.
- Figure drawing: credible, proportionate bodies and hands; observed facial planes; expressive but restrained faces; readable gestures.
- Light and space: clear light direction and stronger grayscale modeling than the baimiao preset, achieved strictly through line weight, line density, and white paper reserve rather than smooth digital gradients.
- Composition: one self-contained narrative moment; cinematic, legible framing; a local 2-4 panel sequence is allowed only when temporal change is essential.
- Texture: very subtle paper grain is optional. Pen marks must remain clean; do not fake aging, photocopy noise, or distressed retro print.
- Text: normally no in-image text. When necessary, use only short Chinese labels; do not use speech balloons as the default narrative device.

## Identity Preservation Rules

The rendering is monochrome, so preserve recognition through non-color anchors:

- head and face silhouette
- body proportion
- signature clothing cut, collar, hat, glasses, or accessory shape
- signature object or motif
- stable light, midtone, and dark placement
- repeatable gesture vocabulary

Record a grayscale mapping in the visual spec. Use white paper reserve for the light identity area, controlled hatching for midtone areas, and dense pen black for the dark anchors. Do not rely on hue alone to distinguish the IP.

## Prompt Block

Use this in the Base Style Prompt and adapt it to the scene:

```text
Pen-and-ink realistic Chinese lianhuanhua illustration, black-and-white late-20th-century serialized picture-book line art; crisp controlled steel-pen contours, realistic anatomy and observed clothing folds, disciplined hatching, cross-hatching, and selective stippling for clear tonal modeling, deliberate white-paper reserve, cinematic narrative composition, readable foreground-midground-background depth, high legibility at article size.
```

## Negative Prompt Block

```text
Traditional Chinese baimiao brush-line rendering, Japanese manga or anime, American superhero comic, chibi or kawaii cartoon, glossy digital painting, 3D render, smooth airbrushed grayscale, colorful gongbi painting, freehand ink-wash, woodcut print, propaganda poster, calendar-poster woman, fantasy game concept art, photorealistic photo, speech bubbles, dense text, random scribbles, muddy hatching, faux distressed retro print.
```

## Scene Rules

- The IP must perform the explanatory action; action clarity outranks rendering density.
- Prefer one clear narrative moment rather than a crowded poster or a full-page infographic.
- Use contrast and pen-line hierarchy to separate the IP, core object, and supporting structure.
- For workflow/comparison/diagnosis scenes, show relations through objects, gesture, framing, and short labels only when essential.
- Use 2-4 panels only when sequence is necessary; preserve enough white space for each moment to read.
- Keep modern tools or interfaces visually simplified; do not turn the image into a photorealistic UI or a costume drama.

## Style QA Additions

Accept only when all are true:

- The character remains recognizable in black and white without depending on color.
- The result reads as crisp pen-and-ink realistic lianhuanhua, not baimiao, generic sketching, manga, woodcut, or digital grayscale illustration.
- Hatching, cross-hatching, and stippling describe form deliberately; they do not become random noise, gray fog, or heavy black fill.
- The image retains readable white-paper reserve and a clear focal hierarchy at intended article or card size.
- Anatomy, hands, clothing folds, perspective, and spatial relations are coherent.
- The image has one intelligible narrative action and does not become a dense, muddy illustration.

Reject or revise when pen marks become scratchy, smooth digital shading replaces line construction, the figure loses black-and-white recognition, or tonal density obscures the article's cognitive anchor.
