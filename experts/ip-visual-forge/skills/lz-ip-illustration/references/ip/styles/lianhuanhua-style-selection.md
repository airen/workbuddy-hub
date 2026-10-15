# Chinese Nostalgic Narrative Rendering Presets: Selection and Validation

Use this guide only for **Chinese nostalgic narrative styles** in reusable IP systems. These include Chinese lianhuanhua, late-20th-century Chinese textbook illustration, region-specific New Year-picture, and Chinese shadow-puppetry. A rendering preset is a **locked component of the IP visual system**, not an article-by-article filter.

For the global style index, read `references/ip/styles/style-selection.md`.
For Japanese manga / animation styles, read `references/ip/styles/japanese-manga-style-selection.md`.

## Rendering Families

- **Chinese lianhuanhua family**: line, print, or controlled-color narrative illustration with stronger medium-specific structure.
- **Chinese textbook-illustration family**: hand-painted, life-observed, child-friendly instructional illustration with softer watercolor/gouache color and everyday narrative atmosphere.
- **Chinese freehand ink-wash narrative family**: expressive xieyi brush-and-ink causality using value hierarchy, paper reserve, and a small number of forceful marks; never reduce it to generic Chinese-style decoration, stock misty landscape, or ornate fantasy.
- **Chinese traditional New Year-picture family**: region-specific folk print-and-paint illustration for celebratory, auspicious, and high-recall narrative moments; never reduce it to generic red-and-gold festival branding.
- **Chinese shadow-puppetry family**: traditional folk-performance and carved translucent-puppet visual language, using backlit screen space, articulated figures, and visible causal action; never reduce it to generic paper-cut or a flat Chinese-style silhouette.

## Available Presets

| Preset | Best-fit IP role and article work | Identity locks | Do not confuse with |
|---|---|---|---|
| Traditional Chinese baimiao realistic lianhuanhua | Scholars, explainers, principles, frameworks, calm narrative instruction | silhouette, clothing/prop shape, light-midtone-dark mapping | generic ink wash, manga, poster art |
| Pen-and-ink realistic lianhuanhua | Technicians, builders, troubleshooting, tools, systems, assembly | silhouette, workwear/tool shapes, white reserve, line-density mapping | baimiao or smooth digital grayscale |
| Gongbi line-and-color realistic lianhuanhua | Meticulous designers, organizers, cultural/technical systems, calm structured explanation | silhouette plus palette roles and exact color placement | glossy Chinese-fantasy art or decorative costume imagery |
| Woodcut-print realistic lianhuanhua | Field repair, links, breaks, recovery, forceful directional action | silhouette, stance, prop shape, black-white mass map, carving-mark direction | propaganda poster, folk stamp, rough texture overlay |
| Late-20th-century Chinese realistic watercolor-and-gouache textbook illustration | Children, family, school, community, nature, gentle life-based teaching | silhouette, approachable expression range, clothing/prop shapes, palette roles and placement, watercolor/gouache balance | lianhuanhua line art, gongbi, flat decorative cartoon, glossy digital retro filter |
| Freehand Ink-Wash Technical Narrative / 写意水墨技术叙事 **(candidate, revision 2)** | Technical guides, maintainers, and makers showing a failure → trace → repair → verification workflow through Signal-Path Poster or Loose Technical Strip composition | each IP’s own silhouette and signature props, its own flow→fault→verified state map, near-black causal anchors, dominant route, repeatable repair gestures | monochrome mood ink wash, generic ink landscape, decorative Chinese-style moodboard, gongbi, line-led lianhuanhua, wuxia/palace fantasy, clean SaaS infographic, or disconnected collage |
| Mianzhu woodblock New Year picture | Active host, maker, organizer, messenger, or celebrant; festive cover, welcome, renewal, milestone, shared-value or auspicious-transformation narrative | silhouette, signature clothing/prop shapes, printed deep-ink contour plus hand-painted color relationship, palette roles and placement, balanced hierarchy | generic red-gold commercial poster, vector papercut, generic guochao, static guardian pose, or another regional New Year-picture tradition |
| Chinese shadow puppetry | Guide, operator, maker, diagnostician, or storyteller; reveal, connection, repair, transformation, or one visible causal action in shallow screen space | side-profile or three-quarter silhouette, articulated-joint grammar, signature costume/prop shapes, pierced-cutout motif family, translucent color placement, screen/backlight relationship | generic paper-cut, opaque vector silhouette, New-Year poster, generic guochao, unjointed decorative puppet, or deep-perspective theatre scene |

## Preset-Specific Test Pattern

Every new Chinese nostalgic preset must pass independently. Do not reuse another preset's reference image, prompt block, or acceptance result.

This test pattern applies to Chinese lianhuanhua, textbook-illustration, traditional New Year-picture, and shadow-puppetry presets.

1. Create an independent temporary IP selected to stress the preset's strengths.
2. Generate one portrait visual master and archive its prompt beside it.
3. Use that master as an image-to-image identity reference for two landscape article scenes:
   - one orchestration / explanation scene;
   - one diagnosis / repair / transformation scene.
4. Archive all prompts, images, dimensions, and a `qa-notes.md` record.
5. Require human visual approval before marking the preset passed.
6. Keep the test IP temporary unless the user separately approves it as a production IP.

## Tested Pairings

- Baimiao: Song Confucian scholar explaining Agent and Skill relationships.
- Pen-and-ink: modern technical maintenance worker wiring and repairing modular systems.
- Gongbi: Song female craft engineer arranging and correcting mechanism modules.
- Woodcut: mountain communications repairer establishing and restoring links.
- Late-20th-century watercolor-and-gouache textbook illustration: community young maker explaining coordination and repair flows; human visual QA approved on 2026-07-11.
- Mianzhu woodblock New Year picture: community “Good-Fortune Repair Shop” host coordinating lantern preparation and restoring a loose lantern connection; human visual QA approved on 2026-07-11. Test IP remains temporary.

These pairings demonstrate useful stress tests; they are not mandatory character choices for future production IPs.
