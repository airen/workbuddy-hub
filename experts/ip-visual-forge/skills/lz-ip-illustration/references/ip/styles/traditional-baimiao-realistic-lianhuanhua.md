# Traditional Chinese Baimiao Realistic Lianhuanhua Style Preset

Use this preset only when the user explicitly selects **Traditional Chinese baimiao realistic lianhuanhua** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a **locked rendering style**, not a one-off retro filter and not a freely switchable article-level variant.

For an IP using this preset:

```text
IP visual = fixed character identity + Traditional Chinese baimiao realistic lianhuanhua rendering
```

Lock it in `visual-spec.md`, repeat it in `prompt-pack.md`, and use the accepted visual master as the identity reference for downstream scenes.

Do not mix this preset with woodcut, ink-wash, gongbi color painting, Japanese manga, American comics, vintage poster art, game concept art, or generic "Chinese style" rendering unless the user explicitly revises the entire IP visual system.

## Visual Language

- Medium: black-and-white Chinese lianhuanhua illustration in the tradition of late 20th-century realistic line art.
- Linework: controlled, fine ink contour lines; clear silhouettes; deliberate clothing folds; selective hatching and cross-hatching for volume.
- Figure drawing: credible, proportionate bodies and hands; expressive but restrained faces; readable gestures.
- Light and space: restrained grayscale through line density rather than glossy digital shading; clear foreground, middle ground, and background depth.
- Composition: one self-contained narrative moment; cinematic but readable framing; a single image may use a local story-panel rhythm, but do not force comic panels into every scene.
- Texture: subtle aged book-paper or traditional print texture only when it does not reduce clarity.
- Text: normally no in-image text. When necessary, use only short Chinese labels; do not imitate speech balloons as the default narrative device.

## Identity Preservation Rules

The rendering is monochrome, so preserve recognition through non-color anchors:

- head and face silhouette
- body proportion
- signature clothing cut, collar, hat, glasses, or accessory shape
- signature object or motif
- repeatable gesture vocabulary

If the IP has a color palette, record a grayscale mapping in the visual spec: identify the character's light, midtone, and dark clothing/prop areas. Do not rely on hue alone to distinguish the IP.

## Prompt Block

Use this in the Base Style Prompt and adapt it to the scene:

```text
Traditional Chinese baimiao realistic lianhuanhua illustration, black-and-white late-20th-century Chinese serialized picture-book line art; disciplined fine ink contours, realistic anatomy and clothing folds, selective pen hatching and cross-hatching for restrained tonal volume, cinematic narrative composition, clear foreground-midground-background depth, subtle traditional book-print paper texture, high legibility at article size.
```

## Negative Prompt Block

```text
Japanese manga or anime, American superhero comic, chibi or kawaii cartoon, glossy digital painting, 3D render, colorful gongbi painting, freehand ink-wash, woodcut print, propaganda poster, calendar-poster woman, fantasy game concept art, photorealistic photo, speech bubbles, dense text, illegible hatching, muddy monochrome, decorative retro filter.
```

## Scene Rules

- The IP must perform the explanatory action; keep the central action clear before adding period texture.
- Prefer one clear narrative moment rather than a dense poster or full-page infographic.
- For workflow/comparison/diagnosis scenes, use objects, gesture, framing, and short labels to make relationships readable.
- For a mini-comic, use 2-4 clearly separated panels only when temporal change is essential.
- Keep modern tools or interfaces visually simplified; do not let anachronistic props turn the image into a costume drama.

## Style QA Additions

Accept only when all are true:

- The character remains recognizable in black and white without depending on color.
- Fine lines and hatching remain readable at intended article or card size.
- The result reads as restrained realistic Chinese lianhuanhua line art, not generic retro Chinese imagery.
- Anatomy, hands, clothing folds, and spatial relations are coherent.
- The image has one intelligible narrative action and does not become a dense, muddy illustration.

Reject or revise when it drifts toward any excluded style, uses excessive paper noise, makes the IP unrecognizable, or obscures the article's cognitive anchor.
