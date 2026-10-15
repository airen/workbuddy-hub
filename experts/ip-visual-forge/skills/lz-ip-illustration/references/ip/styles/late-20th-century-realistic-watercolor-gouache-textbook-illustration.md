# Late-20th-Century Chinese Realistic Watercolor-and-Gouache Textbook Illustration Preset

Use this preset only when the user explicitly selects **Late-20th-century Chinese realistic watercolor-and-gouache textbook illustration** as the rendering style for a new IP, or explicitly revises an existing IP to this style.

## Position in the IP System

This is a **locked rendering style** in the Chinese textbook-illustration family. It is not a generic nostalgic filter, not a temporary retro color grade, and not a freely switchable article-level variant.

For an IP using this preset:

```text
IP visual = fixed character identity + late-20th-century Chinese realistic watercolor-and-gouache textbook illustration rendering
```

Lock the character's silhouette, facial expression range, clothing, prop shapes, palette roles, paper/value treatment, and brushwork constraints in `visual-spec.md`; repeat them in `prompt-pack.md`; use the accepted visual master as the identity reference for downstream scenes.

Do not mix this preset with Traditional Chinese baimiao, pen-and-ink realistic lianhuanhua, gongbi line-and-color, woodcut-print lianhuanhua, freehand ink-wash, children’s decorative cartoon art, Japanese manga, American comics, glossy digital illustration, game concept art, photo realism, or generic "Chinese style" rendering unless the user explicitly revises the entire IP visual system.

## What This Preset Is

This preset evokes the visual language common in late-20th-century Chinese primary-school textbook illustrations: realistic but approachable people and everyday scenes, simple narrative composition, low-saturation hand-painted color, gentle natural light, and educational warmth.

It is a **textbook illustration family**, not a lianhuanhua family. It prioritizes life observation, child-friendly clarity, and a warm instructional atmosphere over strong line-media identity, dramatic heroic force, or ornate historical costume.

## Difference from Existing Rendering Presets

| Dimension | Late-20th-century realistic watercolor-and-gouache textbook illustration | Gongbi line-and-color lianhuanhua | Traditional Chinese baimiao | Pen-and-ink realistic lianhuanhua | Woodcut-print realistic lianhuanhua |
|---|---|---|---|---|---|
| Medium | transparent watercolor washes plus restrained opaque gouache accents | fine ink outline plus contained layered color | monochrome brush-like contour | monochrome technical-pen contour and hatching | monochrome carved black-white masses |
| Color | low-saturation, light-bearing, hand-painted color fields | controlled precise line-contained color | black-and-white only | black-and-white only | black-and-white only |
| Line role | soft pencil or light ink support; never dominant | precise contour is primary | contour is primary | pen and hatching are primary | carved mass is primary |
| Scene feeling | everyday, warm, open, child-friendly, observational | meticulous, calm, structured | airy, flowing, line-led | technical, structural, observational | bold, tactile, forceful |
| Best fit | children, family, school, community, nature, gentle teaching | precision, organization, cultural/technical systems | principles, scholars, calm instruction | tools, assembly, troubleshooting | links, breaks, recovery, directional action |

Do not use another preset's prompt block, reference image, or QA result as evidence that this preset has passed.

## Visual Language

- Medium: hand-painted realistic Chinese textbook illustration with watercolor washes and controlled gouache accents.
- Drawing: credible but friendly proportions, clear gestures, natural faces, and life-observed clothing. Support drawing uses soft pencil or light ink selectively; hard contouring must not dominate the image.
- Color: low-saturation, harmonious palette with warm paper neutrals and restrained blue, green, ochre, earth-red, or grey accents as appropriate to the specific IP. Color fields may be slightly irregular and hand-painted, but must remain clean and intentional.
- Light and material: gentle daylight, soft value transitions, visible watercolor transparency, selective matte gouache for important opaque forms. Do not use glossy gradients, dramatic cinematic bloom, thick impasto, plastic 3D rendering, or photographic texture.
- Composition: one self-contained everyday narrative moment, readable at a textbook-page or article-reading size. Use open space, a clear focal action, and enough environmental detail to ground the story without crowding it.
- Backgrounds: schoolyard, classroom, home, community, workshop, countryside, or nature may support the story when relevant. Background should provide lived context rather than decorative nostalgia.
- Text: normally no in-image text. When labels are necessary, use only short Chinese labels; do not use speech balloons as the default narrative device.

## Identity Preservation Rules

Color is a first-class identity constraint. Preserve recognition through both form and stable palette placement:

- head and face silhouette, expression range, and body proportion
- signature clothing cut and repeatable everyday accessory or prop
- stable palette roles and placement of the main garment, secondary garment, accent, and background neutral
- consistent watercolor transparency versus gouache-opacity balance
- repeatable gesture vocabulary and approachable emotional tone

Record the palette in `visual-spec.md` with named roles:

```text
paper neutral / main garment color / secondary garment color / warm accent / cool accent / signature-prop accent / skin tone range / environmental support colors
```

Use color to establish warmth, subject hierarchy, and recognizability. Do not rely on heavy outlines, saturation, or decorative texture to rescue a weak silhouette.

## Prompt Block

Use this in the Base Style Prompt and adapt it to the scene:

```text
Late-20th-century Chinese realistic watercolor-and-gouache primary-school textbook illustration, hand-painted low-saturation watercolor washes with selective matte gouache accents, natural gentle daylight, credible but approachable anatomy and expressions, soft pencil or light ink support drawing, warm paper-neutral background, clean open composition, everyday narrative clarity, restrained blue-green-ochre-earth-red palette roles, visible but controlled watercolor transparency, high legibility at textbook-page and article size.
```

## Negative Prompt Block

```text
Chinese lianhuanhua line art, gongbi fine-outline color, baimiao ink contour, pen-and-ink hatching, woodcut print, freehand ink-wash, children’s decorative flat cartoon, chibi, Japanese manga or anime, American superhero comic, glossy digital painting, 3D render, photorealistic photo, oversaturated rainbow palette, neon color, plastic smooth gradients, thick impasto oil paint, dramatic fantasy light, vintage poster filter, distressed paper overlay, propaganda poster, dense text, speech bubbles, fake calligraphy, cluttered decorative nostalgia.
```

## Scene Rules

- The IP must perform the explanatory action; warmth and nostalgia cannot replace narrative participation.
- Prefer one calm, life-observed narrative moment rather than a crowded poster, comic page, or dense infographic.
- For technical concepts, translate the system into approachable tangible objects, classroom/workshop tasks, neighborhood scenes, or simple nature metaphors without making the IP merely a teacher beside a finished diagram.
- Use the strongest color contrast for the IP’s action, central object, or before/after change; keep environmental colors quieter.
- Maintain breathing room and a natural reading path. Do not overfill the background with period props just to signal nostalgia.
- Keep modern tools or interfaces visually simplified and human-scaled; avoid literal software dashboards, glossy technology art, or anachronistic costume drama.

## Style QA Additions

Accept only when all are true:

- The character remains recognizable through stable silhouette, approachable expression, clothing/prop shape, and consistent palette placement.
- The result reads as realistic late-20th-century Chinese watercolor-and-gouache textbook illustration, not lianhuanhua, gongbi, ink wash, generic children’s cartoon, glossy digital art, manga, or photo realism.
- Watercolor transparency and matte gouache accents are visible but controlled; edges may be softly hand-painted without becoming muddy, airbrushed, or over-textured.
- Palette is low-saturation, harmonious, and supports a warm instructional hierarchy; it is not flat decorative color, neon, or uniformly saturated nostalgia.
- Faces, hands, gestures, and everyday objects remain natural and readable at intended article or textbook size.
- The scene has one intelligible explanatory action and enough lived context to ground it without becoming a decorative memory collage.

Reject or revise when the result becomes a generic retro filter, a line-art lianhuanhua, flat cartoon iconography, glossy fantasy painting, overly sentimental clutter, or an image where the IP can be removed without harming the explanation.
